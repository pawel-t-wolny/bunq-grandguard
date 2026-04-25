import requests


payload = {
                "id": 66324902,
                "created": "2025-08-16 21:56:24.368292",
                "updated": "2025-08-16 21:56:24.368292",
                "monetary_account_id": 9098979,
                "amount": {
                    "currency": "EUR",
                    "value": "-320.59"
                },
                "payment_fee": None,
                "description": "Huur voorschot 87289",
                "type": "MASTERCARD",
                "merchant_reference": None,
                "alias": {
                    "iban": "NL79BUNQ4664039459",
                    "is_light": False,
                    "display_name": "Mijn Rekening",
                    "avatar": {
                        "uuid": "87358334-bb8f-435f-9d82-65fd8cfb0ee5",
                        "image": [
                            {
                                "attachment_public_uuid": "f696e0ff-89db-457e-8b33-86cb2af2bb37",
                                "height": 1024,
                                "width": 1024,
                                "content_type": "image/jpeg",
                                "urls": [
                                    {
                                        "type": "ORIGINAL",
                                        "url": "https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/42c98902493640629d0d0b7ece50791a.jpg"
                                    }
                                ]
                            }
                        ],
                        "anchor_uuid": None,
                        "style": "NONE"
                    },
                    "label_user": {
                        "uuid": "6c5c209a-bc39-48e7-85cf-55f0b30fcfd5",
                        "display_name": "Mijn Rekening",
                        "country": "NL",
                        "avatar": {
                            "uuid": "e616dfb0-cd84-4226-8479-b4429186d944",
                            "image": [
                                {
                                    "attachment_public_uuid": "1d2ea332-3e62-428e-9733-0a0dd29d5397",
                                    "height": 1024,
                                    "width": 480,
                                    "content_type": "image/jpeg",
                                    "urls": [
                                        {
                                            "type": "ORIGINAL",
                                            "url": "https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/574a8c0503424367982cd0f85617ea25.jpg"
                                        }
                                    ]
                                }
                            ],
                            "anchor_uuid": None,
                            "style": "NONE"
                        },
                        "public_nick_name": "Mijn",
                        "type": "PERSON"
                    },
                    "country": "NL"
                },
                "counterparty_alias": {
                    "iban": "NL13ABNA0581342661",
                    "is_light": False,
                    "display_name": "A. Visser",
                    "avatar": {
                        "uuid": "e5309e24-6903-4f24-b7a3-a315a43a2eb0",
                        "image": [
                            {
                                "attachment_public_uuid": "9999a6ad-1e4a-45d0-b6ba-cfef284d45f9",
                                "height": 480,
                                "width": 480,
                                "content_type": "image/jpeg",
                                "urls": [
                                    {
                                        "type": "ORIGINAL",
                                        "url": "https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/9bdfab00f23f42e3a727e52d8c63482a.jpg"
                                    }
                                ]
                            }
                        ],
                        "anchor_uuid": None,
                        "style": "NONE"
                    },
                    "label_user": {
                        "uuid": "2c5fd532-daa9-44f7-93f9-e4e690772fb9",
                        "display_name": "A. Visser",
                        "country": "NL",
                        "avatar": {
                            "uuid": "ae20c615-c0aa-414f-a6f5-a4cf17deccb2",
                            "image": [
                                {
                                    "attachment_public_uuid": "b88445e6-f490-4c76-899e-2a905d11c2ae",
                                    "height": 1024,
                                    "width": 480,
                                    "content_type": "image/jpeg",
                                    "urls": [
                                        {
                                            "type": "ORIGINAL",
                                            "url": "https://bunq-triage-model-storage-public.s3.eu-central-1.amazonaws.com/bunq_file/File/content/d4c9b76006184115abebab7e8e59fd5c.jpg"
                                        }
                                    ]
                                }
                            ],
                            "anchor_uuid": None,
                            "style": "NONE"
                        },
                        "public_nick_name": "A.",
                        "type": "PERSON"
                    },
                    "country": "NL"
                },
                "attachment": [],
                "geolocation": None,
                "batch_id": None,
                "scheduled_id": None,
                "address_billing": None,
                "address_shipping": None,
                "sub_type": "PAYMENT",
                "payment_arrival_expected": {
                    "status": "ARRIVED",
                    "time": None
                },
                "request_reference_split_the_bill": [],
                "balance_after_mutation": {
                    "currency": "EUR",
                    "value": "3435.58"
                },
                "payment_auto_allocate_instance": None,
                "payment_suspended_outgoing": None,
            }


response = requests.post("http://localhost:8000/predict", json=payload)


print(response.json())