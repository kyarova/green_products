from scripts.utils import load_and_combine_json_files, label_product
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Load all JSON data
df = load_and_combine_json_files()
df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('')

# Define green keywords and apply labeling
green_keywords = [
    'biodegradable', 'natural', 'organic', 'recycled', 'compostable',
    'non-toxic', 'eco-friendly', 'plastic-free', 'sustainable',
    'fair trade', 'energy star', 'bpa-free', 'vegan'
]

df['label'] = df['combined_text'].apply(lambda x: label_product(x, green_keywords))

# Save labeled data
df.to_csv('data/data_labeled/full_labeled_data.csv', index=False)
print("✅ Full labeled dataset saved to 'full_labeled_data.csv'")

# Prepare data for training
X = df['combined_text'].fillna('')
y = df['label'].map({'green': 1, 'not green': 0})

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train_vec, y_train)

# Evaluate model
y_pred = clf.predict(X_test_vec)

print(" Classification Report ")
print(classification_report(y_test, y_pred, target_names=['not green', 'green']))

print(" Confusion Matrix ")
print(confusion_matrix(y_test, y_pred))
