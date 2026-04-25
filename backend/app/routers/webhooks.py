from fastapi import APIRouter, Request, BackgroundTasks
import logging
import json

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/callback", status_code=200)
async def bunq_webhook_callback(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint to receive bunq real-time callbacks (mutations/payments).
    """
    # Using background_tasks allows the endpoint to return 200 OK immediately,
    # preventing timeout issues while you process the potentially large JSON payload.
    try:
        payload = await request.json()
        logger.info(f"Incoming bunq webhook notification received!")
        
        # Dispatch to a processing function in the background
        background_tasks.add_task(process_webhook_payload, payload)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Failed to read webhook payload: {e}")
        return {"status": "error", "message": "Invalid JSON"}

def process_webhook_payload(payload: dict):
    # Safely print or log the incoming JSON payload
    print("--- BUNQ WEBHOOK PAYLOAD ---")
    print(json.dumps(payload, indent=2))
    print("----------------------------")
