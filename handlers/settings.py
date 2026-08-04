import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("CRYPTO_BOT_TOKEN")
TABDEAL_API_KEY = os.getenv("TABDEAL_API_KEY")
TABDEAL_SECURITY_KEY = os.getenv("TABDEAL_SECURITY_KEY")