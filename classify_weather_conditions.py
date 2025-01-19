import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
from collections import Counter
import os

# Step 1: Load and preprocess the dataset
file_path = "/Users/auninasuha/Documents/USM/SEM 7/CPC357/Project/Dataset/Merged_sensor_data.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Step 2: Create a target column based on sensor readings
def classify_weather(row):
    if row['Raining'] == 1:
        return 'Rainy'
    elif row['Temperature'] > 25 and row['Humidity'] < 70:
        return 'Sunny'
    else:
        return 'Cloudy'

# Uncomment this line if you want to create the Weather Condition column based on the logic
data['Weather Condition'] = data.apply(classify_weather, axis=1)

# Step 3: Handle missing values
data = data.dropna()  # Drop rows with missing values

# Step 4: Prepare features (X) and target (y)
X = data[["Raining", "Temperature", "Humidity"]]
y = data["Weather Condition"].astype("category").cat.codes  # Encode target variable

# Check unique classes in the target variable
print("Unique classes in target variable:", y.unique())

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print(f"Original class distribution: {Counter(y_train)}")
print(f"Resampled class distribution: {Counter(y_train_resampled)}")

# Step 7: Train the Random Forest model
model = RandomForestClassifier(class_weight="balanced", random_state=42)
model.fit(X_train_resampled, y_train_resampled)

# Step 8: Evaluate the model
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Calculate ROC AUC for each class
roc_auc_scores = {}
classes = ["Sunny", "Rainy", "Cloudy"]

for i in range(len(classes)):
    # Extract probabilities for the current class
    y_pred_proba_class = y_pred_proba[:, i]  # Get probabilities for class i
    roc_auc = roc_auc_score(
        (y_test == i).astype(int),  # Convert y_test to binary for class i
        y_pred_proba_class,  # Use probabilities for class i
        average="weighted"  # Weighted to account for class imbalance
    )
    roc_auc_scores[classes[i]] = roc_auc

print("Multiclass ROC-AUC Scores:")
for class_name, score in roc_auc_scores.items():
    print(f"{class_name}: {score:.4f}")

# Step 9: Perform cross-validation
skf = StratifiedKFold(n_splits=5)
cv_scores = cross_val_score(model, X_train_resampled, y_train_resampled, cv=skf, scoring="roc_auc_ovr")
print(f"Cross-validated ROC-AUC scores: {cv_scores}")
print(f"Mean ROC-AUC score: {cv_scores.mean()}")

# Step 10: Make predictions on the entire dataset
data['Predicted Weather Condition'] = model.predict(X)

# Step 11: Save the updated DataFrame to a new CSV file
output_file_path = "/Users/auninasuha/Documents/USM/SEM 7/CPC357/Project/Dataset/paddy_sensor_data.csv"
data.to_csv(output_file_path, index=False)
print(f"Predictions saved to '{output_file_path}'")

