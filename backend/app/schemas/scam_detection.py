from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCheckRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "txn_123",
                "amount": -249.99,
                "currency": "EUR",
                "description": "urgent account verification",
                "counterparty_name": "Bunq Verification",
                "counterparty_iban": "NL12BUNQ1234567890",
                "counterparty_country": "NL",
                "payment_type": "BUNQ",
                "merchant_reference": None,
                "created_at": "2026-04-25T21:17:00",
                "direction": "outgoing",
            }
        }
    )

    transaction_id: str | None = Field(default=None, description="Optional transaction id from the caller.")
    amount: float = Field(..., description="Signed amount. Negative usually means outgoing, positive incoming.")
    currency: str = Field(default="EUR", description="ISO 4217 currency code.")
    description: str = Field(default="", description="Transaction description or payment reference.")
    counterparty_name: str = Field(default="", description="Display name of the counterparty.")
    counterparty_iban: str | None = Field(default=None, description="Optional counterparty IBAN.")
    counterparty_country: str | None = Field(default=None, description="Optional ISO country code.")
    payment_type: str = Field(default="BUNQ", description="Bunq payment type or external payment channel.")
    merchant_reference: str | None = Field(default=None, description="Merchant reference when available.")
    created_at: datetime | None = Field(default=None, description="Timestamp of the payment.")
    direction: Literal["incoming", "outgoing", "unknown"] | None = Field(
        default=None,
        description="Optional explicit direction. If omitted, it is inferred from the amount sign.",
    )


class BunqPaymentCheckRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment": {
                    "id": 26174613,
                    "created": "2025-01-01 11:26:10.793853",
                    "amount": {"currency": "EUR", "value": "-28.21"},
                    "description": "shared payment",
                    "type": "BUNQ",
                    "merchant_reference": None,
                    "counterparty_alias": {
                        "iban": "NL72INGB1448361685",
                        "display_name": "Tikkie",
                        "country": "NL",
                    },
                }
            }
        }
    )

    payment: dict[str, Any] = Field(..., description="Raw bunq Payment object.")


class BatchTransactionCheckRequest(BaseModel):
    transactions: list[TransactionCheckRequest] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Up to 100 transactions in a single batch request.",
    )


class ScamCheckResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    transaction_id: str | None = None
    is_scam: bool
    risk_score: float = Field(..., ge=0.0, le=1.0)
    risk_level: Literal["low", "medium", "high"]
    predicted_scam_type: str | None = None
    model_probability: float = Field(..., ge=0.0, le=1.0)
    rule_based_score: float = Field(..., ge=0.0, le=1.0)
    reasons: list[str]
    engine: str


class BatchScamCheckResponse(BaseModel):
    results: list[ScamCheckResponse]


class ScamDetectionHealthResponse(BaseModel):
    status: Literal["ok"]
    engine: str
    ml_model_ready: bool
    training_samples: int
    scam_samples: int
