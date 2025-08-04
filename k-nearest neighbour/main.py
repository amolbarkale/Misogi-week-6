import pandas as pd
import numpy as np
import re
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    confusion_matrix, accuracy_score, classification_report
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import matplotlib.pyplot as plt

def main():
    # -----------------------
    # Part A: K-Nearest Neighbors on Iris Dataset
    # -----------------------
    iris = load_iris()
    X_iris, y_iris = iris.data, iris.target

    # 1) Split (80/20) & scale
    X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(
        X_iris, y_iris, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_i = scaler.fit_transform(X_train_i)
    X_test_i = scaler.transform(X_test_i)

    # 2) Train & evaluate for k = 3, 5, 7
    for k in [3, 5, 7]:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_i, y_train_i)
        y_pred_i = knn.predict(X_test_i)

        acc = accuracy_score(y_test_i, y_pred_i)
        cm = confusion_matrix(y_test_i, y_pred_i)
        report = classification_report(y_test_i, y_pred_i)

        print(f"\n--- Iris KNN (k={k}) ---")
        print(f"Accuracy: {acc:.3f}")
        print("Confusion Matrix:")
        print(cm)
        print("Classification Report:")
        print(report)

    # (Optional) You could visualize decision boundaries for two features by slicing X_iris down to 2 dimensions.

    # -----------------------
    # Part B: Naive Bayes on SMS Spam Collection Dataset
    # -----------------------
    # Make sure you've downloaded the Kaggle CSV into /mnt/data/spam.csv
    sms = pd.read_csv('/mnt/data/spam.csv', encoding='latin-1')
    # This file often has extra unnamed columns; keep only v1(label) and v2(text)
    sms = sms[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'text'})
    sms['target'] = sms['label'].map({'ham': 0, 'spam': 1})

    # 1) Text cleaning
    sms['clean_text'] = (
        sms['text']
        .str.lower()
        .str.replace(r'[^\w\s]', '', regex=True)
    )

    # 2) Train/test split
    X_sms = sms['clean_text']
    y_sms = sms['target']
    X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
        X_sms, y_sms, test_size=0.2, random_state=42
    )

    # 3) Vectorize with TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train_s)
    X_test_vec  = vectorizer.transform(X_test_s)

    # 4A) MultinomialNB
    mnb = MultinomialNB()
    mnb.fit(X_train_vec, y_train_s)
    y_pred_mnb = mnb.predict(X_test_vec)

    print("\n--- MultinomialNB on SMS Spam ---")
    print(f"Accuracy: {accuracy_score(y_test_s, y_pred_mnb):.3f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test_s, y_pred_mnb))
    print("Classification Report:")
    print(classification_report(y_test_s, y_pred_mnb))

    # 4B) BernoulliNB
    bnb = BernoulliNB()
    bnb.fit(X_train_vec, y_train_s)
    y_pred_bnb = bnb.predict(X_test_vec)

    print("\n--- BernoulliNB on SMS Spam ---")
    print(f"Accuracy: {accuracy_score(y_test_s, y_pred_bnb):.3f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test_s, y_pred_bnb))
    print("Classification Report:")
    print(classification_report(y_test_s, y_pred_bnb))

    # 5) False Positives & False Negatives (for MultinomialNB)
    cm_mnb = confusion_matrix(y_test_s, y_pred_mnb)
    fp = cm_mnb[0,1]   # ham→spam
    fn = cm_mnb[1,0]   # spam→ham
    print(f"\nMultinomialNB False Positives (ham→spam): {fp}")
    print(f"MultinomialNB False Negatives (spam→ham): {fn}")

    print("""
    Interpretation:
    - False positives (ham classified as spam) risk blocking legitimate messages.
    - False negatives (spam classified as ham) risk letting spam slip through.
    """)

if __name__ == "__main__":
    main()