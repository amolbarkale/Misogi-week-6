"""
Decision Tree classification on the Mushroom dataset:
- Q1: Load & explore
- Q2: Encode categorical features
- Q3: Train/test split
- Q4: Train Decision Tree
- Q5: Visualize tree
- Q6: Evaluate model
- Q7: Hyperparameter tuning
- Q8: Feature importance
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def main():
    # Q1. Load and Explore
    df = pd.read_csv('mushrooms.csv')
    print("Shape:", df.shape)
    print("Null values per column:\n", df.isnull().sum())
    print("Class distribution:\n", df['class'].value_counts())

    # Q2. Encode Categorical Features
    # Map 'e' → 0, 'p' → 1
    df['target'] = df['class'].map({'e': 0, 'p': 1})
    X_raw = df.drop(['class', 'target'], axis=1)
    y = df['target']
    # One-hot encode all categorical columns
    X = pd.get_dummies(X_raw)
    print("Encoded feature space shape:", X.shape)

    # Q3. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Q4. Build Decision Tree Classifier
    clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
    clf.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, clf.predict(X_train))
    test_acc  = accuracy_score(y_test,  clf.predict(X_test))
    print(f"Training Accuracy: {train_acc:.4f}")
    print(f"Test Accuracy:     {test_acc:.4f}")

    # Q5. Visualize the Decision Tree (depth=3)
    plt.figure(figsize=(20,10))
    plot_tree(
        clf,
        max_depth=3,
        feature_names=X.columns,
        class_names=['edible','poisonous'],
        filled=True,
        fontsize=8,
    )
    plt.title("Decision Tree (depth=3)")
    plt.show()

    # Q6. Evaluate the Model
    y_pred = clf.predict(X_test)
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['edible','poisonous']))

    # Q7. Tune Hyperparameters
    param_grid = {
        'max_depth': [None, 5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid = GridSearchCV(
        DecisionTreeClassifier(criterion='entropy', random_state=42),
        param_grid, cv=5, scoring='accuracy'
    )
    grid.fit(X_train, y_train)
    best = grid.best_estimator_
    print("Best parameters:", grid.best_params_)
    print("Tuned Test Accuracy:", accuracy_score(y_test, best.predict(X_test)))

    # Q8. Feature Importance
    importances = best.feature_importances_
    feat_imp = pd.Series(importances, index=X.columns)
    top5 = feat_imp.sort_values(ascending=False).head(5)
    print("\nTop 5 Feature Importances:")
    print(top5)

    plt.figure(figsize=(8,4))
    top5.plot(kind='bar')
    plt.title("Top 5 Feature Importances")
    plt.ylabel("Importance")
    plt.show()

if __name__ == "__main__":
    main()
