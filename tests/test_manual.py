import os
import sys
from pathlib import Path

os.environ["SMARTCAMPUS_SECRET_KEY"] = "test-secret"
os.environ["GATEWAY_TOKEN"] = "test-token"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.app import app

client = app.test_client()

response = client.get("/notice?name={{7*7}}")

print("Status Code:", response.status_code)
print("Response:", response.get_data(as_text=True))
