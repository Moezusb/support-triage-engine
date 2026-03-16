"""
triage_engine.py
================
Classifies support tickets by category, sentiment, and priority.
Outputs a triaged report CSV and a full accuracy + performance summary.

Author : Mohamed Bah
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("raw_support_tickets.csv")

# ─────────────────────────────────────────────
# CLASSIFICATION ENGINE
# ─────────────────────────────────────────────

def classify_ticket(text: str) -> tuple:
    t = text.lower()

    # ── PRAISE first -- prevent positive tickets misclassifying ──
    if any(w in t for w in ["great job", "phenomenal", "above and beyond",
                             "thank you", "fastest", "onboarding specialist",
                             "doing a great job"]):
        return "Praise", 5, "Normal"

    # ── SALES second -- revenue signals before escalation logic ──
    if any(w in t for w in ["enterprise", "quote", "seats", "upgrade",
                             "annual contract", "budget approval", "non-profit",
                             "discount", "compliance features", "move from",
                             "ready to move", "add 50", "walk us through"]):
        return "Sales", 3, "High"

    # ── PR Risk ──
    if any(w in t for w in ["legal", "social media", "sue", "damages", "regulator",
                             "formal complaint", "public review", "board", "executive response",
                             "filing", "contract", "seeking", "taking this to"]):
        return "PR Risk", 1, "CRITICAL"

    # ── Technical Bug ──
    if any(w in t for w in ["vulnerability", "security", "crash", "api", "500",
                             "error", "broken", "fail", "not syncing",
                             "webhook", "special characters", "sso", "login portal"]):
        sentiment = 2 if any(w in t for w in ["infuriating", "again", "third",
                                               "entire organization", "down"]) else 3
        priority  = "High" if sentiment <= 2 else "Medium"
        return "Technical Bug", sentiment, priority

    # ── Churn Risk ──
    if any(w in t for w in ["competitor", "not sure we will renew", "evaluating other",
                             "hard to justify", "contract is up", "stopped using",
                             "re-evaluating", "roadmap", "looking at competitors"]):
        return "Churn Risk", 2, "High"

    # ── Access Issue ──
    if any(w in t for w in ["password", "reset", "locked", "invitation",
                             "log in", "two-factor", "2fa", "access"]):
        return "Access Issue", 2, "Medium"

    # ── Product Question ──
    if any(w in t for w in ["how do i", "does the", "is it possible", "can i",
                             "what is", "maximum", "schedule", "saml", "okta",
                             "export", "permissions", "roles", "find the button"]):
        return "Product Question", 3, "Normal"

    return "General", 3, "Normal"

    # ── PRIORITY LOGIC ──
    if category == "PR Risk":
        priority = "CRITICAL"

    elif category == "Technical Bug":
        priority = "High" if sentiment <= 2 else "Medium"

    elif category == "Churn Risk":
        priority = "High"

    elif category == "Sales":
        priority = "High"

    elif category == "Access Issue":
        priority = "Medium"

    else:
        priority = "Normal"

    return category, sentiment, priority


# ── APPLY CLASSIFICATION ──
results = df["raw_text"].apply(lambda t: pd.Series(
    classify_ticket(t),
    index=["detected_category", "sentiment_score", "priority"]
))

df = pd.concat([df, results], axis=1)
df.to_csv("triaged_tickets_report.csv", index=False)

# ─────────────────────────────────────────────
# ACCURACY REPORT
# ─────────────────────────────────────────────

correct   = (df["detected_category"] == df["actual_category"]).sum()
total     = len(df)
accuracy  = correct / total * 100

print("=" * 55)
print("  AI TRIAGE ENGINE -- PERFORMANCE REPORT")
print("=" * 55)
print(f"\n  Tickets processed : {total}")
print(f"  Correctly labelled: {correct}")
print(f"  Overall accuracy  : {accuracy:.1f}%")

print(f"\n  Priority breakdown:")
for pri, count in df["priority"].value_counts().items():
    print(f"    {pri:<12} {count}")

print(f"\n  Accuracy by category:")
for cat in df["actual_category"].unique():
    subset   = df[df["actual_category"] == cat]
    cat_acc  = (subset["detected_category"] == subset["actual_category"]).mean() * 100
    print(f"    {cat:<22} {cat_acc:.0f}%")

print(f"\n  Critical PR Risks isolated: {(df['priority'] == 'CRITICAL').sum()}")
print(f"  High-priority items flagged: {(df['priority'] == 'High').sum()}")

# ─────────────────────────────────────────────
# VISUALISATIONS
# ─────────────────────────────────────────────

forest      = "#003314"
forest_mid  = "#6b9e7e"
forest_pale = "#d4e6da"
stone       = "#f0efec"

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("AI Support Triage Engine -- 1,000 Ticket Analysis",
             fontsize=13, fontweight="bold", y=1.02)

# Chart 1: Priority breakdown
pri_counts = df["priority"].value_counts().reindex(
    ["CRITICAL", "High", "Medium", "Normal"], fill_value=0
)
colors1 = [forest, forest_mid, forest_pale, stone]
axes[0].bar(pri_counts.index, pri_counts.values, color=colors1, edgecolor="white", linewidth=0.5)
axes[0].set_title("Tickets by Priority", fontsize=11, fontweight="bold")
axes[0].set_ylabel("Count")
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)
for i, (_, v) in enumerate(pri_counts.items()):
    if v > 0:
        axes[0].text(i, v + 5, str(v), ha="center", fontsize=10,
                     fontweight="bold", color=forest)

# Chart 2: Category breakdown
cat_counts = df["detected_category"].value_counts()
axes[1].barh(cat_counts.index, cat_counts.values, color=forest, height=0.6)
axes[1].set_title("Tickets by Category", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Count")
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
for i, v in enumerate(cat_counts.values):
    axes[1].text(v + 3, i, str(v), va="center", fontsize=9,
                 fontweight="bold", color=forest)

# Chart 3: Accuracy by category
cat_accuracy = {}
for cat in df["actual_category"].unique():
    subset = df[df["actual_category"] == cat]
    cat_accuracy[cat] = (subset["detected_category"] == subset["actual_category"]).mean() * 100

acc_series = pd.Series(cat_accuracy).sort_values()
bar_colors = [forest if v == 100 else forest_mid if v >= 80 else forest_pale
              for v in acc_series.values]
axes[2].barh(acc_series.index, acc_series.values, color=bar_colors, height=0.6)
axes[2].set_title("Detection Accuracy by Category", fontsize=11, fontweight="bold")
axes[2].set_xlabel("Accuracy (%)")
axes[2].set_xlim(0, 115)
axes[2].axvline(x=80, color=forest, linewidth=1, linestyle="--", alpha=0.4)
axes[2].spines["top"].set_visible(False)
axes[2].spines["right"].set_visible(False)
for i, v in enumerate(acc_series.values):
    axes[2].text(v + 1, i, f"{v:.0f}%", va="center", fontsize=9,
                 fontweight="bold", color=forest)

plt.tight_layout()
plt.savefig("outputs/triage_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"\n  Chart saved: outputs/triage_analysis.png")
print("=" * 55)
