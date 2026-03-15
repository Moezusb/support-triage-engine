import pandas as pd

# Load the raw data
df = pd.read_csv('raw_support_tickets.csv')

# The "Triage Logic" Function
# In a production environment, this would be a call to Claude/GPT-4
def simulate_ai_triage(text):
    text = text.lower()
    
    # Simple keyword-based logic to simulate LLM intent detection
    if "charge" in text or "refund" in text or "money" in text:
        category = "Billing"
        sentiment = 2
    elif "error" in text or "api" in text or "500" in text:
        category = "Technical"
        sentiment = 2
    elif "incredible" in text or "saved" in text:
        category = "Praise"
        sentiment = 5
    elif "slow" in text or "competitors" in text:
        category = "Churn Risk"
        sentiment = 1
    else:
        category = "General"
        sentiment = 3
        
    # Urgency Logic: Billing and Churn Risks are always high priority
    priority = "High" if category in ["Billing", "Churn Risk", "Technical"] and sentiment < 3 else "Normal"
    
    return pd.Series([category, sentiment, priority])

# Apply the "AI" logic
df[['detected_category', 'sentiment', 'priority']] = df['raw_text'].apply(simulate_ai_triage)

# Save the Triage Result
df.to_csv('triaged_tickets_report.csv', index=False)

print("--- AI TRIAGE SUMMARY ---")
print(df['priority'].value_counts())
print("\nSample of High-Priority Conversions:")
print(df[df['priority'] == 'High'][['raw_text', 'detected_category', 'priority']].head())
