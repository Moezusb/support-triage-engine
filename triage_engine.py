import pandas as pd

df = pd.read_csv('raw_support_tickets.csv')

def simulate_ai_triage(text):
    text = text.lower()
    
    # Priority Keywords for PR and Security
    if any(word in text for word in ["legal", "social media", "vulnerability", "security", "sue"]):
        category = "PR Risk"
        sentiment = 1
    elif any(word in text for word in ["crash", "error", "api", "500"]):
        category = "Technical Bug"
        sentiment = 2
    elif "enterprise" in text or "quote" in text:
        category = "Sales"
        sentiment = 3
    else:
        category = "General"
        sentiment = 3
        
    # Strategic Urgency Logic
    # PR Risks are ALWAYS Critical. Technical bugs with low sentiment are High.
    if category == "PR Risk":
        priority = "CRITICAL"
    elif category in ["Technical Bug", "Churn Risk"]:
        priority = "High"
    else:
        priority = "Normal"
    
    return pd.Series([category, sentiment, priority])

df[['detected_category', 'sentiment', 'priority']] = df['raw_text'].apply(simulate_ai_triage)
df.to_csv('triaged_tickets_report.csv', index=False)

print("--- AI TRIAGE VOLUME REPORT ---")
print(df['priority'].value_counts())
print("\n--- SAMPLE OF CRITICAL PR RISKS ---")
print(df[df['priority'] == 'CRITICAL'][['raw_text', 'priority']].head())
