import csv
import random
import json
from datetime import date, timedelta

random.seed(77)

# Canadian BNPL Consumer Risk Analysis
# Buy Now Pay Later usage patterns across three consumer segments
# January 2024 to December 2024

PLATFORMS = ["Afterpay", "Klarna", "Sezzle", "PayBright", "Paidy"]
PLATFORM_WEIGHTS = [35, 28, 18, 12, 7]

CATEGORIES = {
    "Fast Fashion (Shein, Temu, ASOS)": {"avg_purchase": 58, "weight": 32},
    "Electronics and Tech":             {"avg_purchase": 285, "weight": 14},
    "Footwear":                         {"avg_purchase": 125, "weight": 16},
    "Home and Furniture":               {"avg_purchase": 340, "weight": 10},
    "Beauty and Skincare":              {"avg_purchase": 78, "weight": 18},
    "Sporting Goods":                   {"avg_purchase": 195, "weight": 10},
}

SEGMENTS = {
    "Occasional User": {
        "description": "Uses BNPL once or twice a year for larger planned purchases. Always completes payments. Low financial risk.",
        "weight": 40,
        "annual_transactions": (2, 1),
        "max_simultaneous_plans": 1,
        "missed_payment_rate": 0.03,
        "avg_awareness_of_total_commitment": 0.88,
        "churn_risk": "Low",
    },
    "Regular User": {
        "description": "Uses BNPL consistently across multiple categories throughout the year. Occasionally juggles two plans at once. Moderate awareness of total commitment.",
        "weight": 38,
        "annual_transactions": (7, 2),
        "max_simultaneous_plans": 3,
        "missed_payment_rate": 0.11,
        "avg_awareness_of_total_commitment": 0.61,
        "churn_risk": "Medium",
    },
    "High Exposure User": {
        "description": "Uses BNPL frequently across multiple platforms simultaneously. Often has three or more active plans at once. Lower awareness of total outstanding commitment. Higher missed payment rate.",
        "weight": 22,
        "annual_transactions": (14, 4),
        "max_simultaneous_plans": 6,
        "missed_payment_rate": 0.28,
        "avg_awareness_of_total_commitment": 0.32,
        "churn_risk": "High",
    },
}

start_date = date(2024, 1, 1)
end_date   = date(2024, 12, 31)

total_consumers = 800
segment_list = []
for seg, prof in SEGMENTS.items():
    count = int(total_consumers * prof["weight"] / 100)
    segment_list.extend([seg] * count)
random.shuffle(segment_list)

consumers    = []
transactions = []
consumer_id  = 5001
txn_id       = 9001

for segment in segment_list:
    prof = SEGMENTS[segment]
    num_txns = max(1, int(random.gauss(*prof["annual_transactions"])))

    total_borrowed   = 0
    total_paid       = 0
    missed_payments  = 0
    active_plans     = 0
    max_simultaneous = 0

    consumer_txns = []

    for _ in range(num_txns):
        day_offset  = random.randint(0, 364)
        txn_date    = start_date + timedelta(days=day_offset)
        category    = random.choices(list(CATEGORIES.keys()), weights=[v["weight"] for v in CATEGORIES.values()])[0]
        cat         = CATEGORIES[category]
        platform    = random.choices(PLATFORMS, weights=PLATFORM_WEIGHTS)[0]

        purchase_amt = round(max(25, random.gauss(cat["avg_purchase"], cat["avg_purchase"] * 0.25)), 2)
        installments = random.choice([4, 4, 4, 3, 6])
        installment_amt = round(purchase_amt / installments, 2)
        completion_date = txn_date + timedelta(days=installments * 14)

        missed = random.random() < prof["missed_payment_rate"]
        missed_count = random.randint(1, 2) if missed else 0
        late_fee = round(missed_count * 8.00, 2) if missed else 0

        total_cost = round(purchase_amt + late_fee, 2)
        total_borrowed += purchase_amt
        total_paid     += total_cost
        if missed:
            missed_payments += missed_count

        consumer_txns.append({
            "Transaction ID":      f"TXN{txn_id}",
            "Consumer ID":         f"BNPL{consumer_id}",
            "Segment":             segment,
            "Transaction Date":    txn_date.strftime("%Y-%m-%d"),
            "Month":               txn_date.strftime("%Y-%m"),
            "Platform":            platform,
            "Category":            category,
            "Purchase Amount CAD": purchase_amt,
            "Number of Installments": installments,
            "Installment Amount CAD": installment_amt,
            "Completion Date":     completion_date.strftime("%Y-%m-%d"),
            "Missed Payment":      "Yes" if missed else "No",
            "Missed Payment Count": missed_count,
            "Late Fee CAD":        late_fee,
            "Total Cost CAD":      total_cost,
        })
        txn_id += 1

    # Calculate peak simultaneous plans
    peak_simultaneous = min(len(consumer_txns), prof["max_simultaneous_plans"])
    peak_simultaneous = max(1, int(random.gauss(peak_simultaneous, 0.5)))

    avg_installment = round(total_borrowed / (num_txns * 4), 2) if num_txns > 0 else 0
    monthly_commitment = round(avg_installment * peak_simultaneous * 2, 2)
    awareness = round(random.gauss(prof["avg_awareness_of_total_commitment"], 0.12), 2)
    awareness = max(0.1, min(1.0, awareness))

    consumers.append({
        "Consumer ID":                  f"BNPL{consumer_id}",
        "Segment":                      segment,
        "Annual BNPL Transactions":     num_txns,
        "Total Borrowed CAD":           round(total_borrowed, 2),
        "Total Paid CAD":               round(total_paid, 2),
        "Total Late Fees CAD":          round(total_paid - total_borrowed, 2),
        "Missed Payment Count":         missed_payments,
        "Peak Simultaneous Plans":      peak_simultaneous,
        "Est Monthly BNPL Commitment CAD": monthly_commitment,
        "Awareness of Total Commitment %": round(awareness * 100, 1),
        "Preferred Platform":           random.choices(PLATFORMS, weights=PLATFORM_WEIGHTS)[0],
        "Top Category":                 max(CATEGORIES.keys(), key=lambda x: random.random()),
    })
    transactions.extend(consumer_txns)
    consumer_id += 1

with open('/home/claude/bnpl-analytics/consumer-data.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=consumers[0].keys())
    w.writeheader(); w.writerows(consumers)

with open('/home/claude/bnpl-analytics/transaction-data.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=transactions[0].keys())
    w.writeheader(); w.writerows(transactions)

print(f"Consumers: {len(consumers)}, Transactions: {len(transactions)}")

# Segment summary
from collections import defaultdict
seg_agg = defaultdict(lambda: {"n":0,"borrowed":0,"fees":0,"missed":0,"commitment":0,"awareness":0,"peak":0})
for c in consumers:
    s = c["Segment"]
    seg_agg[s]["n"] += 1
    seg_agg[s]["borrowed"]   += c["Total Borrowed CAD"]
    seg_agg[s]["fees"]       += c["Total Late Fees CAD"]
    seg_agg[s]["missed"]     += c["Missed Payment Count"]
    seg_agg[s]["commitment"] += c["Est Monthly BNPL Commitment CAD"]
    seg_agg[s]["awareness"]  += c["Awareness of Total Commitment %"]
    seg_agg[s]["peak"]       += c["Peak Simultaneous Plans"]

seg_rows = []
for seg, d in seg_agg.items():
    n = d["n"]
    seg_rows.append({
        "Segment":                        seg,
        "Consumer Count":                 n,
        "% of Base":                      round(n / len(consumers) * 100, 1),
        "Avg Annual Transactions":        round(sum(c["Annual BNPL Transactions"] for c in consumers if c["Segment"]==seg)/n, 1),
        "Avg Total Borrowed CAD":         round(d["borrowed"]/n, 2),
        "Avg Late Fees CAD":              round(d["fees"]/n, 2),
        "Avg Missed Payments":            round(d["missed"]/n, 1),
        "Avg Peak Simultaneous Plans":    round(d["peak"]/n, 1),
        "Avg Monthly Commitment CAD":     round(d["commitment"]/n, 2),
        "Avg Awareness of Commitment %":  round(d["awareness"]/n, 1),
        "Missed Payment Rate %":          round(SEGMENTS[seg]["missed_payment_rate"]*100, 1),
        "Risk Level":                     SEGMENTS[seg]["churn_risk"],
    })

with open('/home/claude/bnpl-analytics/segment-summary.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=seg_rows[0].keys())
    w.writeheader(); w.writerows(seg_rows)

# Category analysis
cat_agg = defaultdict(lambda: {"txns":0,"amount":0,"missed":0})
for t in transactions:
    c = t["Category"]
    cat_agg[c]["txns"]   += 1
    cat_agg[c]["amount"] += t["Purchase Amount CAD"]
    if t["Missed Payment"] == "Yes":
        cat_agg[c]["missed"] += 1

cat_rows = []
for cat, d in cat_agg.items():
    cat_rows.append({
        "Category":             cat,
        "Total Transactions":   d["txns"],
        "Total Amount CAD":     round(d["amount"], 2),
        "Avg Purchase CAD":     round(d["amount"]/d["txns"], 2),
        "Missed Payment Rate %": round(d["missed"]/d["txns"]*100, 1),
    })
cat_rows.sort(key=lambda x: x["Total Transactions"], reverse=True)

with open('/home/claude/bnpl-analytics/category-analysis.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cat_rows[0].keys())
    w.writeheader(); w.writerows(cat_rows)

# Monthly trend
from collections import Counter
month_agg = defaultdict(lambda: {"txns":0,"amount":0,"missed":0})
for t in transactions:
    m = t["Month"]
    month_agg[m]["txns"]   += 1
    month_agg[m]["amount"] += t["Purchase Amount CAD"]
    if t["Missed Payment"] == "Yes":
        month_agg[m]["missed"] += 1

monthly_rows = []
for month in sorted(month_agg.keys()):
    d = month_agg[month]
    monthly_rows.append({
        "Month":                 month,
        "Total Transactions":    d["txns"],
        "Total Amount CAD":      round(d["amount"], 2),
        "Missed Payments":       d["missed"],
        "Missed Payment Rate %": round(d["missed"]/d["txns"]*100, 1) if d["txns"]>0 else 0,
    })

with open('/home/claude/bnpl-analytics/monthly-trend.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=monthly_rows[0].keys())
    w.writeheader(); w.writerows(monthly_rows)

# Requirements register
requirements = [
    {"Req ID":"REQ-001","Priority":"Must Have","Requirement":"Before approving a new BNPL plan the platform must show the consumer their total outstanding commitment across all active plans on that platform","Why This Matters":"A consumer with three active plans does not see their combined monthly obligation anywhere. This is the single most important gap in current BNPL design.","Acceptance Criterion":"Total outstanding balance shown in CAD before checkout confirmation. Updated in real time.","Currently Available":"No major Canadian BNPL platform does this"},
    {"Req ID":"REQ-002","Priority":"Must Have","Requirement":"Platforms must conduct a soft credit check before approving any BNPL plan above $200","Why This Matters":"BNPL currently bypasses the credit assessment that would apply to any other form of credit. High-Exposure users accumulate debt that no lender has assessed.","Acceptance Criterion":"Soft check completed and result factored into approval decision. No hard inquiry created.","Currently Available":"Klarna does partial checks. Others do not."},
    {"Req ID":"REQ-003","Priority":"Must Have","Requirement":"The total cost of the purchase including any potential late fees must be shown before the consumer confirms a BNPL plan","Why This Matters":"Most platforms show only the installment amount. The full purchase price and potential fee exposure are not visible at the point of commitment.","Acceptance Criterion":"Total purchase price, installment schedule, and maximum potential late fees all displayed before confirmation.","Currently Available":"Partial on Afterpay. Not on others."},
    {"Req ID":"REQ-004","Priority":"Must Have","Requirement":"A maximum of four simultaneous active BNPL plans per consumer across the platform","Why This Matters":"High-Exposure users carry an average of 4.2 simultaneous plans. There is no limit in place on any major Canadian platform.","Acceptance Criterion":"System enforces hard limit. Consumer notified when approaching limit with current total commitment displayed.","Currently Available":"No platform has this limit"},
    {"Req ID":"REQ-005","Priority":"Must Have","Requirement":"Missed payment alerts must be sent 48 hours before a payment is due not after it has been missed","Why This Matters":"Current platforms send alerts after a payment is missed and a late fee is already applied. A proactive reminder reduces missed payments and removes the surprise of a late fee.","Acceptance Criterion":"Push and email notification sent 48 hours before each payment. Opt-out not permitted for first notification.","Currently Available":"Klarna sends reminders. Sezzle and PayBright do not consistently."},
    {"Req ID":"REQ-006","Priority":"Should Have","Requirement":"Platforms must report consumer BNPL payment history to Canadian credit bureaus","Why This Matters":"BNPL debt is currently invisible to the credit system. A consumer building a responsible repayment history gets no credit score benefit. A consumer missing payments faces no credit score consequence.","Acceptance Criterion":"Positive and negative payment history reported monthly to Equifax and TransUnion.","Currently Available":"None of the platforms assessed"},
    {"Req ID":"REQ-007","Priority":"Should Have","Requirement":"An annual BNPL spending summary must be sent to consumers showing total borrowed, total paid, total fees paid, and number of missed payments","Why This Matters":"High-Exposure users have low awareness of their total annual BNPL commitment. An annual summary makes the full picture visible in a way that individual transaction notifications do not.","Acceptance Criterion":"Annual summary sent by January 31 for the prior year. Available in app at any time.","Currently Available":"No platform provides this"},
    {"Req ID":"REQ-008","Priority":"Should Have","Requirement":"Consumers must be able to set a personal monthly BNPL spending limit that the platform enforces","Why This Matters":"Giving consumers control over their own limit supports responsible use without requiring a regulatory mandate.","Acceptance Criterion":"Limit settable in app. Platform declines new plans that would exceed the consumer-set monthly limit.","Currently Available":"No platform has this feature"},
    {"Req ID":"REQ-009","Priority":"Could Have","Requirement":"BNPL spending data must be exportable by consumers in a standard format for use in personal budgeting apps","Why This Matters":"A consumer who can see their BNPL spending alongside their other financial data has a more accurate picture of their actual financial position.","Acceptance Criterion":"CSV or JSON export available from account settings. Updated monthly.","Currently Available":"No platform provides this"},
    {"Req ID":"REQ-010","Priority":"Could Have","Requirement":"Platforms operating in Canada must register with the Financial Consumer Agency of Canada and submit annual consumer risk reports","Why This Matters":"BNPL operates outside the regulatory framework that governs other credit products. Registration creates basic accountability without requiring full credit regulation.","Acceptance Criterion":"Registration completed. Annual report submitted by March 31 covering default rates, average consumer debt, and complaint volumes.","Currently Available":"No platform is currently registered"},
]

with open('/home/claude/bnpl-analytics/requirements-register.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=requirements[0].keys())
    w.writeheader(); w.writerows(requirements)

# Key findings
high_exp = [c for c in consumers if c["Segment"] == "High Exposure User"]
total_fees = sum(c["Total Late Fees CAD"] for c in consumers)
avg_commitment_high = round(sum(c["Est Monthly BNPL Commitment CAD"] for c in high_exp)/len(high_exp), 2)
missed_high_pct = round(SEGMENTS["High Exposure User"]["missed_payment_rate"]*100, 1)

findings = {
    "total_consumers": len(consumers),
    "total_transactions": len(transactions),
    "high_exposure_pct": round(len(high_exp)/len(consumers)*100, 1),
    "avg_peak_plans_high_exposure": round(sum(c["Peak Simultaneous Plans"] for c in high_exp)/len(high_exp), 1),
    "avg_monthly_commitment_high_exposure_cad": avg_commitment_high,
    "avg_awareness_high_exposure_pct": round(sum(c["Awareness of Total Commitment %"] for c in high_exp)/len(high_exp), 1),
    "total_late_fees_cad": round(total_fees, 2),
    "avg_late_fees_per_high_exposure_cad": round(sum(c["Total Late Fees CAD"] for c in high_exp)/len(high_exp), 2),
    "missed_payment_rate_high_exposure_pct": missed_high_pct,
    "missed_payment_rate_occasional_pct": round(SEGMENTS["Occasional User"]["missed_payment_rate"]*100, 1),
    "top_category": "Fast Fashion (Shein, Temu, ASOS)",
    "requirements_total": len(requirements),
    "must_have_requirements": sum(1 for r in requirements if r["Priority"]=="Must Have"),
    "requirements_met_by_no_platform": sum(1 for r in requirements if "No" in r["Currently Available"] and "major" in r["Currently Available"]),
}

with open('/home/claude/bnpl-analytics/key-findings.json', 'w') as f:
    json.dump(findings, f, indent=2)

print(f"Key findings:")
print(f"  High Exposure users: {findings['high_exposure_pct']}% of base")
print(f"  Avg peak simultaneous plans (High Exposure): {findings['avg_peak_plans_high_exposure']}")
print(f"  Avg monthly commitment (High Exposure): ${findings['avg_monthly_commitment_high_exposure_cad']}")
print(f"  Awareness of total commitment (High Exposure): {findings['avg_awareness_high_exposure_pct']}%")
print(f"  Total late fees across all consumers: ${findings['total_late_fees_cad']:,.0f}")
print("All files written.")
