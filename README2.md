# Support Triage Engine

**Rule-based risk scoring and routing for enterprise B2B SaaS support operations.**

---

## [ 01. THE PROBLEM ]

Every enterprise support team eventually builds the same broken architecture: one general queue, manual ticket picking, and priority labels that carry no operational consequence. A cancellation request from a $50K ARR account waits behind a password reset. An after-hours SSO outage sits until morning. Agents open four systems to answer one question.

The result is visible in the metrics: enterprise accounts churn at 2–4x the rate of SMB accounts, and support responsiveness is the most cited cancellation reason. The fix is not more agents — it is routing intelligence applied at intake.

This engine does that deterministically.

---

## [ 02. WHAT IT DOES ]

A two-part system: a **Python classification pipeline** for batch processing, and an **interactive HTML scorer** for live triage and evaluation.

**Input signals scored at ticket intake:**

| Signal | Points |
|---|---|
| Enterprise account (100+ seats / $50K+ ARR) | +50 |
| SSO failure / workspace unavailable / multiple users blocked | +40 |
| Cancellation, downgrade, billing dispute, or overcharge | +35 |
| Renewal within 90 days | +30 |
| Repeat complaint from same account within 7 days | +25 |
| Magic import quality failure from enterprise account | +25 |
| Enterprise onboarding or implementation blocker | +20 |
| After-hours ticket | +15 |
| Churn language or executive / CEO mention | +10 |
| Known retryable issue with self-serve path available | −20 |
| Trial or free-tier account, low severity | −10 |

**Output per ticket:**
- Risk score (0–150+)
- Routing lane (P0 through P4)
- SLA target
- Ownership assignment
- One-line routing rationale

**Routing lanes:**

| Lane | Threshold | SLA |
|---|---|---|
| P0 — Enterprise access outage | Score ≥ 90 | 3 min (biz hrs) / 20 min (after-hours) |
| P1 — Commercial risk | Score ≥ 70, commercial category | ACK 10 min / CS task 30 min |
| P1 — Product trust risk | Score ≥ 55, quality category | 15 min + proactive update |
| P2 — Enterprise standard | Score ≥ 40 | 15 min |
| P2 — Implementation / integration | Score ≥ 30, onboarding/API | 15 min |
| P3 — Billing | Score ≥ 20, billing category | 20 min |
| P3 — Canvas technical | Score ≥ 10 | 10 min |
| P4 — General | Score < 10 | 30 min |

---

## [ 03. INTERACTIVE SCORER ]

**[→ Open the live risk scorer](https://moezusb.github.io/support-triage-engine/)**

Three tabs:

- **Risk scorer** — configure ticket inputs and watch the score, lane, SLA, and rationale update in real time
- **Sample tickets** — 12 pre-loaded tickets with current system vs. model comparison side-by-side
- **Score legend** — full weight table, lane definitions, and design rationale

The scorer is standalone HTML — no build step, no dependencies, no framework.

---

## [ 04. PYTHON PIPELINE ]

The batch pipeline ingests raw ticket exports and outputs a triaged report with score, lane, and routing rationale for every ticket.

```bash
pip install pandas matplotlib

python generate_tickets.py    # generates raw_support_tickets.csv (synthetic dataset)
python triage_engine.py       # runs scoring, outputs triaged_tickets_report.csv + chart
```

No local setup required — runs directly in [Google Colab](https://colab.research.google.com) or GitHub Codespaces.

**Pipeline architecture:**

```
raw_support_tickets.csv
        │
        ▼
[ Stage 1: Signal extraction ]
  Account tier · Issue category · Renewal proximity
  Repeat complaint flag · After-hours flag
  Churn language · Executive mention · Retryable flag

        │
        ▼
[ Stage 2: Scoring engine ]
  Deterministic weight accumulation
  Score floor: 0 (no negative totals)
  Breakdown tracked per signal for auditability

        │
        ▼
[ Stage 3: Lane assignment ]
  Ordered conditional routing
  Category context applied before score threshold
  Commercial and quality lanes evaluated separately

        │
        ▼
[ Stage 4: Output ]
  triaged_tickets_report.csv — full scored dataset
  outputs/triage_analysis.png — three-panel summary
```

---

## [ 05. PERFORMANCE — v1 BASELINE ]

**Overall accuracy: 87.2%** across 1,000 synthetic tickets (v1 pipeline)

| Category | Accuracy | Priority |
|---|---|---|
| PR Risk | 88% | CRITICAL |
| Technical Bug | 87% | High / Medium |
| Churn Risk | 83% | High |
| Product Question | 81% | Normal |
| Access Issue | 70% | Medium |
| Praise | 100% | Normal |
| Sales | 100% | High |

v2 scoring model (this repo) applies enterprise account context and renewal proximity — signals absent in v1 — which materially changes the priority of access and commercial-risk tickets.

---

## [ 06. DESIGN DECISIONS ]

**Why deterministic instead of ML or LLM classification?**

Deterministic scores are auditable, explainable to agents, and tunable without retraining. An ops team can change a weight on Monday morning and see the effect on Tuesday's queue. An ML model cannot offer that. In production, the keyword layer can be replaced or augmented by an LLM classifier once the taxonomy, KB, and routing lanes are stable — the architecture is already structured for that swap.

**Why does classification order matter?**

Ticket category context is evaluated before score thresholds. A cancellation request routes to P1 Commercial Risk at score ≥ 35 — not P2 at score ≥ 40 — because the commercial consequence of misrouting a cancellation exceeds the cost of over-escalating it. Same logic applies to import quality vs. import error: retryable errors are deflection candidates; quality failures are product-trust risks. Conflating them is the most common failure in single-queue support architectures.

**Why not lead with AI?**

AI triage requires a stable taxonomy, a reliable knowledge base, and a functioning routing architecture to classify into. Automating into a broken taxonomy amplifies broken signals. Deterministic routing handles the high-confidence patterns (90%+ of volume) while an LLM call can handle genuinely ambiguous tickets at the margin. That evaluation belongs at Month 3, not Day 1.

**On score weights and tuning:**

The weights in this model were calibrated against a 30-ticket enterprise support sample. They should be reviewed weekly against false-positive and false-negative routing outcomes for the first two weeks post-deployment, then monthly. The score is not meant to be mathematically precise — it is meant to make risk visible, auditable, and adjustable by the ops team without an engineering ticket.

---

## [ 07. WHAT I WOULD BUILD NEXT ]

- **Zendesk trigger integration** — implement the scoring logic as a native Zendesk trigger on existing custom fields: no Lambda required, no maintenance debt, zero incremental cost
- **Salesforce enrichment** — pull ARR band, renewal date, and account owner at ticket creation via native Zendesk–Salesforce integration; feeds the enterprise and renewal signals automatically
- **LLM edge-case handler** — route the ~10–15% of tickets that are ambiguous for the rule-based classifier to a lightweight Claude API call (~$0.003/call); handles free-text churn language detection and multi-signal edge cases
- **Feedback loop** — log false positives and false negatives from weekly routing audits back into the weight table; lightweight continuous improvement without a data science team
- **Real-time webhook** — connect to Zendesk or Intercom via webhook so tickets are scored at creation, not in batch

---

## [ 08. REPOSITORY STRUCTURE ]

```
support-triage-engine/
├── index.html                    # Interactive risk scorer (GitHub Pages)
├── triage_engine.py              # Python scoring pipeline
├── generate_tickets.py           # Synthetic dataset generator
├── raw_support_tickets.csv       # v1 synthetic ticket dataset
├── triaged_tickets_report.csv    # v1 scored output
├── outputs/
│   └── triage_analysis.png       # v1 pipeline performance chart
└── README.md
```

---

**Status:** Active  
**Stack:** Python · Pandas · Matplotlib · Vanilla HTML/JS  
**Author:** Mohamed Bah &nbsp;|&nbsp; [LinkedIn](https://www.linkedin.com/in/bah-007700/) &nbsp;|&nbsp; [Portfolio](https://moezusb.github.io)
