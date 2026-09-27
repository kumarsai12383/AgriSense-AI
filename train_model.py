import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

DATASET_PATH = "dataset/Crop_recommendation.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "crop_model.pkl")


def train():
    print("[*] Starting AgriSense Crop Recommendation Model Training...")

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH)
    print(f"[+] Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
    print(f"[+] Unique crops ({len(df['label'].unique())}): {', '.join(sorted(df['label'].unique()))}")

    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    target = 'label'

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("[*] Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("\n[+] Model Evaluation:")
    print(f"[+] Test Accuracy: {acc * 100:.2f}%\n")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[+] Model saved successfully to: {MODEL_PATH}")


if __name__ == "__main__":
    train()

