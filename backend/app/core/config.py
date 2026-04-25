import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BUNQ_API_KEY = os.getenv("BUNQ_API_KEY", "")
    NGROK_URL = os.getenv("NGROK_URL", "")

settings = Settings()
