from .api_client import APIClient
from .utils import APP_URL, CERT_FILE, KEY_FILE

api_client = APIClient(APP_URL, CERT_FILE, KEY_FILE)
