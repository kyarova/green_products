import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AMAZON_API_KEY")

def search_amazon(query, save_path="data/results.json"):
    params = {
        "engine": "amazon",
        "api_key": API_KEY,
        "k": query,
        "amazon_domain": "amazon.com",
        "gl": "us"
    }

    response = requests.get("https://serpapi.com/search", params=params)

    if response.status_code == 200:
        data = response.json()
        with open(save_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved results for '{query}' to {save_path}")
    else:
        print(f"Error: {response.status_code}, {response.content}")

search_amazon("soap", save_path="../data/data_raw/soap.json")
time.sleep(1)  # to respect rate limits
