import json
import random
import uuid
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta


# -----------------------------
# Config
# -----------------------------

N_TRANSACTIONS = 1000

OUTPUT_FILE = "bunq_synthetic_transactions.json"
LABELS_OUTPUT_FILE = "bunq_synthetic_transaction_labels.json"

RANDOM_SEED = 42

START_DATE = datetime(2025, 1, 1, 8, 0, 0)
END_DATE = datetime(2026, 4, 25, 23, 59, 59)

USER_NAME = "A. Visser"
USER_IBAN = "NL51BUNQ2093937468"
USER_COUNTRY = "NL"
MONETARY_ACCOUNT_ID = 2428053

SCAM_RATE = 0.08


random.seed(RANDOM_SEED)


# -----------------------------
# Helpers
# -----------------------------

def money(value: Decimal | float | int | str) -> str:
    value = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{value:.2f}"


def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    micros = random.randint(0, 999999)
    return start + timedelta(seconds=seconds, microseconds=micros)


def bunq_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def random_iban(country: str = "NL") -> str:
    if country == "NL":
        bank = random.choice(["BUNQ", "INGB", "RABO", "ABNA", "TRIO"])
        number = "".join(random.choices("0123456789", k=10))
        return f"NL{random.randint(10, 99)}{bank}{number}"

    if country == "DE":
        return "DE" + "".join(random.choices("0123456789", k=20))

    if country == "BE":
        return "BE" + "".join(random.choices("0123456789", k=14))

    if country == "FR":
        return "FR" + "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=25))

    if country == "ES":
        return "ES" + "".join(random.choices("0123456789", k=22))

    if country == "LT":
        return "LT" + "".join(random.choices("0123456789", k=18))

    if country == "EE":
        return "EE" + "".join(random.choices("0123456789", k=18))

    if country == "RO":
        return "RO" + "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=22))

    return country + "".join(random.choices("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20))


def random_currency(is_scam: bool) -> str:
    if is_scam:
        return random.choices(
            ["EUR", "USD", "GBP", "CHF"],
            weights=[92, 4, 3, 1],
            k=1,
        )[0]

    return random.choices(
        ["EUR", "USD", "GBP", "CHF"],
        weights=[98, 1, 0.7, 0.3],
        k=1,
    )[0]


def weighted_choice(items):
    values, weights = zip(*items)
    return random.choices(values, weights=weights, k=1)[0]


# -----------------------------
# Synthetic counterparties
# -----------------------------

NORMAL_COUNTERPARTIES = [
    {
        "name": "Albert Heijn",
        "country": "NL",
        "descriptions": ["groceries", "boodschappen", "AH winkel", "supermarket"],
        "amount_range": (Decimal("-85.00"), Decimal("-4.00")),
        "weight": 14,
    },
    {
        "name": "Jumbo",
        "country": "NL",
        "descriptions": ["groceries", "jumbo", "boodschappen"],
        "amount_range": (Decimal("-80.00"), Decimal("-3.50")),
        "weight": 10,
    },
    {
        "name": "NS Groep",
        "country": "NL",
        "descriptions": ["train ticket", "NS reis", "ov betaling"],
        "amount_range": (Decimal("-45.00"), Decimal("-2.80")),
        "weight": 8,
    },
    {
        "name": "Spotify",
        "country": "NL",
        "descriptions": ["spotify premium", "monthly subscription"],
        "amount_range": (Decimal("-13.99"), Decimal("-9.99")),
        "weight": 4,
    },
    {
        "name": "Netflix",
        "country": "NL",
        "descriptions": ["netflix subscription", "monthly subscription"],
        "amount_range": (Decimal("-18.99"), Decimal("-7.99")),
        "weight": 3,
    },
    {
        "name": "Bol.com",
        "country": "NL",
        "descriptions": ["online order", "bol.com bestelling", "webshop"],
        "amount_range": (Decimal("-250.00"), Decimal("-8.00")),
        "weight": 7,
    },
    {
        "name": "Tikkie",
        "country": "NL",
        "descriptions": ["tikkie", "dinner split", "drinks", "shared payment"],
        "amount_range": (Decimal("-60.00"), Decimal("-2.00")),
        "weight": 10,
    },
    {
        "name": "Gemeente Amsterdam",
        "country": "NL",
        "descriptions": ["municipal tax", "gemeente betaling", "parking permit"],
        "amount_range": (Decimal("-350.00"), Decimal("-20.00")),
        "weight": 2,
    },
    {
        "name": "DUO",
        "country": "NL",
        "descriptions": ["student finance", "duo payment"],
        "amount_range": (Decimal("250.00"), Decimal("1200.00")),
        "weight": 2,
    },
    {
        "name": "Salary Employer BV",
        "country": "NL",
        "descriptions": ["salary", "salaris", "monthly wage"],
        "amount_range": (Decimal("1500.00"), Decimal("4500.00")),
        "weight": 3,
    },
    {
        "name": "Landlord",
        "country": "NL",
        "descriptions": ["rent", "huur april", "monthly rent"],
        "amount_range": (Decimal("-1600.00"), Decimal("-550.00")),
        "weight": 3,
    },
    {
        "name": "VodafoneZiggo",
        "country": "NL",
        "descriptions": ["phone bill", "internet subscription", "monthly invoice"],
        "amount_range": (Decimal("-95.00"), Decimal("-15.00")),
        "weight": 4,
    },
    {
        "name": "Booking.com",
        "country": "NL",
        "descriptions": ["hotel booking", "travel", "reservation"],
        "amount_range": (Decimal("-900.00"), Decimal("-50.00")),
        "weight": 2,
    },
    {
        "name": "Deutsche Bahn",
        "country": "DE",
        "descriptions": ["train ticket", "travel booking", "DB ticket"],
        "amount_range": (Decimal("-180.00"), Decimal("-15.00")),
        "weight": 2,
    },
]

SCAM_COUNTERPARTIES = [
    {
        "name": "Bunq Verification",
        "country": "NL",
        "descriptions": [
            "urgent account verification",
            "security verification",
            "verify account now",
            "bunq safety check",
        ],
        "amount_range": (Decimal("-3000.00"), Decimal("-25.00")),
        "scam_type": "bank_impersonation",
        "weight": 8,
    },
    {
        "name": "Safe Account NL",
        "country": "NL",
        "descriptions": [
            "safe account transfer",
            "temporary security transfer",
            "fraud prevention transfer",
        ],
        "amount_range": (Decimal("-8000.00"), Decimal("-250.00")),
        "scam_type": "safe_account",
        "weight": 6,
    },
    {
        "name": "Crypto Investment Support",
        "country": "LT",
        "descriptions": [
            "crypto investment",
            "wallet activation fee",
            "trading account topup",
            "investment release payment",
        ],
        "amount_range": (Decimal("-5000.00"), Decimal("-100.00")),
        "scam_type": "investment",
        "weight": 5,
    },
    {
        "name": "Tax Refund Office",
        "country": "NL",
        "descriptions": [
            "tax refund processing",
            "refund release fee",
            "belastingdienst verificatie",
        ],
        "amount_range": (Decimal("-750.00"), Decimal("-10.00")),
        "scam_type": "government_impersonation",
        "weight": 5,
    },
    {
        "name": "Parcel Customs Service",
        "country": "BE",
        "descriptions": [
            "customs release fee",
            "package delivery fee",
            "parcel verification",
        ],
        "amount_range": (Decimal("-80.00"), Decimal("-1.00")),
        "scam_type": "delivery_fee",
        "weight": 7,
    },
    {
        "name": "Unknown Beneficiary",
        "country": "RO",
        "descriptions": [
            "urgent payment",
            "family emergency",
            "temporary loan",
            "release payment",
        ],
        "amount_range": (Decimal("-2500.00"), Decimal("-50.00")),
        "scam_type": "social_engineering",
        "weight": 4,
    },
]

LEGITIMATE_EDGE_CASES = [
    {
        "name": "Foreign Hotel GmbH",
        "country": "DE",
        "descriptions": ["hotel booking", "conference stay", "travel expense"],
        "amount_range": (Decimal("-1200.00"), Decimal("-150.00")),
        "weight": 2,
    },
    {
        "name": "Used Car Deposit",
        "country": "NL",
        "descriptions": ["car deposit", "vehicle down payment"],
        "amount_range": (Decimal("-5000.00"), Decimal("-1000.00")),
        "weight": 1,
    },
    {
        "name": "University Tuition",
        "country": "NL",
        "descriptions": ["tuition fee", "collegegeld", "semester payment"],
        "amount_range": (Decimal("-2500.00"), Decimal("-500.00")),
        "weight": 1,
    },
]


# -----------------------------
# Bunq-like structure
# -----------------------------

def avatar_stub(anchor_uuid=None):
    return {
        "uuid": str(uuid.uuid4()),
        "image": [
            {
                "attachment_public_uuid": str(uuid.uuid4()),
                "height": random.choice([126, 200, 480, 1023, 1024]),
                "width": random.choice([126, 200, 480, 1023, 1024]),
                "content_type": random.choice(["image/jpeg", "image/png"]),
                "urls": [
                    {
                        "type": "ORIGINAL",
                        "url": "https://example.com/synthetic-avatar.png",
                    }
                ],
            }
        ],
        "anchor_uuid": anchor_uuid,
        "style": "NONE",
    }


def make_alias(display_name: str, iban: str, country: str, label_type: str = "PERSON"):
    label_uuid = str(uuid.uuid4())

    return {
        "iban": iban,
        "is_light": False,
        "display_name": display_name,
        "avatar": avatar_stub(),
        "label_user": {
            "uuid": label_uuid,
            "display_name": display_name,
            "country": country,
            "avatar": avatar_stub(anchor_uuid=label_uuid),
            "public_nick_name": display_name,
            "type": label_type,
        },
        "country": country,
    }


def random_amount(min_value: Decimal, max_value: Decimal, scam: bool = False) -> Decimal:
    lo = min(min_value, max_value)
    hi = max(min_value, max_value)

    if scam and random.random() < 0.45:
        round_candidates = [
            Decimal("-10.00"),
            Decimal("-25.00"),
            Decimal("-50.00"),
            Decimal("-100.00"),
            Decimal("-250.00"),
            Decimal("-500.00"),
            Decimal("-1000.00"),
            Decimal("-2500.00"),
            Decimal("-5000.00"),
        ]
        valid = [x for x in round_candidates if lo <= x <= hi]
        if valid:
            return random.choice(valid)

    cents = random.randint(int(lo * 100), int(hi * 100))
    return Decimal(cents) / Decimal("100")


def choose_transaction_profile(is_scam: bool):
    if is_scam:
        return weighted_choice([(p, p["weight"]) for p in SCAM_COUNTERPARTIES])

    normal_pool = NORMAL_COUNTERPARTIES + LEGITIMATE_EDGE_CASES
    return weighted_choice([(p, p["weight"]) for p in normal_pool])


def generate_payment(
    payment_id: int,
    created: datetime,
    amount_value: Decimal,
    currency: str,
    description: str,
    counterparty_name: str,
    counterparty_iban: str,
    counterparty_country: str,
    balance_after: Decimal,
):
    created_str = bunq_datetime(created)

    return {
        "Payment": {
            "id": payment_id,
            "created": created_str,
            "updated": created_str,
            "monetary_account_id": MONETARY_ACCOUNT_ID,
            "amount": {
                "currency": currency,
                "value": money(amount_value),
            },
            "payment_fee": None,
            "description": description,
            "type": "BUNQ",
            "merchant_reference": None,
            "alias": make_alias(USER_NAME, USER_IBAN, USER_COUNTRY),
            "counterparty_alias": make_alias(
                counterparty_name,
                counterparty_iban,
                counterparty_country,
                label_type=random.choices(
                    ["PERSON", "ORGANIZATION"],
                    weights=[55, 45],
                    k=1,
                )[0],
            ),
            "attachment": [],
            "geolocation": None,
            "batch_id": None,
            "scheduled_id": None,
            "address_billing": None,
            "address_shipping": None,
            "sub_type": "PAYMENT",
            "payment_arrival_expected": {
                "status": random.choices(
                    ["ARRIVED", "PENDING", "CANCELLED"],
                    weights=[97, 2.5, 0.5],
                    k=1,
                )[0],
                "time": None,
            },
            "request_reference_split_the_bill": [],
            "balance_after_mutation": {
                "currency": currency,
                "value": money(balance_after),
            },
            "payment_auto_allocate_instance": None,
            "payment_suspended_outgoing": None,
        }
    }


# -----------------------------
# Dataset generation
# -----------------------------

def generate_transaction_specs(n: int):
    """
    Generate internal transaction specs first.

    These specs contain label information, but the labels are NOT written into
    the bunq transaction file. They are only used for the separate labels file.
    """

    specs = []
    balance = Decimal("2500.00")
    payment_id_start = 26174613
    next_payment_id = payment_id_start

    dates = sorted(random_datetime(START_DATE, END_DATE) for _ in range(n))

    for created in dates:
        if len(specs) >= n:
            break

        is_scam = random.random() < SCAM_RATE
        profile = choose_transaction_profile(is_scam)

        counterparty_name = profile["name"]

        if is_scam and random.random() < 0.35:
            counterparty_name = random.choice([
                counterparty_name.upper(),
                counterparty_name.replace("Bunq", "bunq"),
                counterparty_name.replace("Office", "Service"),
                counterparty_name + " BV",
                counterparty_name + " Support",
            ])

        country = profile["country"]
        counterparty_iban = random_iban(country)
        currency = random_currency(is_scam)

        amount_value = random_amount(
            profile["amount_range"][0],
            profile["amount_range"][1],
            scam=is_scam,
        )

        description = random.choice(profile["descriptions"])

        if not is_scam and random.random() < 0.20:
            description += f" {created.strftime('%b').lower()}"

        if is_scam and random.random() < 0.30:
            description = random.choice([
                description.upper(),
                description + " - urgent",
                description + " ref " + str(random.randint(100000, 999999)),
            ])

        balance += amount_value

        specs.append({
            "payment_id": next_payment_id,
            "created": created,
            "amount_value": amount_value,
            "currency": currency,
            "description": description,
            "counterparty_name": counterparty_name,
            "counterparty_iban": counterparty_iban,
            "counterparty_country": country,
            "balance_after": balance,
            "is_scam": is_scam,
            "scam_type": profile.get("scam_type") if is_scam else None,
        })

        next_payment_id += 1

        # Optional scam burst: multiple scam payments close together.
        if is_scam and random.random() < 0.15:
            burst_count = random.randint(1, 3)

            for _ in range(burst_count):
                if len(specs) >= n:
                    break

                burst_created = created + timedelta(minutes=random.randint(1, 20))

                burst_amount = random_amount(
                    profile["amount_range"][0],
                    profile["amount_range"][1],
                    scam=True,
                )

                balance += burst_amount

                specs.append({
                    "payment_id": next_payment_id,
                    "created": burst_created,
                    "amount_value": burst_amount,
                    "currency": currency,
                    "description": random.choice(profile["descriptions"]) + " follow-up",
                    "counterparty_name": counterparty_name,
                    "counterparty_iban": counterparty_iban,
                    "counterparty_country": country,
                    "balance_after": balance,
                    "is_scam": True,
                    "scam_type": profile.get("scam_type"),
                })

                next_payment_id += 1

    specs.sort(key=lambda x: x["created"])

    return specs[:n]


def generate_dataset(n: int):
    specs = generate_transaction_specs(n)

    transactions = []
    labels = {}

    for spec in specs:
        payment = generate_payment(
            payment_id=spec["payment_id"],
            created=spec["created"],
            amount_value=spec["amount_value"],
            currency=spec["currency"],
            description=spec["description"],
            counterparty_name=spec["counterparty_name"],
            counterparty_iban=spec["counterparty_iban"],
            counterparty_country=spec["counterparty_country"],
            balance_after=spec["balance_after"],
        )

        transactions.append(payment)

        labels[str(spec["payment_id"])] = {
            "is_scam": spec["is_scam"],
            "scam_type": spec["scam_type"],
        }

    bunq_dataset = {
        "Response": transactions
    }

    return bunq_dataset, labels


def main():
    dataset, labels = generate_dataset(N_TRANSACTIONS)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    with open(LABELS_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(labels, f, indent=2, ensure_ascii=False)

    n_total = len(dataset["Response"])
    n_scam = sum(1 for label in labels.values() if label["is_scam"])

    print(f"Wrote {n_total} transactions to {OUTPUT_FILE}")
    print(f"Wrote labels to {LABELS_OUTPUT_FILE}")
    print(f"Scam transactions: {n_scam} ({n_scam / n_total:.2%})")


if __name__ == "__main__":
    main()