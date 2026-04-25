import json
import random
import uuid
import string
import os
from datetime import datetime, timedelta


# -----------------------------
# Config
# -----------------------------

NUM_TRANSACTIONS = 5000
FRAUD_RATE = 0.05
OUTPUT_FILE = "transactions_dataset.json"
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


# -----------------------------
# Scam types
# -----------------------------

SCAM_TYPE_WEIGHTS = {
    "phishing": 0.22,
    "whatsapp_impersonation": 0.20,
    "fake_invoice": 0.20,
    "marketplace_scam": 0.18,
    "gift_card": 0.12,
    "investment_scam": 0.08,
}


# -----------------------------
# Helper data
# -----------------------------

BANK_CODES = ["BUNQ", "ABNA", "RABO", "INGB", "SNSB", "TRIO", "ASNB", "KNAB"]

PERSON_NAMES = [
    "A. Visser", "J. de Vries", "S. Bakker", "M. Jansen", "L. de Jong",
    "D. Smit", "T. Meijer", "R. Mulder", "E. Bos", "K. Vos",
    "N. Peters", "B. Willems", "F. Jacobs", "H. van Dijk", "P. Kramer",
    "A. Jansen", "M. de Vries", "J. Bakker", "S. van Leeuwen"
]

COMPANY_NAMES = [
    "Albert Heijn", "Jumbo", "Lidl", "Aldi", "Bol.com",
    "Coolblue", "MediaMarkt", "Netflix International B.V.", "Spotify",
    "NS Reizigers", "Shell", "KPN", "VodafoneZiggo", "Eneco",
    "Vattenfall", "Zilveren Kruis", "CZ Zorgverzekering", "DUO",
    "Belastingdienst", "CJIB", "Gemeente Amsterdam", "PostNL",
    "DHL Parcel", "Marktplaats", "Tikkie", "PayPal Europe",
    "Booking.com", "Airbnb Payments", "IKEA", "H&M", "Zara",
    "Apple Services", "Google Payments", "Steam", "Amazon EU"
]

SCAMMY_COUNTERPARTIES = [
    "Kluisrekening Nederland",
    "Veilige Rekening NL",
    "CJIB Incasso",
    "Belastingdienst Aanmaning",
    "Incassobureau Nederland",
    "PostNL Servicekosten",
    "DHL Bezorgen",
    "Netflix Update",
    "Bank Verificatie",
    "Crypto Invest Nederland",
    "Trading Platform Europe",
    "Giftcard Service",
    "Onbekend",
]

NORMAL_DESCRIPTIONS = [
    "Boodschappen",
    "Supermarkt",
    "Lunch",
    "Koffie",
    "Tikkie",
    "Tikkie eten",
    "Tikkie drankjes",
    "Restaurant",
    "Terras",
    "Bioscoop",
    "Parkeren",
    "Tankstation",
    "Netflix",
    "Spotify",
    "Telefoon abonnement",
    "Internet factuur",
    "Zorgverzekering",
    "Energie termijnbedrag",
    "Waternet",
    "Huur appartement",
    "Servicekosten",
    "Collegegeld",
    "DUO betaling",
    "Vakantie aanbetaling",
    "Hotel reservering",
    "Vliegtickets",
    "Borg kamer",
    "Meubels",
    "Laptop aankoop",
    "Fiets aankoop",
    "Auto reparatie",
    "Belasting betaling",
    "CJIB boete",
    "Gemeente heffing",
    "Betalingsherinnering",
    "Factuur direct betalen",
    "Achterstand zorgverzekering",
    "Laatste herinnering",
    "Verificatie betaling",
    "Account controle",
    "Pakket bezorgkosten",
    "Administratiekosten",
    "Dossier betaling",
]

SCAM_DESCRIPTIONS_BY_TYPE = {
    "phishing": [
        "Account controle",
        "Verificatie betaling",
        "Bank verificatie",
        "Veiligstellen tegoeden",
        "Kluisrekening verificatie",
        "Urgent blokkade opheffen",
        "Test betaling systeem",
        "Betaalverzoek",
    ],
    "whatsapp_impersonation": [
        "Voorschot",
        "Nieuwe telefoon",
        "Hoi mam nieuwe nummer",
        "Huur voorschot",
        "Tikkie dringend",
        "Betaalverzoek",
        "Tikkie eten",
        "Tikkie lunch",
    ],
    "fake_invoice": [
        "Factuur betaling",
        "Dossier betaling",
        "Dossier direct betalen",
        "Administratiekosten",
        "Achterstand betaling",
        "Laatste herinnering",
        "Incasso betaling",
        "Servicekosten",
    ],
    "marketplace_scam": [
        "Marktplaats betaling",
        "Fiets aankoop",
        "Telefoon betaling",
        "Laptop aankoop",
        "Aanbetaling tickets",
        "Borg kamer",
        "Voorschot",
        "Reservering",
    ],
    "gift_card": [
        "Giftcard",
        "Apple tegoed",
        "Google Play",
        "Steam kaart",
        "Bol.com cadeaukaart",
        "Tegoed aankoop",
        "Online voucher",
        "Digitale kaart",
    ],
    "investment_scam": [
        "Investering",
        "Crypto aankoop",
        "Trading account",
        "Beleggingsplatform",
        "Rendement storting",
        "Portfolio betaling",
        "Account funding",
        "Deposit trading",
    ],
}


# -----------------------------
# Helper functions
# -----------------------------

def weighted_choice(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]


def sample_scam_type():
    return weighted_choice(list(SCAM_TYPE_WEIGHTS.items()))


def generate_iban():
    bank = random.choice(BANK_CODES)
    account_num = "".join(random.choices(string.digits, k=10))
    return f"NL{random.randint(10, 99)}{bank}{account_num}"


def random_date(start_days_ago=365, is_fraud=False, scam_type="none"):
    now = datetime.now()

    # Fraud is slightly more likely at evening/night, but not deterministic.
    if is_fraud and scam_type in ["whatsapp_impersonation", "phishing", "investment_scam"]:
        hour_bucket = weighted_choice([
            ("night", 0.16),
            ("morning", 0.14),
            ("day", 0.32),
            ("evening", 0.38),
        ])
    else:
        hour_bucket = weighted_choice([
            ("night", 0.08),
            ("morning", 0.20),
            ("day", 0.42),
            ("evening", 0.30),
        ])

    if hour_bucket == "night":
        hour = random.choice([0, 1, 2, 3, 4, 5])
    elif hour_bucket == "morning":
        hour = random.randint(6, 11)
    elif hour_bucket == "day":
        hour = random.randint(12, 17)
    else:
        hour = random.randint(18, 23)

    random_dt = now - timedelta(days=random.randint(0, start_days_ago))
    random_dt = random_dt.replace(
        hour=hour,
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
        microsecond=random.randint(0, 999999),
    )

    return random_dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def generate_avatar_dict():
    return {
        "uuid": str(uuid.uuid4()),
        "image": [{
            "attachment_public_uuid": str(uuid.uuid4()),
            "height": random.choice([480, 1024]),
            "width": random.choice([480, 1024]),
            "content_type": "image/jpeg",
            "urls": [{
                "type": "ORIGINAL",
                "url": f"https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/{uuid.uuid4().hex}.jpg"
            }]
        }],
        "anchor_uuid": None,
        "style": "NONE"
    }


def generate_alias(name, iban, is_person=True):
    user_uuid = str(uuid.uuid4())

    first_public_name = name
    if is_person and " " in name:
        first_public_name = name.split(" ")[0]

    return {
        "iban": iban,
        "is_light": False,
        "display_name": name,
        "avatar": generate_avatar_dict(),
        "label_user": {
            "uuid": user_uuid,
            "display_name": name,
            "country": "NL",
            "avatar": generate_avatar_dict(),
            "public_nick_name": first_public_name,
            "type": "PERSON" if is_person else "COMPANY"
        },
        "country": "NL"
    }


def generate_amount(is_fraud, scam_type):
    """
    Amount distributions overlap heavily.

    Scam types have tendencies:
    - phishing: micro/small/medium
    - whatsapp: medium, person-like transfer
    - fake_invoice: medium/large
    - marketplace: small/medium
    - gift_card: round-ish medium amounts
    - investment: larger outgoing amounts

    But all patterns overlap with legitimate payments.
    """

    if not is_fraud:
        pattern = weighted_choice([
            ("small_daily", 0.43),
            ("medium_purchase", 0.20),
            ("large_legit", 0.12),
            ("very_large_legit", 0.04),
            ("micro", 0.04),
            ("round_medium", 0.04),
            ("income", 0.10),
            ("refund", 0.03),
        ])
    else:
        if scam_type == "phishing":
            pattern = weighted_choice([
                ("micro", 0.25),
                ("small_daily", 0.30),
                ("medium_purchase", 0.25),
                ("large_legit", 0.10),
                ("random_noise", 0.10),
            ])
        elif scam_type == "whatsapp_impersonation":
            pattern = weighted_choice([
                ("small_daily", 0.15),
                ("medium_purchase", 0.45),
                ("large_legit", 0.25),
                ("round_medium", 0.10),
                ("random_noise", 0.05),
            ])
        elif scam_type == "fake_invoice":
            pattern = weighted_choice([
                ("medium_purchase", 0.35),
                ("large_legit", 0.35),
                ("very_large_legit", 0.15),
                ("small_daily", 0.10),
                ("random_noise", 0.05),
            ])
        elif scam_type == "marketplace_scam":
            pattern = weighted_choice([
                ("small_daily", 0.25),
                ("medium_purchase", 0.45),
                ("large_legit", 0.15),
                ("round_medium", 0.10),
                ("random_noise", 0.05),
            ])
        elif scam_type == "gift_card":
            pattern = weighted_choice([
                ("round_medium", 0.55),
                ("medium_purchase", 0.25),
                ("small_daily", 0.10),
                ("large_legit", 0.05),
                ("random_noise", 0.05),
            ])
        elif scam_type == "investment_scam":
            pattern = weighted_choice([
                ("large_legit", 0.35),
                ("very_large_legit", 0.35),
                ("medium_purchase", 0.15),
                ("random_noise", 0.15),
            ])
        else:
            pattern = "random_noise"

    if pattern == "small_daily":
        amount = random.uniform(-60, -2)

    elif pattern == "medium_purchase":
        amount = random.uniform(-350, -60)

    elif pattern == "large_legit":
        amount = random.uniform(-1500, -350)

    elif pattern == "very_large_legit":
        amount = random.uniform(-5000, -1500)

    elif pattern == "micro":
        amount = random.uniform(-1.00, -0.01)

    elif pattern == "round_medium":
        base = random.choice([25, 50, 75, 100, 150, 200, 250, 300])
        amount = -base + random.uniform(-3, 3)

    elif pattern == "income":
        amount = random.uniform(500, 4500)

    elif pattern == "refund":
        amount = random.uniform(5, 500)

    else:
        amount = random.uniform(-2500, 1000)

    return round(amount, 2)


def generate_balance_after(amount, is_fraud=False, scam_type="none"):
    base_balance = weighted_choice([
        (random.uniform(20, 500), 0.20),
        (random.uniform(500, 2500), 0.45),
        (random.uniform(2500, 8000), 0.30),
        (random.uniform(8000, 20000), 0.05),
    ])

    # Some fraud happens when balance becomes low, but legitimate payments can too.
    low_balance_probability = 0.04
    if is_fraud and scam_type in ["fake_invoice", "investment_scam", "whatsapp_impersonation"]:
        low_balance_probability = 0.09

    if random.random() < low_balance_probability:
        base_balance = random.uniform(-500, 150)

    return round(base_balance, 2)


def generate_description(is_fraud, scam_type):
    """
    Text exists in the JSON for realism, but the model should not use it.

    Scam descriptions are not always obvious.
    Normal descriptions are sometimes suspicious-looking.
    """

    if not is_fraud:
        if random.random() < 0.15:
            desc = random.choice([
                "Betalingsherinnering",
                "Factuur direct betalen",
                "Achterstand betaling",
                "Verificatie betaling",
                "Pakket bezorgkosten",
                "Dossier betaling",
                "Administratiekosten",
                "Account controle",
            ])
        else:
            desc = random.choice(NORMAL_DESCRIPTIONS)
    else:
        if random.random() < 0.70:
            desc = random.choice(SCAM_DESCRIPTIONS_BY_TYPE[scam_type])
        else:
            desc = random.choice(NORMAL_DESCRIPTIONS)

    # Add optional reference numbers to both classes.
    if random.random() < 0.18:
        desc += f" {random.randint(10000, 999999)}"

    if random.random() < 0.10:
        desc += " " + random.choice([
            "INV",
            "REF",
            "ORD",
            "Dossier",
            "Kenmerk",
        ]) + str(random.randint(1000, 99999))

    return desc


def generate_counterparty(is_fraud, scam_type):
    """
    Scam types have tendencies, but counterparties overlap heavily.
    """

    if not is_fraud:
        source = weighted_choice([
            ("person", 0.35),
            ("company", 0.55),
            ("suspicious_benign", 0.10),
        ])
    else:
        if scam_type in ["whatsapp_impersonation", "marketplace_scam"]:
            source = weighted_choice([
                ("person", 0.65),
                ("company", 0.15),
                ("scammy", 0.20),
            ])
        elif scam_type in ["fake_invoice", "phishing"]:
            source = weighted_choice([
                ("person", 0.15),
                ("company", 0.45),
                ("scammy", 0.40),
            ])
        elif scam_type == "gift_card":
            source = weighted_choice([
                ("person", 0.10),
                ("company", 0.65),
                ("scammy", 0.25),
            ])
        elif scam_type == "investment_scam":
            source = weighted_choice([
                ("person", 0.10),
                ("company", 0.40),
                ("scammy", 0.50),
            ])
        else:
            source = weighted_choice([
                ("person", 0.40),
                ("company", 0.35),
                ("scammy", 0.25),
            ])

    if source == "person":
        name = random.choice(PERSON_NAMES)
        is_person = True

        if is_fraud and scam_type == "whatsapp_impersonation" and random.random() < 0.25:
            name = random.choice(PERSON_NAMES) + random.choice([" Nieuw", " Prive", " Mobiel", ""])

    elif source == "company":
        if is_fraud and scam_type == "gift_card":
            name = random.choice([
                "Apple Services",
                "Google Payments",
                "Steam",
                "Bol.com",
                "Amazon EU",
                "MediaMarkt",
                "Coolblue",
            ])
        elif is_fraud and scam_type == "investment_scam":
            name = random.choice([
                "Trading Platform Europe",
                "Crypto Invest Nederland",
                "PayPal Europe",
                "Bank Verificatie",
            ])
        else:
            name = random.choice(COMPANY_NAMES)

        is_person = False

    elif source == "suspicious_benign":
        name = random.choice([
            "Belastingdienst",
            "CJIB",
            "Gemeente Amsterdam",
            "PostNL",
            "DHL Parcel",
            "Incassobureau Nederland",
            "Zorgverzekering Achterstand",
            "Administratiekantoor",
        ])
        is_person = False

    else:
        name = random.choice(SCAMMY_COUNTERPARTIES)
        is_person = False

    return name, is_person


def generate_payment_type(is_fraud=False, scam_type="none"):
    if is_fraud and scam_type == "gift_card":
        return weighted_choice([
            ("BUNQ", 0.40),
            ("IDEAL", 0.25),
            ("MASTERCARD", 0.25),
            ("SEPA", 0.10),
        ])

    if is_fraud and scam_type == "investment_scam":
        return weighted_choice([
            ("BUNQ", 0.45),
            ("SEPA", 0.25),
            ("TRANSFERWISE", 0.20),
            ("IDEAL", 0.10),
        ])

    return weighted_choice([
        ("BUNQ", 0.70),
        ("IDEAL", 0.12),
        ("MASTERCARD", 0.08),
        ("TRANSFERWISE", 0.03),
        ("SEPA", 0.07),
    ])


def generate_sub_type(is_fraud=False, scam_type="none"):
    if is_fraud and scam_type in ["marketplace_scam", "whatsapp_impersonation"]:
        return weighted_choice([
            ("PAYMENT", 0.78),
            ("REQUEST", 0.14),
            ("IDEAL", 0.04),
            ("MASTERCARD", 0.04),
        ])

    if is_fraud and scam_type == "gift_card":
        return weighted_choice([
            ("PAYMENT", 0.55),
            ("IDEAL", 0.20),
            ("MASTERCARD", 0.25),
        ])

    return weighted_choice([
        ("PAYMENT", 0.88),
        ("REQUEST", 0.05),
        ("IDEAL", 0.04),
        ("MASTERCARD", 0.03),
    ])


def maybe_attachment(is_fraud=False, scam_type="none"):
    probability = 0.04

    if is_fraud and scam_type == "fake_invoice":
        probability = 0.18
    elif is_fraud and scam_type in ["phishing", "investment_scam"]:
        probability = 0.08

    if random.random() > probability:
        return []

    return [{
        "id": random.randint(100000, 999999),
        "description": random.choice(["factuur.pdf", "bon.pdf", "bewijs.pdf", "invoice.pdf"]),
        "attachment_public_uuid": str(uuid.uuid4()),
    }]


def generate_merchant_reference(is_fraud=False, scam_type="none"):
    probability = 0.20

    if is_fraud and scam_type in ["fake_invoice", "investment_scam", "gift_card"]:
        probability = 0.45

    if random.random() > probability:
        return None

    prefix = random.choice(["INV-", "ORD-", "REF-", "TRX-", "PAY-"])
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(6, 12)))
    return prefix + suffix


def generate_transaction(is_fraud=False, scam_type="none"):
    tx_id = random.randint(10000000, 99999999)

    created_at = random_date(is_fraud=is_fraud, scam_type=scam_type)
    amount = generate_amount(is_fraud, scam_type)
    desc = generate_description(is_fraud, scam_type)
    counterparty_name, counterparty_is_person = generate_counterparty(is_fraud, scam_type)
    balance = generate_balance_after(amount, is_fraud, scam_type)

    payment_type = generate_payment_type(is_fraud, scam_type)
    sub_type = generate_sub_type(is_fraud, scam_type)
    merchant_reference = generate_merchant_reference(is_fraud, scam_type)

    return {
        "Payment": {
            "id": tx_id,
            "created": created_at,
            "updated": created_at,
            "monetary_account_id": random.randint(1000000, 9999999),
            "amount": {
                "currency": "EUR",
                "value": f"{amount:.2f}"
            },
            "payment_fee": None,
            "description": desc,
            "type": payment_type,
            "merchant_reference": merchant_reference,
            "alias": generate_alias("Mijn Rekening", generate_iban(), True),
            "counterparty_alias": generate_alias(counterparty_name, generate_iban(), counterparty_is_person),
            "attachment": maybe_attachment(is_fraud, scam_type),
            "geolocation": None,
            "batch_id": None,
            "scheduled_id": None,
            "address_billing": None,
            "address_shipping": None,
            "sub_type": sub_type,
            "payment_arrival_expected": {
                "status": weighted_choice([
                    ("ARRIVED", 0.94),
                    ("PENDING", 0.04),
                    ("CANCELLED", 0.01),
                    ("REJECTED", 0.01),
                ]),
                "time": None
            },
            "request_reference_split_the_bill": [],
            "balance_after_mutation": {
                "currency": "EUR",
                "value": f"{balance:.2f}"
            },
            "payment_auto_allocate_instance": None,
            "payment_suspended_outgoing": None,

            # Training labels.
            # Never include these in model features.
            "_is_synthetic_fraud": is_fraud,
            "_synthetic_scam_type": scam_type,
        }
    }


def main():
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    print(f"Target fraud rate: {FRAUD_RATE * 100:.2f}%")

    dataset = []
    fraud_count = 0
    scam_type_counts = {scam_type: 0 for scam_type in SCAM_TYPE_WEIGHTS}
    scam_type_counts["none"] = 0

    for _ in range(NUM_TRANSACTIONS):
        is_fraud = random.random() < FRAUD_RATE

        if is_fraud:
            fraud_count += 1
            scam_type = sample_scam_type()
            scam_type_counts[scam_type] += 1
        else:
            scam_type = "none"
            scam_type_counts["none"] += 1

        dataset.append(generate_transaction(is_fraud, scam_type))

    final_output = {
        "Response": dataset
    }

    file_path = os.path.abspath(OUTPUT_FILE)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    print("Done.")
    print(f"Saved to: {file_path}")
    print(f"Legitimate transactions: {NUM_TRANSACTIONS - fraud_count}")
    print(f"Fraudulent transactions: {fraud_count}")
    print(f"Actual fraud rate: {fraud_count / NUM_TRANSACTIONS:.4f}")
    print()
    print("Scam type counts:")
    for key, value in sorted(scam_type_counts.items()):
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()