"""
NEULIF: Train CNN and Random Forest classifiers on stylometric features
to detect AI-generated text. Based on Aityan et al. (2025).

Run with:  python train.py
"""

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib
import kagglehub
import spacy
import textdescriptives as td

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, classification_report, roc_auc_score, log_loss
)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


SAMPLE_SIZE  = 20_000   # balanced: 10k AI + 10k human
RANDOM_STATE = 42
MODELS_DIR   = "models"
os.makedirs(MODELS_DIR, exist_ok=True)


# ── 1. Dataset ─────────────────────────────────────────────────────────────────
def load_dataset() -> pd.DataFrame:
    print("Downloading dataset from Kaggle …")
    path = kagglehub.dataset_download("shanegerami/ai-vs-human-text")
    print(f"Dataset path: {path}")

    csv_files = [f for f in os.listdir(path) if f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError(f"No CSV found in {path}")
    df = pd.read_csv(os.path.join(path, csv_files[0]))
    print(f"Raw dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    return df


def balance_sample(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower() for c in df.columns]

    # Detect text column
    text_col = next(
        (c for c in df.columns if "text" in c),
        df.columns[0]
    )
    # Detect label column
    label_candidates = [c for c in df.columns if c in ("generated", "label", "ai", "class", "source")]
    label_col = label_candidates[0] if label_candidates else df.columns[-1]

    df = df[[text_col, label_col]].rename(columns={text_col: "text", label_col: "label"})
    df["label"] = df["label"].astype(int)
    df = df.dropna(subset=["text"])
    df = df[df["text"].str.strip().astype(bool)]

    per_class = SAMPLE_SIZE // 2
    ai    = df[df["label"] == 1].sample(min(per_class, (df["label"] == 1).sum()), random_state=RANDOM_STATE)
    human = df[df["label"] == 0].sample(min(per_class, (df["label"] == 0).sum()), random_state=RANDOM_STATE)
    balanced = pd.concat([ai, human]).sample(frac=1, random_state=RANDOM_STATE).reset_index(drop=True)
    print(f"Balanced sample: {balanced.shape}  (AI={len(ai)}, Human={len(human)})")
    return balanced


# ── 2. Feature extraction ──────────────────────────────────────────────────────
def build_nlp():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textdescriptives/all")
    return nlp


def extract_features(texts: list, nlp) -> pd.DataFrame:
    print(f"Extracting features from {len(texts)} texts …")
    docs = list(nlp.pipe(texts, batch_size=64))
    df_feat = td.extract_metrics(docs, spacy_model="en_core_web_sm", metrics=None)
    numeric_cols = df_feat.select_dtypes(include=[np.number]).columns.tolist()
    print(f"Numeric features available: {len(numeric_cols)}")
    return df_feat[numeric_cols].reset_index(drop=True)


# ── 3. Preprocessing ───────────────────────────────────────────────────────────
def preprocess(X: pd.DataFrame, y: pd.Series):
    # Drop rows where any feature is NaN
    mask = ~X.isnull().any(axis=1)
    X, y = X[mask].reset_index(drop=True), y[mask].reset_index(drop=True)
    print(f"After NaN drop: {X.shape}")

    X_tr, X_tmp, y_tr, y_tmp = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    X_val, X_te, y_val, y_te = train_test_split(
        X_tmp, y_tmp, test_size=0.5, random_state=RANDOM_STATE, stratify=y_tmp
    )

    scaler = StandardScaler()
    X_tr  = scaler.fit_transform(X_tr)
    X_val = scaler.transform(X_val)
    X_te  = scaler.transform(X_te)

    print(f"Train={len(y_tr)}  Val={len(y_val)}  Test={len(y_te)}")
    joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.joblib"))
    return X_tr, X_val, X_te, y_tr.values, y_val.values, y_te.values


# ── 4. CNN ─────────────────────────────────────────────────────────────────────
def build_cnn(n_features: int) -> keras.Model:
    inp = keras.Input(shape=(n_features, 1))
    x   = layers.Conv1D(128, kernel_size=3, activation="relu", padding="same")(inp)
    x   = layers.BatchNormalization()(x)
    x   = layers.Flatten()(x)
    x   = layers.Dense(256, activation="relu")(x)
    x   = layers.Dropout(0.4)(x)
    x   = layers.Dense(128, activation="relu")(x)
    x   = layers.Dropout(0.3)(x)
    x   = layers.Dense(64, activation="relu")(x)
    x   = layers.Dropout(0.2)(x)
    out = layers.Dense(1, activation="sigmoid")(x)
    model = keras.Model(inp, out)
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.summary()
    return model


def train_cnn(X_tr, y_tr, X_val, y_val):
    n_features = X_tr.shape[1]
    X_tr3  = X_tr.reshape(-1, n_features, 1)
    X_val3 = X_val.reshape(-1, n_features, 1)

    model = build_cnn(n_features)
    cb = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(
            os.path.join(MODELS_DIR, "cnn_best.keras"),
            save_best_only=True, monitor="val_loss"
        ),
    ]
    model.fit(
        X_tr3, y_tr,
        validation_data=(X_val3, y_val),
        epochs=50, batch_size=64,
        callbacks=cb, verbose=1
    )
    return model, n_features


def evaluate_cnn(model, X_te, y_te, n_features):
    X_te3 = X_te.reshape(-1, n_features, 1)
    probs = model.predict(X_te3).flatten()
    preds = (probs >= 0.5).astype(int)
    print("\n─── CNN Test Results ───────────────────────────────")
    print(f"Accuracy : {accuracy_score(y_te, preds):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_te, probs):.4f}")
    print(f"Log Loss : {log_loss(y_te, probs):.4f}")
    print(classification_report(y_te, preds, target_names=["Human", "AI"]))


# ── 5. Random Forest ───────────────────────────────────────────────────────────
def train_rf(X_tr, y_tr, X_val, y_val):
    rf = RandomForestClassifier(
        n_estimators=100, criterion="gini", random_state=RANDOM_STATE, n_jobs=-1
    )
    rf.fit(X_tr, y_tr)
    val_acc = accuracy_score(y_val, rf.predict(X_val))
    print(f"RF validation accuracy: {val_acc:.4f}")
    return rf


def evaluate_rf(rf, X_te, y_te):
    probs = rf.predict_proba(X_te)[:, 1]
    preds = rf.predict(X_te)
    print("\n─── Random Forest Test Results ─────────────────────")
    print(f"Accuracy : {accuracy_score(y_te, preds):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_te, probs):.4f}")
    print(f"Log Loss : {log_loss(y_te, probs):.4f}")
    print(classification_report(y_te, preds, target_names=["Human", "AI"]))


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    df  = load_dataset()
    df  = balance_sample(df)

    nlp   = build_nlp()
    X_raw = extract_features(df["text"].tolist(), nlp)
    y     = df["label"]

    # Save feature column names for inference
    joblib.dump(X_raw.columns.tolist(), os.path.join(MODELS_DIR, "feature_cols.joblib"))

    X_tr, X_val, X_te, y_tr, y_val, y_te = preprocess(X_raw, y)

    print("\n═══ Training CNN ═══════════════════════════════════")
    cnn, n_features = train_cnn(X_tr, y_tr, X_val, y_val)
    evaluate_cnn(cnn, X_te, y_te, n_features)
    cnn.save(os.path.join(MODELS_DIR, "cnn_final.keras"))
    print("CNN saved →", os.path.join(MODELS_DIR, "cnn_final.keras"))

    print("\n═══ Training Random Forest ═════════════════════════")
    rf = train_rf(X_tr, y_tr, X_val, y_val)
    evaluate_rf(rf, X_te, y_te)
    joblib.dump(rf, os.path.join(MODELS_DIR, "rf.joblib"))
    print("RF saved  →", os.path.join(MODELS_DIR, "rf.joblib"))


if __name__ == "__main__":
    main()
