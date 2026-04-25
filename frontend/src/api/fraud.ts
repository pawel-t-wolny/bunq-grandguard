export interface ScamCheckResponse {
  is_scam: boolean;
}

export const FRAUD_API_URL = process.env.EXPO_PUBLIC_FRAUD_API_URL ?? '';

export function buildSketchyNigerianPrincePayment() {
  return {
    id: 66324902,
    created: '2025-08-16 21:56:24.368292',
    updated: '2025-08-16 21:56:24.368292',
    monetary_account_id: 9098979,
    amount: { currency: 'EUR', value: '-320.59' },
    payment_fee: null,
    description: 'Huur voorschot 87289',
    type: 'MASTERCARD',
    merchant_reference: null,
    alias: {
      iban: 'NL79BUNQ4664039459',
      is_light: false,
      display_name: 'Mijn Rekening',
      avatar: {
        uuid: '87358334-bb8f-435f-9d82-65fd8cfb0ee5',
        image: [
          {
            attachment_public_uuid: 'f696e0ff-89db-457e-8b33-86cb2af2bb37',
            height: 1024,
            width: 1024,
            content_type: 'image/jpeg',
            urls: [
              {
                type: 'ORIGINAL',
                url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/42c98902493640629d0d0b7ece50791a.jpg',
              },
            ],
          },
        ],
        anchor_uuid: null,
        style: 'NONE',
      },
      label_user: {
        uuid: '6c5c209a-bc39-48e7-85cf-55f0b30fcfd5',
        display_name: 'Mijn Rekening',
        country: 'NL',
        avatar: {
          uuid: 'e616dfb0-cd84-4226-8479-b4429186d944',
          image: [
            {
              attachment_public_uuid: '1d2ea332-3e62-428e-9733-0a0dd29d5397',
              height: 1024,
              width: 480,
              content_type: 'image/jpeg',
              urls: [
                {
                  type: 'ORIGINAL',
                  url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/574a8c0503424367982cd0f85617ea25.jpg',
                },
              ],
            },
          ],
          anchor_uuid: null,
          style: 'NONE',
        },
        public_nick_name: 'Mijn',
        type: 'PERSON',
      },
      country: 'NL',
    },
    counterparty_alias: {
      iban: 'NL13ABNA0581342661',
      is_light: false,
      display_name: 'A. Visser',
      avatar: {
        uuid: 'e5309e24-6903-4f24-b7a3-a315a43a2eb0',
        image: [
          {
            attachment_public_uuid: '9999a6ad-1e4a-45d0-b6ba-cfef284d45f9',
            height: 480,
            width: 480,
            content_type: 'image/jpeg',
            urls: [
              {
                type: 'ORIGINAL',
                url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/9bdfab00f23f42e3a727e52d8c63482a.jpg',
              },
            ],
          },
        ],
        anchor_uuid: null,
        style: 'NONE',
      },
      label_user: {
        uuid: '2c5fd532-daa9-44f7-93f9-e4e690772fb9',
        display_name: 'A. Visser',
        country: 'NL',
        avatar: {
          uuid: 'ae20c615-c0aa-414f-a6f5-a4cf17deccb2',
          image: [
            {
              attachment_public_uuid: 'b88445e6-f490-4c76-899e-2a905d11c2ae',
              height: 1024,
              width: 480,
              content_type: 'image/jpeg',
              urls: [
                {
                  type: 'ORIGINAL',
                  url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/d4c9b76006184115abebab7e8e59fd5c.jpg',
                },
              ],
            },
          ],
          anchor_uuid: null,
          style: 'NONE',
        },
        public_nick_name: 'A.',
        type: 'PERSON',
      },
      country: 'NL',
    },
    attachment: [],
    geolocation: null,
    batch_id: null,
    scheduled_id: null,
    address_billing: null,
    address_shipping: null,
    sub_type: 'PAYMENT',
    payment_arrival_expected: { status: 'ARRIVED', time: null },
    request_reference_split_the_bill: [],
    balance_after_mutation: { currency: 'EUR', value: '3435.58' },
    payment_auto_allocate_instance: null,
    payment_suspended_outgoing: null,
  };
}

export function buildLegitPayment() {
  return {
    id: 66324903,
    created: '2025-08-16 21:58:12.917503',
    updated: '2025-08-16 21:58:12.917503',
    monetary_account_id: 9098979,
    amount: { currency: 'EUR', value: '-42.50' },
    payment_fee: null,
    description: 'Pizza vrijdag',
    type: 'BUNQ',
    merchant_reference: null,
    alias: {
      iban: 'NL79BUNQ4664039459',
      is_light: false,
      display_name: 'Mijn Rekening',
      avatar: {
        uuid: '87358334-bb8f-435f-9d82-65fd8cfb0ee5',
        image: [
          {
            attachment_public_uuid: 'f696e0ff-89db-457e-8b33-86cb2af2bb37',
            height: 1024,
            width: 1024,
            content_type: 'image/jpeg',
            urls: [
              {
                type: 'ORIGINAL',
                url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/42c98902493640629d0d0b7ece50791a.jpg',
              },
            ],
          },
        ],
        anchor_uuid: null,
        style: 'NONE',
      },
      label_user: {
        uuid: '6c5c209a-bc39-48e7-85cf-55f0b30fcfd5',
        display_name: 'Mijn Rekening',
        country: 'NL',
        avatar: {
          uuid: 'e616dfb0-cd84-4226-8479-b4429186d944',
          image: [
            {
              attachment_public_uuid: '1d2ea332-3e62-428e-9733-0a0dd29d5397',
              height: 1024,
              width: 480,
              content_type: 'image/jpeg',
              urls: [
                {
                  type: 'ORIGINAL',
                  url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/574a8c0503424367982cd0f85617ea25.jpg',
                },
              ],
            },
          ],
          anchor_uuid: null,
          style: 'NONE',
        },
        public_nick_name: 'Mijn',
        type: 'PERSON',
      },
      country: 'NL',
    },
    counterparty_alias: {
      iban: 'NL42INGB0005432109',
      is_light: false,
      display_name: 'Emma Bakker',
      avatar: {
        uuid: 'a1b2c3d4-e5f6-4708-9a0b-1c2d3e4f5061',
        image: [
          {
            attachment_public_uuid: 'b2c3d4e5-f607-4819-a0b1-c2d3e4f50617',
            height: 480,
            width: 480,
            content_type: 'image/jpeg',
            urls: [
              {
                type: 'ORIGINAL',
                url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/emma-bakker.jpg',
              },
            ],
          },
        ],
        anchor_uuid: null,
        style: 'NONE',
      },
      label_user: {
        uuid: 'c3d4e5f6-0718-492a-b0c1-d2e3f405162a',
        display_name: 'Emma Bakker',
        country: 'NL',
        avatar: {
          uuid: 'd4e5f607-1829-4a3b-c1d2-e3f405162a3b',
          image: [
            {
              attachment_public_uuid: 'e5f60718-293a-4b4c-d2e3-f405162a3b4c',
              height: 480,
              width: 480,
              content_type: 'image/jpeg',
              urls: [
                {
                  type: 'ORIGINAL',
                  url: 'https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/emma-bakker-thumb.jpg',
                },
              ],
            },
          ],
          anchor_uuid: null,
          style: 'NONE',
        },
        public_nick_name: 'Emma',
        type: 'PERSON',
      },
      country: 'NL',
    },
    attachment: [],
    geolocation: null,
    batch_id: null,
    scheduled_id: null,
    address_billing: null,
    address_shipping: null,
    sub_type: 'PAYMENT',
    payment_arrival_expected: { status: 'ARRIVED', time: null },
    request_reference_split_the_bill: [],
    balance_after_mutation: { currency: 'EUR', value: '3157.92' },
    payment_auto_allocate_instance: null,
    payment_suspended_outgoing: null,
  };
}

async function postForScamCheck(body: unknown): Promise<ScamCheckResponse> {
  const res = await fetch(FRAUD_API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`Fraud API responded with HTTP ${res.status}`);
  }

  const data = (await res.json()) as Partial<ScamCheckResponse>;
  if (typeof data?.is_scam !== 'boolean') {
    throw new Error('Fraud API response missing boolean "is_scam"');
  }

  return { is_scam: data.is_scam };
}

export async function checkPaymentForScam(): Promise<ScamCheckResponse> {
  if (!FRAUD_API_URL) {
    console.warn(
      '[fraud-api] EXPO_PUBLIC_FRAUD_API_URL is not set — defaulting to is_scam=true. ' +
        'Set the env var in .env to call the real endpoint.',
    );
    return { is_scam: true };
  }
  return postForScamCheck(buildSketchyNigerianPrincePayment());
}

export async function checkLegitPaymentForScam(): Promise<ScamCheckResponse> {
  if (!FRAUD_API_URL) {
    console.warn(
      '[fraud-api] EXPO_PUBLIC_FRAUD_API_URL is not set — defaulting to is_scam=false for legit demo. ' +
        'Set the env var in .env to call the real endpoint.',
    );
    return { is_scam: false };
  }
  return postForScamCheck(buildLegitPayment());
}
