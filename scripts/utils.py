import json
import pandas as pd
import glob

def load_and_combine_json_files(folder_path="data/data_raw"):
    all_records = []

    json_files = glob.glob(f"{folder_path}/*.json")

    for file in json_files:
        print(f"Loading {file} ...")
        with open(file, "r") as f:
            data = json.load(f)
        products = data.get("organic_results", [])
        for p in products:
            title = p.get("title", "")
            snippet = p.get("snippet", "") or p.get("description", "")
            url = p.get("link", "")
            source_file = file.split("/")[-1]
            all_records.append({
                "title": title,
                "description": snippet,
                "url": url,
                "source": source_file,
                "label": None
            })

    df = pd.DataFrame(all_records)
    return df


def label_product(text, green_keywords):
    if not isinstance(text, str):
        return 'not green'
    text = text.lower()
    for kw in green_keywords:
        if kw in text:
            return 'green'
    return 'not green'