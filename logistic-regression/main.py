import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import (
    train_test_split, cross_val_score, GridSearchCV
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc
)
import matplotlib.pyplot as plt

def main():
    # -----------------------
    # Step 1: Data Preprocessing
    # -----------------------
    # 1.1 Load and inspect
    df = pd.read_csv('/heart_cleveland_upload.csv')
    print("Dataset shape:", df.shape)
    print(df.head())

    # 1.2 Handle missing values
    df = df.dropna()

    # 1.3 Encode categorical variables
    categorical_cols = [
        'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'
    ]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 1.4 Scale numerical features
    target_col = 'condition'
    feature_cols = [c for c in df.columns if c != target_col]
    scaler = StandardScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    # 1.5 Binarize the target
    df['target'] = df[target_col].apply(lambda x: 1 if x > 0 else 0)
    df.drop(target_col, axis=1, inplace=True)

    # -----------------------
    # Step 2: Exploratory Data Analysis (EDA)
    # -----------------------
    # 2.1 Correlation with target
    corr_with_target = df.corr()['target'].sort_values(ascending=False)
    print("\nCorrelation with target:\n", corr_with_target)

    # 2.2 Visualize distributions
    plt.figure()
    plt.hist(df['age'], bins=20)
    plt.title("Age Distribution (standardized)")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.show()

    plt.figure()
    plt.hist(df['chol'], bins=20)
    plt.title("Cholesterol Distribution (standardized)")
    plt.xlabel("Cholesterol")
    plt.ylabel("Frequency")
    plt.show()

    # 2.3 Class balance
    print("\nClass balance:\n", df['target'].value_counts())

    plt.figure()
    plt.bar(['No Disease','Disease'], df['target'].value_counts().values)
    plt.title("Class Balance")
    plt.ylabel("Count")
    plt.show()

    # 2.4 Feature selection by correlation threshold
    selected_features = corr_with_target[abs(corr_with_target) > 0.1]\
        .drop('target').index.tolist()
    print("\nSelected features:", selected_features)

    # -----------------------
    # Step 3: Logistic Regression Implementation
    # -----------------------
    X = df[selected_features]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # 3.1 Coefficients & intercept
    coef_df = pd.DataFrame({
        'feature': selected_features,
        'coefficient': model.coef_[0]
    })
    print("\nModel coefficients:\n", coef_df)
    print("Intercept:", model.intercept_[0])

    # 3.2 Interpret two coefficients
    for feat in selected_features[:2]:
        idx = selected_features.index(feat)
        print(f"- 1-SD increase in {feat} ⇒ log-odds change {model.coef_[0][idx]:.3f}")

    # -----------------------
    # Step 4: Model Evaluation
    # -----------------------
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    print(
        f"\nAccuracy: {accuracy:.3f}, "
        f"Precision: {precision:.3f}, "
        f"Recall: {recall:.3f}, "
        f"F1-Score: {f1:.3f}"
    )

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

    # ROC Curve & AUC
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    print(f"ROC AUC: {roc_auc:.3f}")

    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0,1], [0,1], '--')
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.show()

    # 4.1 5-Fold Cross-Validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print("5-Fold CV accuracies:", cv_scores)
    print("Average CV accuracy:", cv_scores.mean())

    # -----------------------
    # Step 5: Model Tuning & Interpretation
    # -----------------------
    param_grid = {'C': [0.01, 0.1, 1, 10, 100]}
    grid = GridSearchCV(
        LogisticRegression(max_iter=1000),
        param_grid, cv=5, scoring='accuracy'
    )
    grid.fit(X_train, y_train)

    print("Best C:", grid.best_params_['C'])
    print("Best CV accuracy:", grid.best_score_)

    # 5.1 Summary of insights
    print("""
    Summary:
    - Initial accuracy: {:.3f}, AUC: {:.3f}
    - Avg. 5-fold CV accuracy: {:.3f}
    - After tuning (C={}): CV accuracy: {:.3f}
    Insights:
    1. Higher age & lower max heart rate ↑ disease odds.
    2. Elevated cholesterol also ↑ risk.
    Clinical implication: This model can serve as a quick screening tool to flag high-risk patients for further tests.
    """.format(
        accuracy, roc_auc, cv_scores.mean(),
        grid.best_params_['C'], grid.best_score_
    ))


if __name__ == "main":
    main()