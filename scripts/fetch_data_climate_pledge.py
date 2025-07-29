import requests
import time
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AMAZON_API_KEY")

def fetch_products(query, max_pages=2):
    base_url = "https://serpapi.com/search"
    product_list = []

    for page in range(1, max_pages + 1):
        params = {
            "engine": "amazon",
            "amazon_domain": "amazon.com",
            "k": query,
            "api_key": API_KEY,
            "page": page
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Error on page {page}: {data['error']}")
            break

        products = data.get("organic_results", [])
        if not products:
            break

        for product in products:
            title = product.get("title")
            snippet = product.get("snippet")
            asin = product.get("asin")
            # Check for climate pledge label
            is_climate_friendly = (
                product.get("climate_pledge_friendly") or
                product.get("badge") == "Climate Pledge Friendly"
            )

            product_list.append({
                "title": title,
                "snippet": snippet,
                "asin": asin,
                "climate_pledge_friendly": is_climate_friendly
            })

    return product_list

def fetch_product_description(asin):
    url = "https://serpapi.com/search"
    params = {
        "engine": "amazon_product",
        "amazon_domain": "amazon.com",
        "product_id": asin,
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data.get("product_description")

# Fetch green products
green_products = fetch_products(query="eco friendly", max_pages=2)

# Fetch broader products
all_products = fetch_products(query="household", max_pages=2)

# Remove duplicates from broader list if already in green_products
green_asins = set(p['asin'] for p in green_products if p['asin'])
non_green_products = [p for p in all_products if p['asin'] not in green_asins]

# Combine lists
combined_products = green_products + non_green_products

# Label by presence of climate pledge friendly
for p in combined_products:
    if p.get("climate_pledge_friendly"):
        p["label"] = "Green"
    else:
        p["label"] = "Not Green"

# Fetch descriptions for all products
for product in combined_products:
    asin = product.get("asin")
    if asin:
        product["description"] = fetch_product_description(asin)
    else:
        product["description"] = None

# Save results
df = pd.DataFrame(combined_products)
os.makedirs("data", exist_ok=True)
df.to_csv("data/products_labeled.csv", index=False)
