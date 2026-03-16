"""
generate_tickets.py
===================
Generates a realistic synthetic dataset of 1,000 enterprise support tickets
across 7 categories. Uses a fixed random seed for reproducibility.

Author : Mohamed Bah
"""

import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────────
# SCENARIO BANK
# 40 distinct scenarios across 7 categories
# ─────────────────────────────────────────────

SCENARIOS = [
    # PR Risk (8)
    {"text": "Refunding this now or I am taking this to social media. Charged twice!", "category": "PR Risk"},
    {"text": "Our legal team is reviewing our contract due to this ongoing service outage.", "category": "PR Risk"},
    {"text": "I am posting a public review about this experience unless resolved today.", "category": "PR Risk"},
    {"text": "This is the third billing error this quarter. I am escalating to my board.", "category": "PR Risk"},
    {"text": "Your service caused us to miss a client deadline. We are seeking damages.", "category": "PR Risk"},
    {"text": "I will be filing a formal complaint with the regulator if this is not addressed.", "category": "PR Risk"},
    {"text": "We have documented every outage and are preparing a case against your SLA.", "category": "PR Risk"},
    {"text": "My CEO is cc'd on this email. We need an executive response today.", "category": "PR Risk"},

    # Technical Bug (8)
    {"text": "I think I found a security vulnerability in your login portal.", "category": "Technical Bug"},
    {"text": "The app crashed again while I was mid-presentation. Infuriating.", "category": "Technical Bug"},
    {"text": "API returning 500 errors on every POST request since this morning.", "category": "Technical Bug"},
    {"text": "The export function silently fails -- no error message, no file.", "category": "Technical Bug"},
    {"text": "SSO login is broken for our entire organization since the last update.", "category": "Technical Bug"},
    {"text": "Data is not syncing between the mobile app and the web dashboard.", "category": "Technical Bug"},
    {"text": "Webhook events stopped firing three hours ago. Our automation is down.", "category": "Technical Bug"},
    {"text": "The search function returns incorrect results for any query with special characters.", "category": "Technical Bug"},

    # Churn Risk (6)
    {"text": "Looking at competitors because your uptime has been terrible lately.", "category": "Churn Risk"},
    {"text": "We are evaluating other vendors. Your pricing has become hard to justify.", "category": "Churn Risk"},
    {"text": "Our contract is up in 60 days and we are not sure we will renew.", "category": "Churn Risk"},
    {"text": "Three of our team members have stopped using the platform entirely.", "category": "Churn Risk"},
    {"text": "We expected the roadmap feature by Q2. It is now Q4 and nothing has shipped.", "category": "Churn Risk"},
    {"text": "Executive sponsor has left the company and the new one is re-evaluating all tools.", "category": "Churn Risk"},

    # Sales (5)
    {"text": "We are ready to move from the Free plan to Enterprise. Please send a quote.", "category": "Sales"},
    {"text": "Is there a discount available for non-profit organizations?", "category": "Sales"},
    {"text": "We want to add 50 more seats to our current plan. Who should I talk to?", "category": "Sales"},
    {"text": "Can you walk us through the Enterprise security and compliance features?", "category": "Sales"},
    {"text": "We have a budget approval for an annual contract. What are the next steps?", "category": "Sales"},

    # Product Question (5)
    {"text": "How do I export my data to a CSV? I cannot find the button.", "category": "Product Question"},
    {"text": "Is it possible to set up custom roles and permissions for our team?", "category": "Product Question"},
    {"text": "Does the platform support SAML-based SSO with Okta?", "category": "Product Question"},
    {"text": "Can I schedule automated reports to be sent to my team every Monday?", "category": "Product Question"},
    {"text": "What is the maximum file size for document uploads?", "category": "Product Question"},

    # Access Issue (4)
    {"text": "The password reset link expired before I could use it. Please resend.", "category": "Access Issue"},
    {"text": "I cannot log in after your maintenance window ended. Account appears locked.", "category": "Access Issue"},
    {"text": "New team member has not received the invitation email after 24 hours.", "category": "Access Issue"},
    {"text": "Two-factor authentication is failing for three members of my team.", "category": "Access Issue"},

    # Praise (4)
    {"text": "Just wanted to say the support team is doing a phenomenal job.", "category": "Praise"},
    {"text": "The new dashboard update is exactly what we asked for. Thank you.", "category": "Praise"},
    {"text": "Your onboarding specialist went above and beyond for our team.", "category": "Praise"},
    {"text": "Fastest support response I have ever received from any SaaS vendor.", "category": "Praise"},
]

URGENCY_MODIFIERS = [
    "",
    " This is urgent.",
    " ASAP please.",
    " We need this resolved today.",
    " This is blocking our team.",
    " This is our third time contacting support about this.",
    " Our entire team is affected.",
    "",  # weighted toward no modifier
    "",
    "",
]

CUSTOMER_TIERS = ["SMB", "Mid-Market", "Enterprise"]
TIER_WEIGHTS   = [0.45, 0.38, 0.17]

# ─────────────────────────────────────────────
# GENERATE DATASET
# ─────────────────────────────────────────────

records = []
for i in range(1000):
    scenario  = random.choice(SCENARIOS)
    modifier  = random.choice(URGENCY_MODIFIERS)
    tier      = random.choices(CUSTOMER_TIERS, weights=TIER_WEIGHTS, k=1)[0]

    records.append({
        "ticket_id":       f"REQ-{5000 + i}",
        "customer_tier":   tier,
        "raw_text":        scenario["text"] + modifier,
        "actual_category": scenario["category"],
    })

df = pd.DataFrame(records)
df.to_csv("raw_support_tickets.csv", index=False)

print("Ticket generation complete.")
print(f"  Total tickets : {len(df)}")
print(f"\n  Category breakdown:")
for cat, count in df["actual_category"].value_counts().items():
    print(f"    {cat:<20} {count}")
print(f"\n  Tier breakdown:")
for tier, count in df["customer_tier"].value_counts().items():
    print(f"    {tier:<15} {count}")
