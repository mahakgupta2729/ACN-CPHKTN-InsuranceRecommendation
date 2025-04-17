import os
import requests

def search_insurance_plans(query_text):
    search_service = os.getenv("SEARCH_ENDPOINT")
    index_name = os.getenv("SEARCH_INDEX_NAME")
    api_key = os.getenv("AZURE_SEARCH_API_KEY")
    api_version = "2023-10-01-Preview"

    url = f"https://{search_service}.search.windows.net/indexes/{index_name}/docs/search?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    payload = {
        "search": query_text,
        "top": 3  # Get top 3 results
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    results = response.json()
    return [doc["content"] for doc in results["value"]]
