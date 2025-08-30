import joblib
import os
import numpy as np
from .models import PredictionInput

# Load your trained model (placeholder for now)
def load_model():
    # For now, we'll return a placeholder. You will replace this with your actual model.
    print("ML Model Loaded - Using rule-based fraud detection")
    return "rule_based_model"

# Real fraud detection logic
def predict(model, input_data: PredictionInput):
    """
    Simple rule-based fraud detection using ONLY the available fields.
    """
    fraud_rules = {
        'suspicious_coupon': False,
        'known_fraudulent_ip': False,
        'suspicious_user_pattern': False
    }
    
    fraud_score = 0.0
    
    # Rule 1: Check for suspicious coupon patterns (using available field)
    suspicious_coupons = ['FREE100', '100OFF', 'FREEITEM', 'FREE', '100']
    if any(coupon in input_data.coupon_code.upper() for coupon in suspicious_coupons):
        fraud_rules['suspicious_coupon'] = True
        fraud_score += 0.4
    
    # Rule 2: Check for known fraudulent IP ranges (using available field)
    fraudulent_ips = ['192.168.1.100', '10.0.0.666', '172.16.0.123']
    if input_data.ip_address in fraudulent_ips:
        fraud_rules['known_fraudulent_ip'] = True
        fraud_score += 0.5
    
    # Rule 3: Check for suspicious user ID patterns (using available field)
    # Example: User IDs that look auto-generated or sequential
    if input_data.user_id.startswith('temp_') or 'bot' in input_data.user_id.lower():
        fraud_rules['suspicious_user_pattern'] = True
        fraud_score += 0.3
    
    # Cap the fraud score at 1.0
    fraud_probability = min(fraud_score, 1.0)
    is_fraud = fraud_probability > 0.6  # Threshold for fraud
    
    # Debug output
    print(f"Fraud Analysis for user {input_data.user_id}:")
    print(f"  Coupon: {input_data.coupon_code}")
    print(f"  IP: {input_data.ip_address}")
    print(f"  Rules triggered: {[k for k, v in fraud_rules.items() if v]}")
    print(f"  Fraud probability: {fraud_probability:.2f}")
    print(f"  Is fraud: {is_fraud}")
    
    return {
        "fraud_probability": round(fraud_probability, 2),
        "is_fraud": is_fraud,
        "triggered_rules": [k for k, v in fraud_rules.items() if v]
    }