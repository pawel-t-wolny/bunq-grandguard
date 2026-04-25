from __future__ import annotations

import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from app.schemas.scam_detection import BunqPaymentCheckRequest, ScamCheckResponse, TransactionCheckRequest

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).resolve().parents[2]
TRAINING_DATASET_PATH = ROOT_DIR / "bunq_synthetic_transactions.json"
TRAINING_LABELS_PATH = ROOT_DIR / "bunq_synthetic_transaction_labels.json"

TRUSTED_COUNTRIES = {"NL", "BE", "DE", "FR", "ES", "LU"}
LOW_RISK_THRESHOLD = 0.35
HIGH_RISK_THRESHOLD = 0.65
SCAM_THRESHOLD = 0.55
FORCE_SCAM_RULE_THRESHOLD = 0.82

SUSPICIOUS_TERMS = {
    "urgent",
    "verification",
    "verify",
    "security",
    "safe account",
    "fraud prevention",
    "refund",
    "customs",
    "douane",
    "parcel",
    "pakket",
    "delivery",
    "crypto",
    "investment",
    "wallet",
    "trading",
    "belasting",
    "tax",
    "invoice",
    "factuur",
    "giftcard",
    "cadeaukaart",
    "whatsapp",
    "new number",
    "voorschot",
    "dringend",
    "mam",
    "helpdesk",
    "support",
    "account control",
    "controle",
}

SPOOFED_ENTITY_TERMS = {
    "bunq",
    "bank",
    "support",
    "helpdesk",
    "verify",
    "verification",
    "safe account",
    "veilige rekening",
    "kluisrekening",
    "belasting",
    "tax",
    "customs",
    "douane",
    "postnl",
    "dhl",
    "parcel",
    "crypto",
    "trading",
}

SCAM_TYPE_HINTS = {
    "bank_impersonation": ["bunq", "bank", "support", "helpdesk", "verification", "verify", "security"],
    "safe_account": ["safe account", "veilige rekening", "kluisrekening", "fraud prevention", "veiligstellen"],
    "investment": ["crypto", "investment", "wallet", "trading", "belegging", "deposit"],
    "government_impersonation": ["belasting", "tax", "refund", "cjib", "gemeente", "office"],
    "delivery_fee": ["parcel", "pakket", "postnl", "dhl", "customs", "douane", "delivery"],
    "social_engineering": ["whatsapp", "new number", "mam", "voorschot", "dringend", "family"],
}


@dataclass
class NormalizedTransaction:
    transaction_id: str | None
    amount: float
    currency: str
    description: str
    counterparty_name: str
    counterparty_iban: str | None
    counterparty_country: str | None
    payment_type: str
    merchant_reference: str | None
    created_at: datetime | None
    direction: str


@dataclass
class RuleAssessment:
    score: float
    reasons: list[str]
    type_hint: str | None
    keyword_hits: int
    spoof_hits: int


class ScamDetector:
    engine_name = "hybrid-logistic-rules/v1"

    def __init__(self) -> None:
        self.binary_model: Pipeline | None = None
        self.type_model: Pipeline | None = None
        self.training_samples = 0
        self.scam_samples = 0
        self._train_models()

    def _train_models(self) -> None:
        if not TRAINING_DATASET_PATH.exists() or not TRAINING_LABELS_PATH.exists():
            logger.warning("Training files are missing. Falling back to rule-only scam detection.")
            return

        try:
            features_df, labels_df = self._load_training_frames()
            self.training_samples = len(features_df)
            self.scam_samples = int(labels_df["is_scam"].sum())

            binary_preprocessor = self._build_preprocessor()
            self.binary_model = Pipeline(
                steps=[
                    ("preprocessor", binary_preprocessor),
                    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
                ]
            )
            self.binary_model.fit(features_df, labels_df["is_scam"])

            scam_only_mask = labels_df["is_scam"] == 1
            scam_only_features = features_df.loc[scam_only_mask]
            scam_only_labels = labels_df.loc[scam_only_mask, "scam_type"]
            scam_only_labels = scam_only_labels[scam_only_labels.notna() & (scam_only_labels != "none")]
            scam_only_features = scam_only_features.loc[scam_only_labels.index]

            if not scam_only_features.empty:
                type_preprocessor = self._build_preprocessor()
                self.type_model = Pipeline(
                    steps=[
                        ("preprocessor", type_preprocessor),
                        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced")),
                    ]
                )
                self.type_model.fit(scam_only_features, scam_only_labels)

            logger.info(
                "Scam detector trained on %s payments (%s labeled scams).",
                self.training_samples,
                self.scam_samples,
            )
        except Exception:
            logger.exception("Scam detector model training failed. Falling back to rule-only detection.")
            self.binary_model = None
            self.type_model = None
            self.training_samples = 0
            self.scam_samples = 0

    def _build_preprocessor(self) -> ColumnTransformer:
        numeric_features = [
            "amount_abs",
            "amount_signed",
            "created_hour",
            "created_dayofweek",
            "description_length",
            "rule_score",
            "keyword_hit_count",
            "spoof_hit_count",
            "is_night",
            "is_weekend",
            "has_merchant_reference",
        ]
        categorical_features = [
            "currency",
            "payment_type",
            "counterparty_country",
            "direction",
            "counterparty_bank_code",
        ]
        return ColumnTransformer(
            transformers=[
                (
                    "num",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    numeric_features,
                ),
                (
                    "cat",
                    Pipeline(
                        steps=[
                            ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore")),
                        ]
                    ),
                    categorical_features,
                ),
                ("text", TfidfVectorizer(ngram_range=(1, 2), max_features=1500), "combined_text"),
            ]
        )

    def _load_training_frames(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        with TRAINING_DATASET_PATH.open("r", encoding="utf-8") as transactions_file:
            transaction_items = json.load(transactions_file).get("Response", [])

        with TRAINING_LABELS_PATH.open("r", encoding="utf-8") as labels_file:
            labels = json.load(labels_file)

        feature_rows: list[dict[str, Any]] = []
        label_rows: list[dict[str, Any]] = []

        for item in transaction_items:
            payment = item.get("Payment")
            if not payment:
                continue

            normalized = self._normalize_bunq_payment(payment)
            label = labels.get(str(payment.get("id")))
            if label is None:
                continue

            feature_rows.append(self._feature_row(normalized))
            label_rows.append(
                {
                    "is_scam": int(bool(label.get("is_scam"))),
                    "scam_type": label.get("scam_type") or "none",
                }
            )

        return pd.DataFrame(feature_rows), pd.DataFrame(label_rows)

    def evaluate_transaction(self, request: TransactionCheckRequest) -> ScamCheckResponse:
        normalized = self._normalize_request(request)
        return self._score_transaction(normalized)

    def evaluate_bunq_payment(self, request: BunqPaymentCheckRequest) -> ScamCheckResponse:
        normalized = self._normalize_bunq_payment(request.payment)
        return self._score_transaction(normalized)

    def _score_transaction(self, transaction: NormalizedTransaction) -> ScamCheckResponse:
        feature_row = self._feature_row(transaction)
        features_df = pd.DataFrame([feature_row])
        rule_assessment = self._assess_rules(transaction)

        model_probability = 0.0
        if self.binary_model is not None:
            positive_class_index = list(self.binary_model.classes_).index(1)
            model_probability = float(self.binary_model.predict_proba(features_df)[0][positive_class_index])

        risk_score = rule_assessment.score
        if self.binary_model is not None:
            risk_score = (0.65 * model_probability) + (0.35 * rule_assessment.score)

        if rule_assessment.score >= FORCE_SCAM_RULE_THRESHOLD:
            risk_score = max(risk_score, rule_assessment.score)

        risk_score = round(max(0.0, min(risk_score, 1.0)), 4)
        risk_level = self._risk_level(risk_score)
        is_scam = risk_score >= SCAM_THRESHOLD or rule_assessment.score >= FORCE_SCAM_RULE_THRESHOLD

        predicted_scam_type = None
        if is_scam or risk_score >= LOW_RISK_THRESHOLD:
            predicted_scam_type = self._predict_scam_type(features_df, rule_assessment.type_hint)

        reasons = rule_assessment.reasons[:]
        if not reasons:
            if risk_level == "low":
                reasons.append("No strong scam indicators were detected.")
            else:
                reasons.append("The model detected an elevated pattern risk without a dominant rule trigger.")

        return ScamCheckResponse(
            transaction_id=transaction.transaction_id,
            is_scam=is_scam,
            risk_score=risk_score,
            risk_level=risk_level,
            predicted_scam_type=predicted_scam_type,
            model_probability=round(model_probability, 4),
            rule_based_score=round(rule_assessment.score, 4),
            reasons=reasons[:5],
            engine=self.engine_name,
        )

    def _predict_scam_type(self, features_df: pd.DataFrame, rule_type_hint: str | None) -> str | None:
        if self.type_model is not None:
            try:
                return str(self.type_model.predict(features_df)[0])
            except Exception:
                logger.exception("Scam type prediction failed. Falling back to rules.")
        return rule_type_hint

    def _risk_level(self, risk_score: float) -> str:
        if risk_score >= HIGH_RISK_THRESHOLD:
            return "high"
        if risk_score >= LOW_RISK_THRESHOLD:
            return "medium"
        return "low"

    def _normalize_request(self, request: TransactionCheckRequest) -> NormalizedTransaction:
        direction = request.direction or self._infer_direction(request.amount)
        created_at = request.created_at
        counterparty_country = (request.counterparty_country or self._iban_country(request.counterparty_iban) or "unknown").upper()
        return NormalizedTransaction(
            transaction_id=request.transaction_id,
            amount=float(request.amount),
            currency=(request.currency or "EUR").upper(),
            description=(request.description or "").strip(),
            counterparty_name=(request.counterparty_name or "").strip(),
            counterparty_iban=(request.counterparty_iban or None),
            counterparty_country=counterparty_country,
            payment_type=(request.payment_type or "UNKNOWN").upper(),
            merchant_reference=request.merchant_reference,
            created_at=created_at,
            direction=direction,
        )

    def _normalize_bunq_payment(self, payment: dict[str, Any]) -> NormalizedTransaction:
        amount = payment.get("amount", {})
        counterparty_alias = payment.get("counterparty_alias", {})
        created_raw = payment.get("created")
        created_at = None
        if created_raw:
            try:
                created_at = datetime.fromisoformat(created_raw)
            except ValueError:
                logger.debug("Could not parse payment timestamp %s", created_raw)

        amount_value = float(amount.get("value", 0))
        iban = counterparty_alias.get("iban")
        country = (counterparty_alias.get("country") or self._iban_country(iban) or "unknown").upper()

        return NormalizedTransaction(
            transaction_id=str(payment.get("id")) if payment.get("id") is not None else None,
            amount=amount_value,
            currency=(amount.get("currency") or "EUR").upper(),
            description=str(payment.get("description") or "").strip(),
            counterparty_name=str(counterparty_alias.get("display_name") or "").strip(),
            counterparty_iban=iban,
            counterparty_country=country,
            payment_type=str(payment.get("type") or "UNKNOWN").upper(),
            merchant_reference=payment.get("merchant_reference"),
            created_at=created_at,
            direction=self._infer_direction(amount_value),
        )

    def _feature_row(self, transaction: NormalizedTransaction) -> dict[str, Any]:
        rule_assessment = self._assess_rules(transaction)
        created_hour = transaction.created_at.hour if transaction.created_at else 12
        created_dayofweek = transaction.created_at.weekday() if transaction.created_at else 0
        description = transaction.description.strip()
        counterparty_name = transaction.counterparty_name.strip()
        combined_text = " ".join(part for part in [description, counterparty_name] if part).lower()

        return {
            "amount_abs": abs(transaction.amount),
            "amount_signed": float(transaction.amount),
            "created_hour": created_hour,
            "created_dayofweek": created_dayofweek,
            "description_length": len(description),
            "currency": transaction.currency.upper(),
            "payment_type": transaction.payment_type.upper(),
            "counterparty_country": (transaction.counterparty_country or "unknown").upper(),
            "direction": transaction.direction,
            "counterparty_bank_code": self._extract_bank_code(transaction.counterparty_iban),
            "has_merchant_reference": int(bool(transaction.merchant_reference)),
            "rule_score": rule_assessment.score,
            "keyword_hit_count": rule_assessment.keyword_hits,
            "spoof_hit_count": rule_assessment.spoof_hits,
            "is_night": int(created_hour < 6 or created_hour >= 23),
            "is_weekend": int(created_dayofweek >= 5),
            "combined_text": combined_text,
        }

    def _assess_rules(self, transaction: NormalizedTransaction) -> RuleAssessment:
        description = transaction.description.lower()
        counterparty_name = transaction.counterparty_name.lower()
        combined_text = f"{description} {counterparty_name}".strip()

        matched_keywords = sorted(term for term in SUSPICIOUS_TERMS if term in combined_text)
        matched_spoof_terms = sorted(term for term in SPOOFED_ENTITY_TERMS if term in counterparty_name)

        reasons: list[str] = []
        score = 0.0

        if matched_keywords:
            score += min(0.12 + (0.05 * (len(matched_keywords) - 1)), 0.32)
            reasons.append(
                "Description contains suspicious wording: " + ", ".join(matched_keywords[:4]) + "."
            )

        if matched_spoof_terms:
            score += min(0.18 + (0.06 * (len(matched_spoof_terms) - 1)), 0.34)
            reasons.append(
                "Counterparty resembles a spoofed institution or support entity: "
                + ", ".join(matched_spoof_terms[:4])
                + "."
            )

        type_scores: dict[str, float] = defaultdict(float)
        for scam_type, terms in SCAM_TYPE_HINTS.items():
            matched_terms = [term for term in terms if term in combined_text]
            if matched_terms:
                type_scores[scam_type] = 0.14 + (0.05 * min(len(matched_terms), 3))

        if type_scores:
            strongest_type = max(type_scores, key=type_scores.get)
            score += type_scores[strongest_type]
        else:
            strongest_type = None

        amount_abs = abs(transaction.amount)
        if transaction.direction == "outgoing" and amount_abs >= 250:
            score += 0.08
            reasons.append("This is a relatively large outgoing transfer.")

        if 0 < amount_abs <= 5 and matched_keywords:
            score += 0.08
            reasons.append("A small verification-style transfer can be used as a scam test payment.")

        if transaction.created_at and transaction.direction == "outgoing":
            if transaction.created_at.hour < 6 or transaction.created_at.hour >= 23:
                score += 0.05
                reasons.append("The transfer happened outside typical banking hours.")

        if transaction.currency.upper() != "EUR":
            score += 0.03
            reasons.append("Cross-currency payments are slightly riskier in this detector.")

        if (
            transaction.counterparty_country
            and transaction.counterparty_country.upper() not in TRUSTED_COUNTRIES
            and (matched_keywords or matched_spoof_terms)
        ):
            score += 0.05
            reasons.append("The payment mixes suspicious wording with a less common counterparty country.")

        unique_reasons = []
        seen = set()
        for reason in reasons:
            if reason not in seen:
                unique_reasons.append(reason)
                seen.add(reason)

        return RuleAssessment(
            score=round(min(score, 0.99), 4),
            reasons=unique_reasons,
            type_hint=strongest_type,
            keyword_hits=len(matched_keywords),
            spoof_hits=len(matched_spoof_terms),
        )

    def _infer_direction(self, amount: float) -> str:
        if amount < 0:
            return "outgoing"
        if amount > 0:
            return "incoming"
        return "unknown"

    def _extract_bank_code(self, iban: str | None) -> str:
        if not iban:
            return "UNKNOWN"
        iban = iban.replace(" ", "").upper()
        if len(iban) >= 8 and iban[:2].isalpha():
            return iban[4:8]
        return "UNKNOWN"

    def _iban_country(self, iban: str | None) -> str | None:
        if not iban:
            return None
        iban = iban.replace(" ", "").upper()
        if len(iban) >= 2 and iban[:2].isalpha():
            return iban[:2]
        return None


@lru_cache(maxsize=1)
def get_scam_detector() -> ScamDetector:
    return ScamDetector()
