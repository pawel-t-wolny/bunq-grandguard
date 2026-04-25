import json
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# --- CONFIGURATION & RULES ---
SUSPICIOUS_KEYWORDS = ['verificatie', 'controle', 'pakket', 'douane', 'dossier', 'refund', 'invoerrechten', 'vrijgave', 'test']
SPOOFED_ENTITIES = ['bunq', 'support', 'helpdesk', 'verify', 'ideal', 'douane', 'postnl', 'escrow']

def parse_and_engineer_features(json_file_path):
    """Parses the JSON and creates features for the ML pipeline."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    responses = data.get("Response", [])
    rows = []
    
    for item in responses:
        payment = item.get("Payment")
        if not payment:
            continue
            
        # Extract Raw Values
        amount_str = payment.get('amount', {}).get('value', '0')
        amount = abs(float(amount_str))
        desc = str(payment.get('description', '')).lower()
        counterparty = payment.get("counterparty_alias", {}).get("display_name", "").lower()
        
        try:
            hour = int(payment.get("created", "").split(' ')[1].split(':')[0])
        except:
            hour = 12

        # ---------------------------------------------------------
        # LAYER 1: RULE-BASED ENGINE (Feature Engineering)
        # ---------------------------------------------------------
        is_micro = 1 if 0.00 < amount <= 5.00 else 0
        has_phishing_word = 1 if any(kw in desc for kw in SUSPICIOUS_KEYWORDS) else 0
        has_spoofed_name = 1 if any(ent in counterparty for ent in SPOOFED_ENTITIES) else 0
        
        rule_score = 0
        if is_micro: rule_score += 2
        if has_phishing_word: rule_score += 4
        if has_spoofed_name: rule_score += 3
        
        # We need a "Ground Truth" label to test accuracy against. 
        # In a real bank, a human sets this. Here, we simulate it based on strict rules.
        is_scam = 1 if rule_score >= 5 else 0 

        rows.append({
            'amount': amount,
            'hour_of_day': hour,
            'desc_length': len(desc),
            'is_micro': is_micro,
            'has_phishing_word': has_phishing_word,
            'has_spoofed_name': has_spoofed_name,
            'rule_score': rule_score,
            'is_scam': is_scam
        })
        
    return pd.DataFrame(rows)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hybrid_fraud_test.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    print(f"Loading data from {file_path}...")
    df = parse_and_engineer_features(file_path)

    if df['is_scam'].nunique() < 2:
        print("Error: Need both safe and scam transactions to evaluate accuracy.")
        sys.exit(1)

    # ---------------------------------------------------------
    # LAYER 2: UNSUPERVISED ANOMALY DETECTION
    # ---------------------------------------------------------
    print("\nRunning Anomaly Detection (Isolation Forest)...")
    # We hide the 'is_scam' label so the model has to guess what looks weird
    features_for_anomaly = df[['amount', 'hour_of_day', 'desc_length']] 
    
    # Isolation forest flags normal as 1, anomalies as -1
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = iso_forest.fit_predict(features_for_anomaly)
    
    # Convert from [-1, 1] to [1, 0] where 1 means anomalous
    df['is_anomalous'] = df['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

    # ---------------------------------------------------------
    # LAYER 3: SUPERVISED MACHINE LEARNING (Random Forest)
    # ---------------------------------------------------------
    print("Training Supervised ML Model (Random Forest)...")
    
    # Our final inputs combine the raw math, the rule engine, and the anomaly detector
    X = df[['amount', 'hour_of_day', 'desc_length', 'is_micro', 
            'has_phishing_word', 'has_spoofed_name', 'rule_score', 'is_anomalous']]
    y = df['is_scam'] # The target we are trying to predict

    # Split data: 80% to train the model, 20% to test its accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)

    # ---------------------------------------------------------
    # EVALUATING ACCURACY
    # ---------------------------------------------------------
    print("\nTesting Model Accuracy on unseen data...")
    predictions = rf_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions)

    print("-" * 50)
    print(f"OVERALL ACCURACY: {accuracy * 100:.2f}%")
    print("-" * 50)
    
    print("\nCONFUSION MATRIX:")
    print(f"True Negatives (Safe guessed Safe):   {conf_matrix[0][0]}")
    print(f"False Positives (Safe guessed Scam):  {conf_matrix[0][1]}  <-- Annoyed Customers")
    print(f"False Negatives (Scam guessed Safe):  {conf_matrix[1][0]}  <-- Missed Fraud")
    print(f"True Positives (Scam guessed Scam):   {conf_matrix[1][1]}")
    
    print("\nDETAILED CLASSIFICATION REPORT:")
    print(classification_report(y_test, predictions, target_names=['Safe', 'Scam']))

if __name__ == "__main__":
    main()