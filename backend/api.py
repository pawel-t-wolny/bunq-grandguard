import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime

# -----------------------------
# Config
# -----------------------------

MODEL_PATH = "xgboost_binary_scam_model.joblib"

# Choose the threshold based on your earlier threshold evaluation.
# 0.40 is a reasonable starting point, but tune this.
SCAM_THRESHOLD = 0.40


# -----------------------------
# Load model
# -----------------------------

import joblib
import sklearn.compose._column_transformer as sklearn_column_transformer

class _RemainderColsList(list):
    pass

if not hasattr(sklearn_column_transformer, "_RemainderColsList"):
    sklearn_column_transformer._RemainderColsList = _RemainderColsList

model = joblib.load(MODEL_PATH)


# -----------------------------
# FastAPI app
# -----------------------------

app = FastAPI(
    title="Payment Scam Detection API",
    description="Predicts whether a bunq-style payment object is a scam.",
    version="1.0.0",
)


# -----------------------------
# Request / response models
# -----------------------------

class ScamPredictionResponse(BaseModel):
    is_scam: bool


# -----------------------------
# Feature definitions
# Must match training notebook exactly
# -----------------------------

NUMERIC_FEATURES = [
    "amount_value",
    "amount_abs",
    "balance_after",
    "balance_after_abs",
    "amount_balance_ratio",

    "created_hour",
    "created_dayofweek",
    "created_month",
    "is_weekend",
    "is_night",

    "is_outgoing",
    "is_incoming",

    "attachment_count",
    "has_attachment",
    "has_merchant_reference",
]

CATEGORICAL_FEATURES = [
    "payment_type",
    "sub_type",
    "amount_currency",
    "counterparty_country",
    "counterparty_user_type",
    "counterparty_bank_code",
    "own_bank_code",
    "payment_arrival_status",
]

FEATURE_COLS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


# -----------------------------
# Helper functions
# -----------------------------

def extract_bank_code(iban: Optional[str]) -> Optional[str]:
    if not isinstance(iban, str):
        return None

    if len(iban) >= 8:
        return iban[4:8]

    return None


def flatten_payment(payment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes one bunq-style Payment object, not wrapped in {"Payment": ...}.

    Expected input shape:

    {
        "id": 26174613,
        "created": "...",
        "amount": {"currency": "EUR", "value": "-50.00"},
        "alias": {...},
        "counterparty_alias": {...},
        ...
    }
    """

    counterparty = payment.get("counterparty_alias", {}) or {}
    counterparty_label = counterparty.get("label_user", {}) or {}

    alias = payment.get("alias", {}) or {}
    alias_label = alias.get("label_user", {}) or {}

    payment_arrival = payment.get("payment_arrival_expected", {}) or {}

    amount_obj = payment.get("amount", {}) or {}
    balance_obj = payment.get("balance_after_mutation", {}) or {}

    amount_value = float(amount_obj.get("value", 0.0))
    balance_after = float(balance_obj.get("value", 0.0))

    return {
        "payment_id": payment.get("id"),
        "created": payment.get("created"),
        "updated": payment.get("updated"),
        "monetary_account_id": payment.get("monetary_account_id"),

        "amount_value": amount_value,
        "amount_currency": amount_obj.get("currency", "EUR"),

        # Text fields are intentionally not used as model features.
        "description": payment.get("description", ""),
        "counterparty_display_name": counterparty.get("display_name"),

        "payment_type": payment.get("type"),
        "sub_type": payment.get("sub_type"),
        "merchant_reference": payment.get("merchant_reference"),

        "own_display_name": alias.get("display_name"),
        "own_iban": alias.get("iban"),
        "own_user_type": alias_label.get("type"),

        "counterparty_iban": counterparty.get("iban"),
        "counterparty_country": counterparty.get("country"),
        "counterparty_user_type": counterparty_label.get("type"),

        "attachment_count": len(payment.get("attachment", []) or []),
        "payment_arrival_status": payment_arrival.get("status"),

        "balance_after": balance_after,
    }


def build_features(payment: Dict[str, Any]) -> pd.DataFrame:
    """
    Converts one payment object into a one-row DataFrame
    with the exact columns expected by the trained model pipeline.
    """

    row = flatten_payment(payment)
    df = pd.DataFrame([row])

    df["created_dt"] = pd.to_datetime(df["created"], errors="coerce")

    df["created_hour"] = df["created_dt"].dt.hour.fillna(0).astype(int)
    df["created_dayofweek"] = df["created_dt"].dt.dayofweek.fillna(0).astype(int)
    df["created_month"] = df["created_dt"].dt.month.fillna(0).astype(int)

    df["is_weekend"] = df["created_dayofweek"].isin([5, 6]).astype(int)
    df["is_night"] = df["created_hour"].between(0, 5).astype(int)

    df["amount_abs"] = df["amount_value"].abs()
    df["is_outgoing"] = (df["amount_value"] < 0).astype(int)
    df["is_incoming"] = (df["amount_value"] > 0).astype(int)

    df["balance_after_abs"] = df["balance_after"].abs()
    df["amount_balance_ratio"] = df["amount_abs"] / (df["balance_after_abs"] + 1)

    df["has_merchant_reference"] = df["merchant_reference"].notna().astype(int)
    df["has_attachment"] = (df["attachment_count"] > 0).astype(int)

    df["counterparty_bank_code"] = df["counterparty_iban"].apply(extract_bank_code)
    df["own_bank_code"] = df["own_iban"].apply(extract_bank_code)

    # Make sure all expected feature columns exist.
    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = None

    X = df[FEATURE_COLS].copy()

    return X


# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Payment scam detection API is running.",
    }


@app.post("/predict", response_model=ScamPredictionResponse)
def predict(payment: Dict[str, Any]):
    X = build_features(payment)

    print(X)

    scam_probability = model.predict_proba(X)[0, 1]
    is_scam = bool(scam_probability >= SCAM_THRESHOLD)

    print(payment)
    print(datetime.now())
    print(is_scam)

    return {
        "is_scam": is_scam
    }