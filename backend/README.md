# bunq Hackathon FastAPI Framework

A production-ready but hackathon-fast FastAPI scaffolding for interacting with the [bunq API](https://doc.bunq.com/).
It now also exposes a scam-detection API that other applications can call to score transactions.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.12+
- A bunq [Sandbox API Key](https://doc.bunq.com/basics/sandbox)

### 2. Installation
```bash
# Install dependencies
python3 -m pip install -r requirements.txt
```

### 3. Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Fill in your `BUNQ_API_KEY` and `NGROK_URL` (for webhooks).

### 4. Running the App
```bash
# Start the development server
python3 -m uvicorn app.main:app --reload
```
The API will be available at [http://localhost:8000](http://localhost:8000).
Interactive docs (Swagger) are at [http://localhost:8000/docs](http://localhost:8000/docs).

## 🛠️ Project Structure
- `app/main.py`: FastAPI entry point & middleware setup.
- `app/core/bunq_client.py`: The lightweight bunq API wrapper (signs requests, handles session).
- `app/services/bunq_service.py`: High-level business logic for common bunq tasks.
- `app/routers/webhooks.py`: Real-time callback handler for mutations/s.

## ⚡ Key Features
- **Rate Limit Protection**: Automatically caches session context in `bunq_context.json` to avoid the 1 req / 30s session rate limit.
- **Async Ready**: Service layer uses `asyncio.to_thread` to ensure the synchronous bunq client doesn't block the FastAPI event loop.
- **Fast Webhooks**: Webhook callbacks are processed in the background, ensuring immediate `200 OK` responses to bunq.
- **Scam Detection API**: Classifies transactions with a hybrid detector that combines rule-based signals with a lightweight model trained from the bundled synthetic dataset.
- **VS Code Ready**: Includes `.vscode/launch.json` for easy debugging.

## Scam Detection Endpoints

### Single Transaction Check
`POST /api/v1/scam/check`

Example request:
```json
{
  "transaction_id": "txn_123",
  "amount": -249.99,
  "currency": "EUR",
  "description": "urgent account verification",
  "counterparty_name": "Bunq Verification",
  "counterparty_iban": "NL12BUNQ1234567890",
  "counterparty_country": "NL",
  "payment_type": "BUNQ",
  "created_at": "2026-04-25T21:17:00",
  "direction": "outgoing"
}
```

Example response:
```json
true
```

### Raw bunq Payment Check
`POST /api/v1/scam/check/bunq`

Send a raw bunq `Payment` object inside a `payment` field. This is useful if another service already receives bunq-style webhook payloads. This endpoint also returns only `true` or `false`.

### Batch Check
`POST /api/v1/scam/check/batch`

Send a `transactions` array with up to 100 items to score multiple transactions in one call. The response is a JSON array of booleans.

### Detailed Responses
- `POST /api/v1/scam/check/details`
- `POST /api/v1/scam/check/bunq/details`
- `POST /api/v1/scam/check/batch/details`

Use these endpoints only if you want the extra fields like `risk_score`, `predicted_scam_type`, and `reasons`.

### Health
`GET /api/v1/scam/health`

Returns whether the model trained successfully and how many bundled samples were used.

## 🔗 Useful Links
- [bunq Doc](https://doc.bunq.com/)
- [bunq Sandbox](https://public-api.sandbox.bunq.com)
