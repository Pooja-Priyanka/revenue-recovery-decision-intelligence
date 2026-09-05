import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)


# ==========================================
# 1. LOAD DATA
# ==========================================

file_path = "data/processed/temporal_account_features.csv"

df = pd.read_csv(file_path)

print("====================================")
print("CHURN MODEL TRAINING")
print("====================================")

print("\nDataset shape:")
print(df.shape)


# ==========================================
# 2. DEFINE FEATURES AND TARGET
# ==========================================

target = "churn_target"

# Columns that should NOT be used for training
drop_columns = [
    "account_id",
    "account_name",
    "signup_date",
    "churn_target"
]

X = df.drop(columns=drop_columns)
y = df[target]


print("\nFeatures used:")
for column in X.columns:
    print("-", column)

print("\nTarget:")
print(target)


# ==========================================
# 3. IDENTIFY COLUMN TYPES
# ==========================================

categorical_features = [
    "industry",
    "country",
    "referral_source",
    "plan_tier"
]

numeric_features = [
    "seats",
    "current_mrr",
    "current_arr",
    "total_usage_count",
    "ticket_count",
    "avg_satisfaction",
    "escalation_rate",
    "tenure_days"
]

boolean_features = [
    "is_trial",
    "has_upgraded",
    "has_downgraded"
]


# ==========================================
# 4. PREPROCESSING
# ==========================================

numeric_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_pipeline, numeric_features),
        ("categorical", categorical_pipeline, categorical_features)
    ]
)


# ==========================================
# 5. CREATE MODEL PIPELINE
# ==========================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )
    ]
)


# ==========================================
# 6. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 7. TRAIN MODEL
# ==========================================

print("\nTraining Logistic Regression...")

model.fit(X_train, y_train)

print("Training completed!")


# ==========================================
# 8. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# ==========================================
# 9. EVALUATE MODEL
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n====================================")
print("MODEL PERFORMANCE")
print("====================================")

print(f"Accuracy :  {accuracy:.4f}")
print(f"Precision:  {precision:.4f}")
print(f"Recall   :  {recall:.4f}")
print(f"F1 Score :  {f1:.4f}")
print(f"ROC-AUC  :  {roc_auc:.4f}")


print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))


# ==========================================
# 10. SAVE MODEL
# ==========================================

model_path = "models/churn_risk_model.joblib"

joblib.dump(model, model_path)

print("\n====================================")
print("MODEL SAVED")
print("====================================")

print(f"Saved to: {model_path}")