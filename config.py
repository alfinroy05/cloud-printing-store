import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API URLs
BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
STORE_ID = os.getenv("STORE_ID")  # Correctly fetch STORE_ID
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")  # Read the token from .env
print(f"✅ Loaded API_URL: {BASE_URL}")
print(f"✅ Loaded STORE_ID: {STORE_ID}")
print(f"✅ Loaded ADMIN_TOKEN: {ADMIN_TOKEN[:10]}... (truncated)")

# Validate Token and Store ID
if not ADMIN_TOKEN:
    raise ValueError("❌ ADMIN_TOKEN is missing. Please check your .env file.")
if not STORE_ID:
    raise ValueError("❌ STORE_ID is missing. Please check your .env file.")

# API Endpoints
FETCH_ORDERS_URL = f"{BASE_URL}/orders/"
FETCH_DECRYPTION_KEY_URL = f"{BASE_URL}/get-decryption-key/"
UPDATE_STATUS_URL = f"{BASE_URL}/update-order-status/"
