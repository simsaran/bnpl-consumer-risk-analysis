# The BNPL Trap
### Canadian Buy Now Pay Later Consumer Risk Analysis

Buy Now Pay Later is on every checkout page now. Shein, Temu, even grocery apps. You can split a $40 order into four payments and it barely registers as a financial decision. I started wondering what that looks like when you map it out across a full year for different types of buyers.

For most people it is fine. They use it occasionally and pay it off without issue. But for a meaningful group the picture is very different. Not because they are irresponsible but because no platform shows them what they have already committed to before they start a new plan.

---

## What this is

A consumer risk analysis of Canadian Buy Now Pay Later usage across 800 synthetic consumers and 4,879 transactions. Three segments modelled across five platforms. A missed payment analysis. An awareness gap study showing how many High Exposure users know what they owe across all their active plans at once. Ten requirements written for what responsible BNPL design actually looks like.

---

## Live app

[Launch the BNPL Consumer Risk Dashboard](https://bnpl-consumer-risk-analysis-2026.streamlit.app/)

---

## What the data showed

22% of consumers are High Exposure users — running an average of 5.5 simultaneous BNPL plans at once. Their average monthly commitment across all active plans is $395. Only 30.6% of them know what that total is. Their missed payment rate is 28%, nearly ten times higher than Occasional Users at 3%.

Fast fashion — Shein, Temu, and ASOS — is the most common BNPL category. A $58 order split into four $14.50 payments does not feel like a credit decision. That psychological effect compounds across multiple simultaneous plans until a payment is missed and a late fee appears without warning.

| Segment | Size | Avg Monthly Commitment | Awareness of Total | Missed Payment Rate |
|---------|------|----------------------|-------------------|---------------------|
| Occasional User | 40% | Low | 88% | 3% |
| Regular User | 38% | Moderate | 61% | 11% |
| High Exposure User | 22% | $395 | 30.6% | 28% |

---

## What the five tabs cover

The Invisible Debt tab shows the monthly transaction volume, simultaneous plan comparison by segment, and BNPL usage broken down by product category.

Who Is Using It shows the three-segment breakdown, the awareness of total commitment comparison, and the full segment metrics table.

The Risk Picture shows the missed payment rate by segment, the scatter plot of monthly commitment versus awareness showing the inverse relationship, and the distribution of monthly commitment across all consumers.

What Responsible Design Looks Like shows the full requirements register with priority, why each requirement matters, and which platforms currently meet it.

The Business Case covers the regulatory gap, who the stakeholders are, and the fintech opportunity in building responsible features before regulation requires them.

---

## Files in this repo

| File | What it is |
|------|-----------|
| app.py | Streamlit consumer risk dashboard |
| consumer-data.csv | 800 consumers with segment, commitment, awareness, and missed payment data |
| transaction-data.csv | 4,879 BNPL transactions across 5 platforms and 6 categories |
| segment-summary.csv | Aggregated segment metrics |
| category-analysis.csv | BNPL usage and missed payment rates by product category |
| monthly-trend.csv | Monthly transaction volume and missed payment rate trend |
| requirements-register.csv | 10 requirements for responsible BNPL design |
| key-findings.json | Headline findings |
| ba-report.pdf | Full business analysis report |
| generate-data.py | Python script that built all data files |
| requirements.txt | Package dependencies |

---

## Skills this project demonstrates

Consumer behaviour segmentation. Financial risk modelling. Awareness gap analysis. Requirements elicitation with MoSCoW prioritisation. Regulatory gap analysis. Business case development. Python for data generation and analysis. Streamlit dashboard design and deployment. Fintech and consumer credit domain knowledge.

---

## About this project

Part of a portfolio series built while job searching in Canada after graduating from the University of Waterloo.

Prepared by Simran Saran. Targeting business analyst, product analyst, and fintech roles across Canada.

All data is synthetic. Platform information based on publicly available BNPL product details as of May 2026.
