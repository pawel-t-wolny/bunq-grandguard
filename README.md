# bunq Anti-Scam

A fraud detection system for bunq that combines a **XGBoost-based ML model** with an AI voice agent to protect elderly customers from scams. Built for the bunq Hackathon.

## Overview

When a suspicious transaction is detected, the system:
1. **Frontend sends transaction** to FastAPI backend for scam detection
2. **Backend returns is_scam=true** if the XGBoost model flags it
3. **Frontend directly calls ElevenLabs** to launch the AI voice agent
4. **Agent converses with the customer**, explains the risk, and helps prevent the scam

The frontend demonstrates a realistic scam scenario where an elderly user is targeted by "Microsoft Tech Support" attempting to steal €10,000.

---

## Architecture

```
                    ┌──────────────────┐
                    │   ElevenLabs     │
                    │   Voice Agent    │
                    │   (AI Agent)     │
                    └────────▲─────────┘
                             │
┌─────────────────┐          │
│  React Native   │──────────┼──────────▶┌──────────────────┐
│  Mobile App     │          │           │   FastAPI        │
│  (Expo)         │──────────┘           │   Backend        │
└─────────────────┘                      │   + XGBoost      │
                                         └──────────────────┘
```

**Flow:**
1. Frontend sends transaction to **FastAPI** for scam detection
2. If scam detected, frontend directly calls **ElevenLabs** to launch voice agent

**Backend** (FastAPI + Python)
- XGBoost binary classification model (pre-trained)
- Quantitative feature engineering (amounts, timing, balance ratios)
- No text/description analysis (purely numerical approach)

**Frontend** (React Native + Expo)
- Multi-screen demo flow
- Real-time fraud checking
- Voice agent trigger

---

## Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **npm or yarn**

---

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source ./.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server (using the XGBoost API)
uvicorn api:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000)

**Note**: The XGBoost models are pre-trained and included in the repo. No training required.

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file with the backend URL
echo "EXPO_PUBLIC_FRAUD_API_URL=http://localhost:8000/predict" > .env
```

Start the development server:
```bash
npm start
```

We recommend using Expo Go app on mobile.

---

### 3. ElevenLabs Setup

The AI voice agent is configured in the **ElevenLabs web interface**, not in code. You need to:

1. **Create an Agent** in ElevenLabs
   - Define the agent's personality and instructions for handling scam scenarios
   - Set up conversation rules for interacting with elderly customers
   - Configure tools/knowledge base if needed

2. **Configure the Voice**
   - Select or create a clear, friendly voice appropriate for elderly users
   - Test pronunciation and tone

3. **Set up Twilio for Phone Calls**
   - Create a [Twilio](https://www.twilio.com/) account
   - Purchase a phone number or use a trial number
   - In the ElevenLabs Agent settings, connect your Twilio account and your number

4. **Connect the Agent**
   - The frontend triggers the agent when a scam is detected
   - See [`frontend/src/api/elevenlabs.ts`](frontend/src/api/elevenlabs.ts) for the integration point

> **Note**: The demo works without ElevenLabs/Twilio credentials. The app defaults to a mock mode if API keys are not provided.

## How the XGBoost Model Works

The detection engine ([`backend/api.py`](backend/api.py)) uses a **quantitative-only approach**:

### Features Used

**Numeric Features:**
- Transaction amount (absolute and signed)
- Balance after transaction
- Amount-to-balance ratio
- Time features (hour, day of week, month, weekend, night)
- Direction indicators (outgoing/incoming)
- Attachment count
- Merchant reference flag

**Categorical Features:**
- Payment type (BUNQ, MASTERCARD, etc.)
- Sub-type
- Currency
- Counterparty country
- Counterparty user type
- Bank codes (extracted from IBAN)

## Notes

- The models are trained on synthetic data based on the included in the repo
- No bunq API key is required for the demo (mock data works)
- ElevenLabs integration is optional for the demo flow
- The `app/` directory contains an older implementation using Logistic Regression and is not used in production
