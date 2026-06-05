import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

st.set_page_config(
    page_title="Canadian BNPL Consumer Risk Analysis",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .block-container{padding:1.5rem 2rem}
    .kpi{background:white;border-radius:12px;padding:16px 20px;border:1px solid #E8E8E8;box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px}
    .kpi-label{font-size:11px;color:#888;margin-bottom:4px;font-weight:500;text-transform:uppercase;letter-spacing:.04em}
    .kpi-value{font-size:26px;font-weight:700;color:#111;line-height:1.1}
    .kpi-note{font-size:11px;color:#888;margin-top:3px}
    .kpi-red .kpi-value{color:#C0392B}
    .kpi-green .kpi-value{color:#0A7540}
    .kpi-amber .kpi-value{color:#B7791F}
    .kpi-blue .kpi-value{color:#0C447C}
    .finding{background:#F0FBF6;border-left:3px solid #27AE60;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#1A5C35;margin:10px 0;line-height:1.6}
    .alert{background:#FDF2F2;border-left:3px solid #C0392B;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#7B1818;margin:10px 0;line-height:1.6}
    .warning{background:#FEF9EC;border-left:3px solid #F39C12;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#7D5A00;margin:10px 0;line-height:1.6}
    .insight{background:#EEF3FB;border-left:3px solid #1A56DB;border-radius:0 8px 8px 0;padding:11px 15px;font-size:13px;color:#0C2A6E;margin:10px 0;line-height:1.6}
    .section-title{font-size:15px;font-weight:600;color:#111;margin:18px 0 10px 0;padding-bottom:6px;border-bottom:1.5px solid #EBEBEB}
    footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    base = Path(__file__).parent
    consumers  = pd.read_csv(base / "consumer-data.csv")
    txns       = pd.read_csv(base / "transaction-data.csv")
    segments   = pd.read_csv(base / "segment-summary.csv")
    categories = pd.read_csv(base / "category-analysis.csv")
    monthly    = pd.read_csv(base / "monthly-trend.csv")
    reqs       = pd.read_csv(base / "requirements-register.csv")
    with open(base / "key-findings.json") as f:
        findings = json.load(f)
    return consumers, txns, segments, categories, monthly, reqs, findings

consumers, txns, segments, categories, monthly, reqs, findings = load()

SEG_COLORS = {
    "Occasional User":    "#0A7540",
    "Regular User":       "#4285F4",
    "High Exposure User": "#C0392B",
}

st.markdown("## Canadian BNPL Consumer Risk Analysis")
st.markdown("**800 consumers modelled** &nbsp;|&nbsp; **4,879 transactions** &nbsp;|&nbsp; **3 segments** &nbsp;|&nbsp; **5 platforms** &nbsp;|&nbsp; **January to December 2024**")
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  The Invisible Debt  ",
    "  Who Is Using It  ",
    "  The Risk Picture  ",
    "  What Responsible Design Looks Like  ",
    "  The Business Case  ",
])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">High Exposure users</div>
            <div class="kpi-value">{findings['high_exposure_pct']}%</div>
            <div class="kpi-note">Running 5+ simultaneous BNPL plans on average</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">Avg monthly commitment — High Exposure</div>
            <div class="kpi-value">${findings['avg_monthly_commitment_high_exposure_cad']:,.0f}</div>
            <div class="kpi-note">Across all active plans simultaneously</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="kpi kpi-amber">
            <div class="kpi-label">Awareness of total commitment</div>
            <div class="kpi-value">{findings['avg_awareness_high_exposure_pct']}%</div>
            <div class="kpi-note">High Exposure users who know their total</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">Total late fees generated</div>
            <div class="kpi-value">${findings['total_late_fees_cad']:,.0f}</div>
            <div class="kpi-note">Across all 800 consumers in 12 months</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    st.markdown(f'<div class="alert"><strong>The core problem:</strong> Buy Now Pay Later splits every purchase into small payments that individually feel manageable. A High Exposure user with 5 simultaneous plans is committing an average of ${findings["avg_monthly_commitment_high_exposure_cad"]:,.0f} per month in BNPL payments. Only {findings["avg_awareness_high_exposure_pct"]}% of them know what that total is. No platform shows it to them before they start a new plan.</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Monthly BNPL transaction volume and missed payment rate</div>', unsafe_allow_html=True)
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Bar(
            name="Total Transactions", x=monthly["Month"], y=monthly["Total Transactions"],
            marker_color="#94A3B8", opacity=0.7,
        ))
        fig_monthly.add_trace(go.Scatter(
            name="Missed Payment Rate %", x=monthly["Month"], y=monthly["Missed Payment Rate %"],
            yaxis="y2", line=dict(color="#C0392B", width=2), mode="lines+markers",
        ))
        fig_monthly.update_layout(
            height=320, plot_bgcolor="white",
            yaxis=dict(title="Transactions", gridcolor="#F1F1F1"),
            yaxis2=dict(title="Missed %", overlaying="y", side="right", ticksuffix="%"),
            xaxis=dict(title="", tickangle=45),
            legend=dict(orientation="h", y=1.1),
            margin=dict(t=10, b=60),
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Simultaneous active plans — how many plans does each segment juggle at once</div>', unsafe_allow_html=True)
        fig_plans = go.Figure(go.Bar(
            x=segments["Segment"],
            y=segments["Avg Peak Simultaneous Plans"],
            marker_color=[SEG_COLORS[s] for s in segments["Segment"]],
            text=[f"{v:.1f} plans" for v in segments["Avg Peak Simultaneous Plans"]],
            textposition="outside",
        ))
        fig_plans.update_layout(
            height=320, plot_bgcolor="white",
            yaxis=dict(title="Avg simultaneous plans", gridcolor="#F1F1F1"),
            xaxis=dict(title=""),
            margin=dict(t=10, b=20),
        )
        st.plotly_chart(fig_plans, use_container_width=True)

    st.markdown('<div class="section-title">BNPL by category — where Canadians are using Buy Now Pay Later most</div>', unsafe_allow_html=True)
    fig_cat = px.bar(
        categories.sort_values("Total Transactions", ascending=True),
        x="Total Transactions", y="Category", orientation="h",
        color="Missed Payment Rate %",
        color_continuous_scale=["#27AE60","#F59E0B","#C0392B"],
        text="Total Transactions",
    )
    fig_cat.update_traces(textposition="outside")
    fig_cat.update_layout(
        height=300, plot_bgcolor="white",
        xaxis=dict(title="Total transactions", gridcolor="#F1F1F1"),
        yaxis=dict(title=""),
        coloraxis_colorbar=dict(title="Missed %"),
        margin=dict(t=10, b=20),
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('<div class="insight">Fast fashion — primarily Shein, Temu, and ASOS — is the most common BNPL category. These are low-value, high-frequency purchases where the psychological effect of splitting a $58 order into four $14.50 payments is strongest. They are also the category where consumers are least likely to feel like they are taking on meaningful debt.</div>', unsafe_allow_html=True)

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Three types of BNPL users with very different risk profiles</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(segments, values="Consumer Count", names="Segment",
            color="Segment", color_discrete_map=SEG_COLORS, hole=0.45)
        fig_pie.update_layout(height=280, margin=dict(t=10,b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_awareness = go.Figure(go.Bar(
            x=segments["Segment"],
            y=segments["Avg Awareness of Commitment %"],
            marker_color=[SEG_COLORS[s] for s in segments["Segment"]],
            text=[f"{v}%" for v in segments["Avg Awareness of Commitment %"]],
            textposition="outside",
        ))
        fig_awareness.add_hline(y=50, line_dash="dot", line_color="#888",
            annotation_text="50% awareness threshold")
        fig_awareness.update_layout(
            height=280, plot_bgcolor="white",
            yaxis=dict(title="Avg awareness of total commitment %", gridcolor="#F1F1F1", range=[0,110], ticksuffix="%"),
            xaxis=dict(title=""),
            margin=dict(t=10,b=20),
        )
        st.plotly_chart(fig_awareness, use_container_width=True)

    st.markdown('<div class="section-title">Segment comparison — the full picture</div>', unsafe_allow_html=True)
    disp = segments[[
        "Segment","Consumer Count","% of Base","Avg Annual Transactions",
        "Avg Total Borrowed CAD","Avg Late Fees CAD","Avg Peak Simultaneous Plans",
        "Avg Monthly Commitment CAD","Avg Awareness of Commitment %","Missed Payment Rate %","Risk Level"
    ]].copy()
    for col in ["Avg Total Borrowed CAD","Avg Late Fees CAD","Avg Monthly Commitment CAD"]:
        disp[col] = disp[col].apply(lambda x: f"${x:,.2f}")
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ── TAB 3 ─────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Where the financial risk is concentrated</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert">High Exposure users make up 22% of the consumer base but generate the majority of late fees. Their missed payment rate is 28% — nearly ten times higher than Occasional Users at 3%. The problem is not that they are irresponsible. It is that no platform shows them what they have already committed to before they start a new plan.</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Missed payment rate by segment</div>', unsafe_allow_html=True)
        missed_data = pd.DataFrame({
            "Segment": ["Occasional User","Regular User","High Exposure User"],
            "Missed Payment Rate %": [
                findings["missed_payment_rate_occasional_pct"],
                11.0,
                findings["missed_payment_rate_high_exposure_pct"],
            ]
        })
        fig_missed = go.Figure(go.Bar(
            x=missed_data["Segment"], y=missed_data["Missed Payment Rate %"],
            marker_color=[SEG_COLORS[s] for s in missed_data["Segment"]],
            text=[f"{v}%" for v in missed_data["Missed Payment Rate %"]],
            textposition="outside",
        ))
        fig_missed.update_layout(
            height=300, plot_bgcolor="white",
            yaxis=dict(title="Missed payment rate %", gridcolor="#F1F1F1", ticksuffix="%"),
            xaxis=dict(title=""),
            margin=dict(t=10,b=20),
        )
        st.plotly_chart(fig_missed, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Monthly commitment vs awareness of commitment — High Exposure users</div>', unsafe_allow_html=True)
        high_exp = consumers[consumers["Segment"]=="High Exposure User"].sample(min(150, len(consumers[consumers["Segment"]=="High Exposure User"])), random_state=42)
        fig_scatter = px.scatter(
            high_exp,
            x="Awareness of Total Commitment %",
            y="Est Monthly BNPL Commitment CAD",
            color_discrete_sequence=["#C0392B"],
            opacity=0.6,
            trendline="ols",
        )
        fig_scatter.update_layout(
            height=300, plot_bgcolor="white",
            xaxis=dict(title="Awareness of total commitment %", gridcolor="#F1F1F1", ticksuffix="%"),
            yaxis=dict(title="Monthly BNPL commitment (CAD)", gridcolor="#F1F1F1", tickformat="$,.0f"),
            margin=dict(t=10,b=20),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("Higher monthly commitments correlate with lower consumer awareness — the more someone owes across plans the less likely they are to know the total.")

    st.markdown('<div class="section-title">Distribution of monthly BNPL commitment — High Exposure vs others</div>', unsafe_allow_html=True)
    fig_dist = px.histogram(
        consumers, x="Est Monthly BNPL Commitment CAD", color="Segment",
        barmode="overlay", opacity=0.7, nbins=40,
        color_discrete_map=SEG_COLORS,
    )
    fig_dist.update_layout(
        height=280, plot_bgcolor="white",
        xaxis=dict(title="Monthly BNPL commitment (CAD)", gridcolor="#F1F1F1", tickformat="$,.0f"),
        yaxis=dict(title="Number of consumers", gridcolor="#F1F1F1"),
        legend=dict(orientation="h", y=1.1),
        margin=dict(t=10,b=20),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# ── TAB 4 ─────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">What responsible BNPL design needs to include</div>', unsafe_allow_html=True)
    mh = len(reqs[reqs["Priority"]=="Must Have"])
    none_met = sum(1 for _, r in reqs.iterrows() if "No major" in str(r["Currently Available"]))

    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">Must Have requirements</div>
            <div class="kpi-value">{mh}</div>
            <div class="kpi-note">Minimum for responsible BNPL design</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="kpi kpi-red">
            <div class="kpi-label">Met by no major platform</div>
            <div class="kpi-value">{none_met} of {len(reqs)}</div>
            <div class="kpi-note">Requirements currently unimplemented</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="kpi kpi-blue">
            <div class="kpi-label">Single highest impact change</div>
            <div class="kpi-value" style="font-size:15px">Show total commitment</div>
            <div class="kpi-note">Before approving any new BNPL plan</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    priority_filter = st.multiselect(
        "Filter by priority",
        ["Must Have","Should Have","Could Have"],
        default=["Must Have","Should Have","Could Have"],
        key="req_filter"
    )
    filtered = reqs[reqs["Priority"].isin(priority_filter)]
    for _, req in filtered.iterrows():
        box_class = "alert" if req["Priority"]=="Must Have" else "warning" if req["Priority"]=="Should Have" else "insight"
        st.markdown(f"""<div class="{box_class}">
            <strong>{req['Req ID']} ({req['Priority']}) — {req['Requirement']}</strong><br>
            <strong>Why this matters:</strong> {req['Why This Matters']}<br>
            <strong>Currently available:</strong> {req['Currently Available']}
        </div>""", unsafe_allow_html=True)

# ── TAB 5 ─────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-title">Why this matters for regulators, fintechs, and consumers</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">The regulatory gap</div>', unsafe_allow_html=True)
        st.markdown("""<div class="alert">
            BNPL is the fastest-growing consumer credit product in Canada but it operates almost entirely
            outside the regulatory framework that governs credit cards, lines of credit, and personal loans.
            There is no mandatory credit assessment. No reporting to bureaus. No limit on simultaneous plans.
            No requirement to show consumers their total commitment before they add another plan.
            Canada is watching Australia and the UK move toward BNPL regulation and a similar framework
            is expected here within the next 12 to 24 months.
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class="insight">
            The fintech opportunity here is significant. The platform that introduces responsible
            design features before regulation requires them builds consumer trust and positions itself
            as the default choice when Canadians who want to use BNPL responsibly look for a platform
            they can actually rely on.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Stakeholder summary</div>', unsafe_allow_html=True)
        stakeholders = pd.DataFrame([
            {"Stakeholder":"Canadian Consumers","Interest":"Use BNPL without building invisible debt. Understand their total commitment."},
            {"Stakeholder":"BNPL Platforms","Interest":"Grow user base. Avoid regulatory backlash. Differentiate on trust."},
            {"Stakeholder":"Canadian Banks","Interest":"Monitor BNPL as shadow credit. Understand exposure of their customers."},
            {"Stakeholder":"Financial Consumer Agency of Canada","Interest":"Protect consumers from deceptive credit products. Update regulatory framework."},
            {"Stakeholder":"Retailers","Interest":"Offer BNPL to increase conversion. Avoid association with consumer debt harm."},
        ])
        st.dataframe(stakeholders, use_container_width=True, hide_index=True)

st.divider()
st.markdown(
    "**Data note:** All consumer and transaction data is synthetic and generated for portfolio purposes. "
    "BNPL platform information based on publicly available product details as of May 2026. "
    "Consumer behaviour patterns modelled on published Canadian fintech industry research. "
    "Prepared by Simran Saran as part of The Case Files portfolio series."
)
