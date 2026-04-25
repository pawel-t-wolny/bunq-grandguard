const API_KEY = process.env.EXPO_PUBLIC_ELEVENLABS_API_KEY ?? '';
const AGENT_ID = process.env.EXPO_PUBLIC_ELEVENLABS_AGENT_ID ?? '';
const PHONE_NUMBER_ID =
  process.env.EXPO_PUBLIC_ELEVENLABS_PHONE_NUMBER_ID ?? '';

const TO_NUMBER = '+48780012803';
const ENDPOINT = 'https://api.elevenlabs.io/v1/convai/twilio/outbound-call';

const MERCHANT_NAME = 'Microsoft Tech Support';
const MERCHANT_COUNTRY = 'United States';
const TRANSACTION_DESCRIPTION = 'Microsoft Security Subscription Renewal';
const TRANSACTION_AMOUNT = '10000';

function formatTransactionDate(d: Date): string {
  return d.toLocaleString('en-GB', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  });
}

function buildDynamicVariables() {
  return {
    transaction_date: formatTransactionDate(new Date()),
    transaction_amount: TRANSACTION_AMOUNT,
    transaction_description: TRANSACTION_DESCRIPTION,
    merchant_name: MERCHANT_NAME,
    merchant_country: MERCHANT_COUNTRY,
    transfer_amount: TRANSACTION_AMOUNT,
    transfer_recipient: MERCHANT_NAME,
  };
}

export function triggerFraudSpecialistCall(): void {
  if (!API_KEY || !AGENT_ID || !PHONE_NUMBER_ID) {
    console.warn(
      '[elevenlabs] Missing env vars — skipping fraud-specialist call. Set ' +
        'EXPO_PUBLIC_ELEVENLABS_API_KEY, EXPO_PUBLIC_ELEVENLABS_AGENT_ID, and ' +
        'EXPO_PUBLIC_ELEVENLABS_PHONE_NUMBER_ID in .env.',
    );
    return;
  }

  fetch(ENDPOINT, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': API_KEY,
    },
    body: JSON.stringify({
      agent_id: AGENT_ID,
      agent_phone_number_id: PHONE_NUMBER_ID,
      to_number: TO_NUMBER,
      conversation_initiation_client_data: {
        dynamic_variables: buildDynamicVariables(),
      },
    }),
  })
    .then(async res => {
      if (!res.ok) {
        const text = await res.text().catch(() => '');
        console.warn(
          `[elevenlabs] Fraud call request failed: HTTP ${res.status} ${text}`,
        );
        return;
      }
      const data = await res.json().catch(() => null);
      console.log('[elevenlabs] Fraud call queued:', data);
    })
    .catch(err => {
      console.warn('[elevenlabs] Fraud call network error:', err);
    });
}
