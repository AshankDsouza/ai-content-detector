"""
AI Text Detector — REST API

Endpoints:
  POST /submit           Submit text for attribution analysis
  POST /appeal/<id>      Contest a classification decision
  GET  /log              View the structured audit log
"""

import os
import uuid
import sqlite3
import warnings
import logging
from datetime import datetime, timezone

warnings.filterwarnings("ignore")

import numpy as np
import joblib
import spacy
import textdescriptives as td
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from detection_methods.digital_traces_detection import analyze as analyze_digital_traces
from detection_methods.stylometric_detection import stylometric as analyze_stylometric

# ── Config ────────────────────────────────────────────────────────────────────
MODELS_DIR = "models"
DB_PATH = "audit.db"

# ── App & Rate Limiter ────────────────────────────────────────────────────────
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── Database ──────────────────────────────────────────────────────────────────
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS submissions (
                id                  TEXT PRIMARY KEY,
                submitted_at        TEXT NOT NULL,
                text_preview        TEXT,
                word_count          INTEGER,
                cnn_score           REAL,
                rf_score            REAL,
                ensemble_score      REAL,
                attribution         TEXT,
                confidence          REAL,
                transparency_label  TEXT,
                status              TEXT DEFAULT 'decided'
            );

            CREATE TABLE IF NOT EXISTS appeals (
                id                  TEXT PRIMARY KEY,
                submission_id       TEXT NOT NULL,
                appealed_at         TEXT NOT NULL,
                creator_reasoning   TEXT,
                FOREIGN KEY(submission_id) REFERENCES submissions(id)
            );
        """)


# ── Model Singletons ──────────────────────────────────────────────────────────
_nlp = None
_scaler = None
_feature_cols = None
_cnn = None
_rf = None
_models_ready = False


def load_models():
    global _nlp, _scaler, _feature_cols, _cnn, _rf, _models_ready
    logger.info("Loading spaCy + TextDescriptives pipeline…")
    _nlp = spacy.load("en_core_web_sm")
    _nlp.add_pipe("textdescriptives/all")

    logger.info("Loading scaler and feature columns…")
    _scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
    _feature_cols = joblib.load(os.path.join(MODELS_DIR, "feature_cols.joblib"))

    logger.info("Loading CNN model…")
    from tensorflow import keras
    _cnn = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_final.keras"))

    logger.info("Loading Random Forest model…")
    _rf = joblib.load(os.path.join(MODELS_DIR, "rf.joblib"))

    _models_ready = True
    logger.info("All models loaded and ready.")


# ── Inference ─────────────────────────────────────────────────────────────────
def extract_features(text: str) -> np.ndarray:
    doc = _nlp(text)
    df_raw = td.extract_metrics([doc], spacy_model="en_core_web_sm", metrics=None)
    numeric = df_raw.select_dtypes(include=[np.number])
    row = numeric.reindex(columns=_feature_cols, fill_value=0).fillna(0)
    return row.values.astype(np.float32)


def run_inference(text: str) -> dict:
    feats = extract_features(text)
    feats_scaled = _scaler.transform(feats)

    prob_cnn = float(_cnn.predict(feats_scaled.reshape(1, -1, 1), verbose=0)[0][0])
    prob_rf = float(_rf.predict_proba(feats_scaled)[0][1])
    ensemble_prob = 0.75 * prob_cnn + 0.25 * prob_rf

    cnn_score = round(prob_cnn * 100, 1)
    rf_score = round(prob_rf * 100, 1)
    ensemble_score = round(ensemble_prob * 100, 1)

    confidence = round(abs(ensemble_prob - 0.5) * 2, 4)

    return {
        "cnn_score": cnn_score,
        "rf_score": rf_score,
        "ensemble_score": ensemble_score,
        "confidence": confidence,
    }


STYLOMETRIC_FAIL_THRESHOLD = 50


def determine_verdict(ensemble_score: float, trace_verdict: str) -> str:
    """Return 'ai' or 'human' per planning.md thresholds."""
    if ensemble_score >= 80:
        return "ai"
    if ensemble_score >= 75 and trace_verdict == "red":
        return "ai"
    return "human"


def build_transparency_label(ensemble_score: float, trace_verdict: str, is_ai: bool) -> str:
    if is_ai:
        return "High-confidence AI-generated"
    if ensemble_score < 25 and trace_verdict == "green":
        return "High-confidence human-generated"
    return "Uncertain"


def build_warning_report(trace: dict, styl: dict) -> dict:
    return {
        "digital_trace_report": trace,
        "stylometric_report": styl,
    }


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute; 50 per hour")
def submit():
    """
    Accept a piece of text and return an attribution analysis.

    Request body (JSON):
      { "text": "<string>" }

    Response (JSON):
      result, score, transparency_label, warning_report
    """
    if not _models_ready:
        return jsonify({"error": "Models are still loading. Please retry shortly."}), 503

    body = request.get_json(silent=True)
    if not body or "text" not in body:
        return jsonify({"error": "Request body must be JSON with a 'text' field."}), 400

    text = body["text"].strip()
    if not text:
        return jsonify({"error": "'text' must not be empty."}), 400
    if len(text.split()) < 20:
        return jsonify({"error": "Text must contain at least 20 words for a reliable analysis."}), 422

    try:
        result = run_inference(text)
        trace_report = analyze_digital_traces(text)
        stylometric_report = analyze_stylometric(text)
    except Exception as exc:
        logger.exception("Inference failed for new submission")
        return jsonify({"error": f"Inference error: {exc}"}), 500

    attribution = determine_verdict(result["ensemble_score"], trace_report["verdict"])
    is_ai = attribution == "ai"
    transparency_label = build_transparency_label(
        result["ensemble_score"], trace_report["verdict"], is_ai
    )
    warning_report = build_warning_report(trace_report, stylometric_report)

    submission_id = str(uuid.uuid4())
    submitted_at = datetime.now(timezone.utc).isoformat()
    text_preview = text[:200] + ("…" if len(text) > 200 else "")
    word_count = len(text.split())

    db = get_db()
    db.execute(
        """INSERT INTO submissions
               (id, submitted_at, text_preview, word_count,
                cnn_score, rf_score, ensemble_score,
                attribution, confidence, transparency_label, status)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            submission_id, submitted_at, text_preview, word_count,
            result["cnn_score"], result["rf_score"], result["ensemble_score"],
            attribution, result["confidence"],
            transparency_label, "decided",
        ),
    )
    db.commit()

    logger.info(
        "Submission %s | score=%.1f | result=%s | label=%s",
        submission_id, result["ensemble_score"],
        "failed" if is_ai else "passed", transparency_label,
    )

    return jsonify({
        "result": "failed" if is_ai else "passed",
        "confidence_score": round(result["ensemble_score"]),
        "transparency_label": transparency_label,
        "warning_report": warning_report,
        "submission_id": submission_id,
    }), 200


@app.route("/appeal/<submission_id>", methods=["POST"])
def appeal(submission_id):
    """
    Contest a classification decision.

    Request body (JSON):
      { "reasoning": "<string>" }

    Response (JSON):
      appeal_id, submission_id, appealed_at, status, message
    """
    db = get_db()
    row = db.execute(
        "SELECT id, status FROM submissions WHERE id = ?", (submission_id,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Submission not found."}), 404

    body = request.get_json(silent=True)
    if not body or "reasoning" not in body:
        return jsonify({"error": "Request body must be JSON with a 'reasoning' field."}), 400

    reasoning = body["reasoning"].strip()
    if not reasoning:
        return jsonify({"error": "'reasoning' must not be empty."}), 400

    appeal_id = str(uuid.uuid4())
    appealed_at = datetime.now(timezone.utc).isoformat()

    db.execute(
        "INSERT INTO appeals (id, submission_id, appealed_at, creator_reasoning) VALUES (?,?,?,?)",
        (appeal_id, submission_id, appealed_at, reasoning),
    )
    db.execute(
        "UPDATE submissions SET status = 'under_review' WHERE id = ?",
        (submission_id,),
    )
    db.commit()

    logger.info("Appeal %s filed for submission %s", appeal_id, submission_id)

    return jsonify({
        "appeal_id": appeal_id,
        "submission_id": submission_id,
        "appealed_at": appealed_at,
        "status": "under_review",
        "message": "Your appeal has been received. The submission is now under review.",
    }), 201

@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return jsonify({"status": "ok"}), 200

@app.route("/log", methods=["GET"])
def audit_log():
    """
    Return the full structured audit log.

    Each entry includes the attribution decision (with confidence score and
    signals used) and any appeals filed against it.

    Optional query params:
      ?limit=N    Maximum entries to return (default 100)
      ?offset=N   Skip N entries (for pagination)
    """
    try:
        limit = max(1, min(int(request.args.get("limit", 100)), 500))
        offset = max(0, int(request.args.get("offset", 0)))
    except ValueError:
        return jsonify({"error": "'limit' and 'offset' must be integers."}), 400

    db = get_db()
    rows = db.execute(
        """
        SELECT
            s.id               AS submission_id,
            s.submitted_at,
            s.text_preview,
            s.word_count,
            s.cnn_score,
            s.rf_score,
            s.ensemble_score,
            s.attribution,
            s.confidence,
            s.transparency_label,
            s.status,
            a.id               AS appeal_id,
            a.appealed_at,
            a.creator_reasoning
        FROM submissions s
        LEFT JOIN appeals a ON a.submission_id = s.id
        ORDER BY s.submitted_at DESC
        LIMIT ? OFFSET ?
        """,
        (limit * 10, offset),  # over-fetch to account for multi-appeal rows
    ).fetchall()

    # Group appeals under their parent submission
    entries = {}
    order = []
    for r in rows:
        sid = r["submission_id"]
        if sid not in entries:
            entries[sid] = {
                "submission_id": sid,
                "submitted_at": r["submitted_at"],
                "text_preview": r["text_preview"],
                "word_count": r["word_count"],
                "signals": {
                    "cnn_score": r["cnn_score"],
                    "rf_score": r["rf_score"],
                    "ensemble_score": r["ensemble_score"],
                },
                "attribution": r["attribution"],
                "confidence": r["confidence"],
                "transparency_label": r["transparency_label"],
                "status": r["status"],
                "appeals": [],
            }
            order.append(sid)
        if r["appeal_id"]:
            entries[sid]["appeals"].append({
                "appeal_id": r["appeal_id"],
                "appealed_at": r["appealed_at"],
                "creator_reasoning": r["creator_reasoning"],
            })

    result_list = [entries[sid] for sid in order][:limit]

    return jsonify({
        "total_returned": len(result_list),
        "limit": limit,
        "offset": offset,
        "entries": result_list,
    }), 200


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("initialising the rest api service")
    init_db()
    load_models()
    app.run(host="0.0.0.0", port=5001, debug=True)
    print("Service running on port 5001")
