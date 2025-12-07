"""
Training script for language detection model.
This script trains the model and saves all necessary components.
"""

import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("=" * 60)
print("Language Detection Model Training")
print("=" * 60)

# 1. Load dataset
print("\n[1/6] Loading dataset...")
try:
    df = pd.read_csv('Language Detection.csv')
    print(f"[OK] Dataset loaded: {df.shape[0]} samples, {df.shape[1]} columns")
    
    # Show language distribution
    lang_counts = df['Language'].value_counts()
    print(f"\n[INFO] Language distribution:")
    for lang, count in lang_counts.items():
        print(f"  {lang:20s}: {count:5d} samples")
    
    # Warn about languages with very few samples
    min_samples = 50
    low_sample_langs = lang_counts[lang_counts < min_samples]
    if len(low_sample_langs) > 0:
        print(f"\n[WARNING] Languages with fewer than {min_samples} samples:")
        for lang, count in low_sample_langs.items():
            print(f"  {lang:20s}: {count:5d} samples (may affect accuracy)")
        print(f"  Consider adding more samples for better accuracy.")
    
except FileNotFoundError:
    print("[ERROR] 'Language Detection.csv' not found!")
    print("Please download it from: https://www.kaggle.com/basilb2s/language-detection")
    print("Or create one using: python add_languages.py")
    exit(1)

# 2. Preprocessing function
def preprocess_text(text):
    """Clean and preprocess text data."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 3. Preprocess data
print("\n[2/6] Preprocessing text data...")
df['Text_Cleaned'] = df['Text'].apply(preprocess_text)

# Remove empty texts
empty_texts = df[df['Text_Cleaned'].str.len() == 0]
if len(empty_texts) > 0:
    df = df[df['Text_Cleaned'].str.len() > 0].reset_index(drop=True)
    print(f"[OK] Removed {len(empty_texts)} empty texts")
print(f"[OK] Preprocessing complete: {len(df)} samples remaining")

# 4. Label encoding
print("\n[3/6] Encoding language labels...")
label_encoder = LabelEncoder()
df['Language_Encoded'] = label_encoder.fit_transform(df['Language'])
print(f"[OK] Encoded {len(label_encoder.classes_)} languages:")
for lang in sorted(label_encoder.classes_):
    print(f"  - {lang}")

# 5. Prepare features and split data
print("\n[4/6] Preparing features and splitting data...")
X = df['Text_Cleaned']
y = df['Language_Encoded']

# Use stratify only if all classes have at least 2 samples
try:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
except ValueError:
    # If stratification fails (some languages have too few samples), don't stratify
    print("[WARNING] Some languages have too few samples for stratification. Using non-stratified split.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
print(f"[OK] Training set: {len(X_train)} samples")
print(f"[OK] Test set: {len(X_test)} samples")

# 6. Feature engineering
print("\n[5/6] Creating feature vectors...")
count_vectorizer = CountVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_bow = count_vectorizer.fit_transform(X_train)
X_test_bow = count_vectorizer.transform(X_test)
print(f"[OK] Feature matrix shape: {X_train_bow.shape}")

# Also create TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
tfidf_vectorizer.fit(X_train)
print(f"[OK] TF-IDF vectorizer created")

# 7. Train model
print("\n[6/6] Training Multinomial Naive Bayes model...")
nb_model = MultinomialNB(alpha=1.0)
nb_model.fit(X_train_bow, y_train)
print("[OK] Model trained successfully")

# Evaluate model
y_pred = nb_model.predict(X_test_bow)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n[Performance] Model Performance:")
print(f"   Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("\n[Classification Report]")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# 8. Save model and components
print("\n[Saving] Saving model and components...")
try:
    joblib.dump(nb_model, 'language_detection_model.pkl')
    joblib.dump(count_vectorizer, 'count_vectorizer.pkl')
    joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
    joblib.dump(label_encoder, 'label_encoder.pkl')
    print("[OK] Model saved: language_detection_model.pkl")
    print("[OK] Vectorizer saved: count_vectorizer.pkl")
    print("[OK] TF-IDF vectorizer saved: tfidf_vectorizer.pkl")
    print("[OK] Label encoder saved: label_encoder.pkl")
except Exception as e:
    print(f"[ERROR] Error saving model: {e}")
    exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] Training completed successfully!")
print("=" * 60)
print("\nYou can now run the Streamlit app:")
print("  streamlit run app.py")

