# Support Triage Engine

**Rule-based AI classification pipeline for high-volume enterprise support**

---

## [ 01. THE PROBLEM ]

Enterprise support teams operating at scale face the same structural failure: every ticket enters the same queue regardless of urgency. A billing threat destined for Legal sits next to a password reset. A churn signal from a $50K account waits behind a product question.

Manual triage at volume is slow, inconsistent, and expensive. This engine automates it.

---

## [ 02. WHAT IT DOES ]

A two-stage Python pipeline that ingests raw support ticket text, classifies each ticket by category and sentiment, assigns a strategic priority, and outputs an actionable triage report.

**Input:** 1,000 synthetic enterprise support tickets across 7 categories

**Output:**
- `triaged_tickets_report.csv` -- every ticket with detected category, sentiment score, and priority
- `outputs/triage_analysis.png` -- three-panel visual summary of pipeline performance

**Categories detected:** PR Risk, Technical Bug, Churn Risk, Sales, Access Issue, Product Question, Praise

**Priority levels:** CRITICAL, High, Medium, Normal

---

## [ 03. PIPELINE ARCHITECTURE ]
