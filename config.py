import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API URLs
BASE_URL = os.getenv("API_URL", "http://localhost:8000/api")
STORE_ID = os.getenv("1")
ADMIN_TOKEN = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODMyMzUwLCJpYXQiOjE3NDI4MzIwNTAsImp0aSI6IjM4MjhiY2M3MDQ4NDQ1NjRiMjRiYTY1OGQzMmU3OTU1IiwidXNlcl9pZCI6Nn0.SS8kp3OWJU2B29C8iwqNhnWL3s8iTmOPErXxGTVV44w")

FETCH_ORDERS_URL = f"{BASE_URL}/store/orders/"
FETCH_DECRYPTION_KEY_URL = f"{BASE_URL}/get-decryption-key/"
UPDATE_STATUS_URL = f"{BASE_URL}/update-order-status/"
