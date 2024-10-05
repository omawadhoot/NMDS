import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier  # Example classifier
from sklearn.metrics import accuracy_score  # For evaluation purposes

def preprocess_data(filepath):
    # Load the dataset
    data = pd.read_csv(filepath)

    # Print the columns to debug
    print("Columns in the DataFrame:", data.columns.tolist())

    # Strip whitespace from column names
    data.columns = data.columns.str.strip()

    # Data cleaning steps (e.g., handling NaN values, removing duplicates)
    data.dropna(inplace=True)

    # Feature selection/extraction
    features = data[['netspeed', 'pingtest', 'traceroute']]  # Adjust as needed
    labels = data['coverage']  # Assuming you have a 'coverage' column

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Normalize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test

def classify_network_coverage(X_train, X_test, y_train, y_test):
    # Create and train a classifier (e.g., RandomForestClassifier)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model (optional)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")

    # Example logic to classify coverage based on prediction
    # Here we are assuming you have specific thresholds or mapping logic
    coverage_results = {
        "good": sum(y_pred == "good"),
        "moderate": sum(y_pred == "moderate"),
        "bad": sum(y_pred == "bad"),
    }

    # Return the coverage results as a formatted string
    return f"Good: {coverage_results['good']}, Moderate: {coverage_results['moderate']}, Bad: {coverage_results['bad']}"
