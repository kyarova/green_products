# Green Product Classifier

This project classifies Amazon product listings as **Green**, **Not Green**, or **Unsure**, based on product titles and descriptions. The goal is to identify eco-friendly products and inform customers about greener product choice.

---

## Project Objective

Build a lightweight text classifier to help distinguish between green and non-green consumer products, using simple text-based features and an iterative, keyword-driven approach. 

---

## Future Vision

This model can be deployed as a browser extension to inform customers whether products are green or non-green, raising awareness and encouraging eco-friendly purchases. The ultimate goal is a recommender system that suggests green alternatives when customers browse non-green products.

---

## How It Works

1. **Keyword-Based Seeding**

   * Began with a list of “green” keywords such as `reusable`, `organic`, `compostable`, etc.
   * These keywords were used to collect an initial dataset of products from Amazon.

2. **Balanced Dataset Collection**

   * Queried both green and neutral keywords to gather a roughly even split of green and non-green products.

3. **Text Classification**

   * A classifier (e.g., logistic regression) was trained using TF-IDF features from product titles.
   * Predictions include probability scores used to assess confidence levels.

4. **Confidence-Based Labeling**

   * Products are labeled as:

     * **Green**: Classified as green with high confidence.
     * **Not Green**: Classified as not green with high confidence.
     * **Unsure**: Confidence is below the defined threshold (currently 70%), indicating uncertainty or ambiguous signals.

5. **Streamlit Interface**

   * Built an internal tool to inspect classifications, review errors, and refine keyword logic and model predictions.

---

## Project Evolution

* Initial version relied solely on a limited list of green keywords.
* Expanded keyword list by reviewing misclassified products and incorporating additional sustainability terms.
* Introduced a third category, **Unsure**, for cases with low model confidence.
* Identified mislabeling opportunities, such as reusable metal razors incorrectly marked as greenish due to keyword gaps.
* Future step: begin manual labeling to correct and improve model performance, particularly for edge cases.

---

## Potential Improvements

* Include product descriptions in addition to titles (in progress).
* Label based on "Climate Pledge" badge from Amazon (in progress).
* Use contextual language models (e.g., BERT) to better handle implicit green indicators.
* Develop a greenwashing detector by comparing product claims to actual materials or features.

---

## Setup and Run Instructions

1. Clone the repository
2. Set up a virtual environment

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies

   ```
   pip install -r requirements.txt
   ```
4. Get a SerpAPI key and save it in a `.env` file

   - Sign up at: https://serpapi.com/
   - Create a file named `.env` in the project root with the following content:

     ```
     AMAZON_API_KEY="YOUR_API_KEY"
     ```
5. Generate training data

   ```
   python scripts/fetch_data.py
   ```
6. Train the model

   ```
   python main.py
   ```
7. Launch the Streamlit app

   ```
   streamlit run app.py
   ```

---

## Project Structure

```
green_products/
│
├── models/
│   ├── green_classifier.pkl          # Trained classification model for green product detection
│   └── vectorizer.pkl                # Fitted vectorizer (e.g., TF-IDF) used for transforming product titles
│
├── scripts/
│   ├── fetch_data.py                 # Script to fetch and store Amazon product data
│   ├── fetch_data_climate_pledge.py  # (In progress) Script to fetch description for product data and climate pledge badge
│   └── utils.py                      # Helper functions used across the project
│
├── .env                              # Environment variable file (e.g., for API keys)
├── .gitignore                        # Files and directories to ignore in version control
├── app.py                            # Streamlit app for reviewing and correcting classifications
├── green_keywords.txt                # Initial and expanded list of green-related keywords
├── main.py                           # Main training and inference script for the classifier
├── requirements.txt                  # Project dependencies 
└── README.md                         # Project documentation

```
