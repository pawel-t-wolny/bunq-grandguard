from fastapi import APIRouter

from app.schemas.scam_detection import (
    BatchScamCheckResponse,
    BatchTransactionCheckRequest,
    BunqPaymentCheckRequest,
    ScamCheckResponse,
    ScamDetectionHealthResponse,
    TransactionCheckRequest,
)
from app.services.scam_detector import get_scam_detector

router = APIRouter(prefix="/api/v1/scam", tags=["Scam Detection"])


@router.get("/health", response_model=ScamDetectionHealthResponse)
async def health() -> ScamDetectionHealthResponse:
    detector = get_scam_detector()
    return ScamDetectionHealthResponse(
        status="ok",
        engine=detector.engine_name,
        ml_model_ready=detector.binary_model is not None,
        training_samples=detector.training_samples,
        scam_samples=detector.scam_samples,
    )


@router.post("/check", response_model=bool)
async def check_transaction(request: TransactionCheckRequest) -> bool:
    detector = get_scam_detector()
    return detector.evaluate_transaction(request).is_scam


@router.post("/check/details", response_model=ScamCheckResponse)
async def check_transaction_details(request: TransactionCheckRequest) -> ScamCheckResponse:
    detector = get_scam_detector()
    return detector.evaluate_transaction(request)


@router.post("/check/bunq", response_model=bool)
async def check_bunq_payment(request: BunqPaymentCheckRequest) -> bool:
    detector = get_scam_detector()
    return detector.evaluate_bunq_payment(request).is_scam


@router.post("/check/bunq/details", response_model=ScamCheckResponse)
async def check_bunq_payment_details(request: BunqPaymentCheckRequest) -> ScamCheckResponse:
    detector = get_scam_detector()
    return detector.evaluate_bunq_payment(request)


@router.post("/check/batch", response_model=list[bool])
async def check_transaction_batch(request: BatchTransactionCheckRequest) -> list[bool]:
    detector = get_scam_detector()
    return [detector.evaluate_transaction(transaction).is_scam for transaction in request.transactions]


@router.post("/check/batch/details", response_model=BatchScamCheckResponse)
async def check_transaction_batch_details(request: BatchTransactionCheckRequest) -> BatchScamCheckResponse:
    detector = get_scam_detector()
    return BatchScamCheckResponse(
        results=[detector.evaluate_transaction(transaction) for transaction in request.transactions]
    )
