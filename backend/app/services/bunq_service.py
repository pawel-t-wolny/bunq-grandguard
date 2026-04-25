import logging
from typing import Dict, Any, Optional
import asyncio

from app.core.bunq_client import BunqClient 
from app.core.config import settings

logger = logging.getLogger(__name__)

# NOTE: Instantiating the client globally ensures it can reuse the context cache
# from bunq_context.json, avoiding the 1 request per 30 seconds rate limit on /session-server.
bunq_client = BunqClient(api_key=settings.BUNQ_API_KEY, sandbox=True)
bunq_client.authenticate()


async def get_primary_account() -> Optional[Dict[str, Any]]:
    """
    Retrieves the user's primary monetary account.
    """
    try:
        # Using asyncio.to_thread for synchronous requests inside bunq_client
        account_id = await asyncio.to_thread(bunq_client.get_primary_account_id)
        # Fetch full details if needed, or just return basic info
        accounts = await asyncio.to_thread(bunq_client.get, f"user/{bunq_client.user_id}/monetary-account-bank/{account_id}")
        return accounts[0] if accounts else None
    except Exception as e:
        logger.error(f"Error fetching monetary account: {e}")
        return None

async def make_payment(email: str, amount: str, description: str) -> Optional[Dict[str, Any]]:
    """
    Makes a payment to an email address.
    """
    try:
        payload = {
            "amount": { "value": amount, "currency": "EUR" },
            "counterparty_alias": { "type": "EMAIL", "value": email },
            "description": description
        }
        account_id = await asyncio.to_thread(bunq_client.get_primary_account_id)
        return await asyncio.to_thread(bunq_client.post, f"user/{bunq_client.user_id}/monetary-account/{account_id}/payment", payload)
    except Exception as e:
        logger.error(f"Error making payment: {e}")
        return None

async def create_payment_link(amount: str, description: str) -> Optional[Dict[str, Any]]:
    """
    Creates a bunq.me payment link.
    """
    try:
        payload = {
            "amount_requested": { "value": amount, "currency": "EUR" },
            "description": description
        }
        return await asyncio.to_thread(bunq_client.post, f"user/{bunq_client.user_id}/monetary-account-bank-payment-link", payload)

    except Exception as e:
        logger.error(f"Error creating payment link: {e}")
        return None
