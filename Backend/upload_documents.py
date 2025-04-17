import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

search_service = os.getenv("SEARCH_ENDPOINT")
api_key = os.getenv("AZURE_SEARCH_API_KEY")
index_name = "insurance-index"
plans_dir = "../insurance_plans"  # adjust if needed

url = f"https://{search_service}.search.windows.net/indexes/{index_name}/docs/index?api-version=2023-10-01-Preview"
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

documents = []

# Read each .txt file from the folder
for filename in os.listdir(plans_dir):
    if filename.endswith(".txt"):
        path = os.path.join(plans_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            doc_id = os.path.splitext(filename)[0]
            doc = {
                "@search.action": "upload",
                "id": doc_id,
                "content": content,
                "filename": filename
            }
            documents.append(doc)

# Upload in batch
response = requests.post(url, headers=headers, data=json.dumps({"value": documents}))

if response.status_code == 200:
    print("✅ Documents uploaded successfully.")
else:
    print(f"❌ Upload failed\n{response.status_code}: {response.text}")
