from scripts.utils import load_and_combine_json_files, label_product, load_green_keywords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

import pandas as pd
import joblib
import os

os.makedirs('data/data_labeled', exist_ok=True)
os.makedirs('models', exist_ok=True)

df = load_and_combine_json_files()
df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')

green_keywords = load_green_keywords('green_keywords.txt')
print(green_keywords)

df['label'] = df['combined_text'].apply(lambda x: label_product(x, green_keywords))

df.to_csv('data/data_labeled/full_labeled_data.csv', index=False)
print("Full labeled dataset saved to 'data/data_labeled/full_labeled_data.csv'")

X = df['combined_text'].fillna('')
y = df['label'].map({'green': 1, 'not green': 0})

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

joblib.dump(clf, 'models/green_classifier.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')
print("Model and vectorizer saved to 'models/' folder")

# Get predicted labels and probabilities
y_pred = clf.predict(X_test_vec)
y_prob = clf.predict_proba(X_test_vec)

print("Classification Report")
print(classification_report(y_test, y_pred, target_names=['not green', 'green']))

print("Confusion Matrix")
print(confusion_matrix(y_test, y_pred))

test_indices = y_test.index
test_df = df.loc[test_indices].copy()
test_df['manual_label'] = y_test.map({1: 'green', 0: 'not green'})
test_df['model_label'] = pd.Series(y_pred, index=test_indices).map({1: 'green', 0: 'not green'})

print("Done")
