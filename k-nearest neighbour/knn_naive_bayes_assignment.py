# Assignment: K-Nearest Neighbors (KNN) & Naive Bayes

# Practical -  
# Dataset
# Use the following datasets:

# Wine Dataset from sklearn.datasets
# Fake and Real News Dataset from Kaggle (containing article text and labels)
# Part A: K-Nearest Neighbors on Wine Dataset
# Load the Wine dataset using sklearn.datasets.load_wine.
# Divide the data into training and testing sets (80-20).
# Scale the features using StandardScaler.
# Train a KNN classifier and make predictions.

# Evaluate the model using:
# Accuracy
# Confusion matrix
# Classification report
# Test the model with different k values (e.g., 1, 3, 7, 11) and summarize the results.
# Plot accuracy vs different values of k.
# Part B: Naive Bayes on Fake News Dataset
# Load the dataset from Kaggle (contains news headlines/content and a label indicating fake or real).
# Perform:
# Text preprocessing (lowercase, stopword removal, punctuation handling)

# Tokenization
# Vectorization using TfidfVectorizer
# Split the dataset into training and testing sets (80-20).
# Train and evaluate a Multinomial Naive Bayes model.
# Use the following metrics:

# Accuracy
# Precision, Recall, F1-Score
# Confusion matrix

# Also train a Bernoulli Naive Bayes model and compare performance.
# Comment on the types of misclassifications and what might be causing them.
# _____________________________________________________________________________________________________

import os
import re
import pandas as pd
import numpy as np
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import matplotlib.pyplot as plt

# -----------------------
# Part A: K-Nearest Neighbors on Wine Dataset
# -----------------------
def run_wine_knn():
    wine = load_wine()
    X, y = wine.data, wine.target

    # Split (80/20) & scale
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    ks = [1, 3, 7, 11]
    accuracies = {}
    for k in ks:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        accuracies[k] = acc
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred)

        print(f"\nWine Dataset – KNN (k={k})")
        print(f"Accuracy: {acc:.3f}")
        print("Confusion Matrix:")
        print(cm)
        print("Classification Report:")
        print(report)

    # Plot accuracy vs k
    plt.figure()
    plt.plot(ks, [accuracies[k] for k in ks], marker='o')
    plt.title("Wine Dataset: Accuracy vs. k")
    plt.xlabel("k (neighbors)")
    plt.ylabel("Accuracy")
    plt.xticks(ks)
    plt.show()

# -----------------------
# Part B: Naive Bayes on Fake/Real News Dataset
# -----------------------
def run_fake_real_nb():
    # Adjust filenames/paths as needed
    # This assumes Kaggle’s Fake.csv and True.csv are in ./data/
    fake_path = './data/Fake.csv'
    true_path = './data/True.csv'
    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        raise FileNotFoundError("Place Fake.csv and True.csv in ./data/")

    df_fake = pd.read_csv(fake_path)
    df_true = pd.read_csv(true_path)
    df_fake['label'] = 'fake'
    df_true['label'] = 'real'
    df = pd.concat([df_fake, df_true], ignore_index=True)

    # Use the article text column (often named 'text' or 'title + text')
    # Here we assume df has a 'text' column; adjust if necessary.
    text_col = 'text' if 'text' in df.columns else df.columns[1]
    df = df.dropna(subset=[text_col, 'label'])
    df['clean_text'] = (
        df[text_col]
        .astype(str)
        .str.lower()
        .str.replace(r'[^\w\s]', '', regex=True)
    )
    df['target'] = df['label'].map({'real': 0, 'fake': 1})

    # Split & vectorize
    X = df['clean_text']
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    vect = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_vec = vect.fit_transform(X_train)
    X_test_vec  = vect.transform(X_test)

    # MultinomialNB
    mnb = MultinomialNB()
    mnb.fit(X_train_vec, y_train)
    y_pred_mnb = mnb.predict(X_test_vec)
    print("\nMultinomialNB on Fake/Real News")
    print("Accuracy:", accuracy_score(y_test, y_pred_mnb))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_mnb))
    print("Classification Report:\n", classification_report(y_test, y_pred_mnb))

    # BernoulliNB
    bnb = BernoulliNB()
    bnb.fit(X_train_vec, y_train)
    y_pred_bnb = bnb.predict(X_test_vec)
    print("\nBernoulliNB on Fake/Real News")
    print("Accuracy:", accuracy_score(y_test, y_pred_bnb))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_bnb))
    print("Classification Report:\n", classification_report(y_test, y_pred_bnb))

    # Misclassification analysis
    cm_mnb = confusion_matrix(y_test, y_pred_mnb)
    fp = cm_mnb[0,1]
    fn = cm_mnb[1,0]
    print(f"\nFalse Positives (real→fake): {fp}")
    print(f"False Negatives (fake→real): {fn}")
    print("""
Interpretation:
- False positives (real classified as fake) may occur when legitimate articles share sensational wording.
- False negatives (fake classified as real) can happen if fake articles mimic straightforward journalistic style.
""")

if __name__ == "__main__":
    print("=== Part A: Wine KNN ===")
    run_wine_knn()
    print("\n=== Part B: Fake/Real News Naive Bayes ===")
    run_fake_real_nb()
