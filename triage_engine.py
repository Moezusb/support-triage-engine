import pandas as pd
import numpy as np
import random

# Expanded scenarios for a high-volume simulation
scenarios = [
    {"text": "Refunding this now or I am taking this to social media. Charged twice!", "type": "PR Risk"},
    {"text": "I think I found a security vulnerability in your login portal.", "type": "Technical Bug"},
    {"text": "Our legal team is reviewing our contract due to this service outage.", "type": "PR Risk"},
    {"text": "How do I export my data to a CSV? I can't find the button.", "type": "Product Question"},
    {"text": "We are ready to move from the Free plan to Enterprise. Send a quote.", "type": "Sales"},
    {"text": "The app crashed again while I was mid-presentation. Infuriating.", "type": "Technical Bug"},
    {"text": "Is there a discount for non-profit organizations?", "type": "Sales"},
    {"text": "Just wanted to say the support team is doing a great job!", "type": "Praise"},
    {"text": "The password reset link is expired. Help.", "type": "Access Issue"},
    {"text": "Looking at competitors because your uptime is terrible lately.", "type": "Churn Risk"}
]

data = []
for i in range(1000):
    s = random.choice(scenarios)
    # Add slight variation to the text to simulate real data
    variation = random.choice(["", " PLEASE HELP.", " ASAP!", " Thanks.", " (Urgently)"])
    data.append({
        "ticket_id": f"REQ-{5000+i}",
        "raw_text": s["text"] + variation,
        "actual_category": s["type"]
    })

df = pd.DataFrame(data)
df.to_csv('raw_support_tickets.csv', index=False)
print(f"✅ Generated {len(df)} raw support tickets.")
