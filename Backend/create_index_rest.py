import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Load from .env
search_service = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = "insurance-index"
api_key = os.getenv("AZURE_SEARCH_API_KEY")

# Construct the endpoint
url = url = f"{search_service}/indexes/insurance-index?api-version=2023-10-01-Preview"

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Payload without vector search
payload = {
    "name": index_name,
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "searchable": False},
        {"name": "content", "type": "Edm.String", "searchable": True},
        {"name": "filename", "type": "Edm.String", "filterable": True, "sortable": True}
    ]
}

response = requests.put(url, headers=headers, data=json.dumps(payload))

if response.status_code == 201:
    print("✅ Non-vector index created successfully.")
else:
    print(f"❌ Failed to create index\n{response.status_code}: {response.text}")
