import streamlit as st
import requests
from bs4 import BeautifulSoup
import joblib

clf = joblib.load('models/green_classifier.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

def extract_title(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.amazon.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            st.warning(f"Failed to fetch page, status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('span', id='productTitle')
        if not title_tag:
            title_tag = soup.find('span', class_='a-size-large product-title-word-break')

        if title_tag:
            return title_tag.get_text(strip=True)
        else:
            st.warning("Title tag not found in HTML")
            return None
    except Exception as e:
        st.error(f"Exception during title extraction: {e}")
        return None

def classify_title(title, threshold=0.65):
    processed = vectorizer.transform([title])
    pred = clf.predict(processed)[0]
    prob = clf.predict_proba(processed)[0][pred]
    if prob < threshold:
        return ('UNSURE', prob)
    return ('GREEN' if pred == 1 else 'NOT GREEN', prob)

st.title("Green Product Classifier")

url = st.text_input("Enter Amazon product URL:")

if st.button("Check"):
    if not url:
        st.error("Please enter a URL first.")
    else:
        title = extract_title(url)
        if title:
            st.write(f"**Product Title:** {title}")
            label, prob = classify_title(title)
            if label == "GREEN":
                color = "green"
            elif label == "NOT GREEN":
                color = "red"
            else:
                color = "orange"
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>**Prediction:** {label} (Confidence: {prob:.2%})</span>", unsafe_allow_html=True)
        else:
            st.error("Could not extract product title from URL. Make sure it's a valid product page.")
