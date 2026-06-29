"""
Predict AI-generation probability for one or more texts.

Usage (activate venv first):
    python predict.py --text "Your text here"
    python predict.py --file my_essay.txt
    python predict.py --model cnn        (default)
    python predict.py --model rf
    python predict.py --model both

Output: score 0-100 where 0 = certainly human, 100 = certainly AI.
"""

import argparse
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib
import spacy
import textdescriptives as td


MODELS_DIR = "models"


def load_artifacts(model_type: str):
    scaler       = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
    feature_cols = joblib.load(os.path.join(MODELS_DIR, "feature_cols.joblib"))

    cnn, rf = None, None
    if model_type in ("cnn", "both"):
        from tensorflow import keras
        cnn = keras.models.load_model(os.path.join(MODELS_DIR, "cnn_final.keras"))
    if model_type in ("rf", "both"):
        rf = joblib.load(os.path.join(MODELS_DIR, "rf.joblib"))

    return scaler, feature_cols, cnn, rf


def extract_features_for_text(text: str, nlp, feature_cols: list) -> np.ndarray:
    doc    = nlp(text)
    df_raw = td.extract_metrics([doc], spacy_model="en_core_web_sm", metrics=None)
    numeric = df_raw.select_dtypes(include=[np.number])
    # Align to training columns, fill missing with 0
    row = numeric.reindex(columns=feature_cols, fill_value=0).fillna(0)
    return row.values.astype(np.float32)


def predict_text(text: str, nlp, scaler, feature_cols, cnn, rf, model_type: str) -> dict:
    feats        = extract_features_for_text(text, nlp, feature_cols)
    feats_scaled = scaler.transform(feats)

    results = {}

    if cnn is not None:
        feats_3d    = feats_scaled.reshape(1, -1, 1)
        prob_cnn    = float(cnn.predict(feats_3d, verbose=0)[0][0])
        results["cnn"] = round(prob_cnn * 100, 1)

    if rf is not None:
        prob_rf     = float(rf.predict_proba(feats_scaled)[0][1])
        results["rf"] = round(prob_rf * 100, 1)

    if model_type == "both" and cnn is not None and rf is not None:
        results["ensemble"] = round((results["cnn"] + results["rf"]) / 2, 1)

    return results


def verdict(score: float) -> str:
    if score >= 75:
        return "Very likely AI-generated"
    elif score >= 50:
        return "Possibly AI-generated"
    elif score >= 25:
        return "Possibly human-written"
    else:
        return "Very likely human-written"


def main():
    parser = argparse.ArgumentParser(description="AI text detector — score 0-100")
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text string to analyse")
    group.add_argument("--file", type=str, help="Path to a text file to analyse")
    parser.add_argument(
        "--model", choices=["cnn", "rf", "both"], default="cnn",
        help="Which trained model to use (default: cnn)"
    )
    args = parser.parse_args()

    text = args.text if args.text else open(args.file).read()
    if not text.strip():
        raise ValueError("Input text is empty.")

    print("Loading models …")
    scaler, feature_cols, cnn, rf = load_artifacts(args.model)

    print("Loading NLP pipeline …")
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textdescriptives/all")

    print("Running inference …")
    scores = predict_text(text, nlp, scaler, feature_cols, cnn, rf, args.model)

    print("\n── AI-Generation Score ─────────────────────────────")
    print(f"  Words in input : {len(text.split())}")
    for name, score in scores.items():
        label = {"cnn": "CNN", "rf": "Random Forest", "ensemble": "Ensemble (avg)"}[name]
        bar   = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"  {label:16s}: [{bar}]  {score:.1f}/100")
    print()

    final = scores.get("ensemble") or scores.get("cnn") or scores.get("rf")
    print(f"  Verdict: {verdict(final)} ({final:.1f}/100)\n")


if __name__ == "__main__":
    main()
