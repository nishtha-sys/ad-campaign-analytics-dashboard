import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ad Campaign Performance Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/ad_campaign_cleaned.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

st.title("📊 Ad Campaign Performance Dashboard")
st.caption("Cross-platform campaign analytics — Google Ads, Meta Ads, TikTok Ads")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect("Platform", options=df['platform'].unique(), default=list(df['platform'].unique()))
campaign_types = st.sidebar.multiselect("Campaign Type", options=df['campaign_type'].unique(), default=list(df['campaign_type'].unique()))
industries = st.sidebar.multiselect("Industry", options=df['industry'].unique(), default=list(df['industry'].unique()))
countries = st.sidebar.multiselect("Country", options=df['country'].unique(), default=list(df['country'].unique()))

date_min, date_max = df['date'].min(), df['date'].max()
date_range = st.sidebar.date_input("Date Range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

filtered = df[
    (df['platform'].isin(platforms)) &
    (df['campaign_type'].isin(campaign_types)) &
    (df['industry'].isin(industries)) &
    (df['country'].isin(countries))
]

if len(date_range) == 2:
    filtered = filtered[(filtered['date'] >= pd.to_datetime(date_range[0])) & (filtered['date'] <= pd.to_datetime(date_range[1]))]

if filtered.empty:
    st.warning("No data matches the selected filters. Adjust filters in the sidebar.")
    st.stop()

# ---------------- KPI ROW ----------------
total_spend = filtered['ad_spend'].sum()
total_revenue = filtered['revenue'].sum()
overall_roas = total_revenue / total_spend if total_spend else 0
avg_ctr = filtered['CTR'].mean()
avg_cpc = filtered['CPC'].mean()
avg_cpm = filtered['CPM'].mean()
total_conversions = filtered['conversions'].sum()

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Spend", f"${total_spend:,.0f}")
k2.metric("Total Revenue", f"${total_revenue:,.0f}")
k3.metric("Overall ROAS", f"{overall_roas:.2f}x")
k4.metric("Avg CTR", f"{avg_ctr*100:.2f}%")
k5.metric("Avg CPC", f"${avg_cpc:.2f}")
k6.metric("Avg CPM", f"${avg_cpm:.2f}")

st.divider()

# ---------------- PLATFORM COMPARISON ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("ROAS by Platform")
    platform_roas = filtered.groupby('platform', as_index=False)['ROAS'].mean().sort_values('ROAS', ascending=False)
    fig1 = px.bar(platform_roas, x='platform', y='ROAS', color='platform', text_auto='.2f')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Spend vs Revenue by Platform")
    spend_rev = filtered.groupby('platform', as_index=False)[['ad_spend', 'revenue']].sum()
    spend_rev_melt = spend_rev.melt(id_vars='platform', value_vars=['ad_spend', 'revenue'], var_name='Metric', value_name='Amount')
    fig2 = px.bar(spend_rev_melt, x='platform', y='Amount', color='Metric', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TREND OVER TIME ----------------
st.subheader("ROAS Trend Over Time")
trend = filtered.groupby([pd.Grouper(key='date', freq='W'), 'platform'], as_index=False)['ROAS'].mean()
fig3 = px.line(trend, x='date', y='ROAS', color='platform', markers=True)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- CAMPAIGN TYPE & INDUSTRY ----------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Avg ROAS by Campaign Type")
    ct = filtered.groupby('campaign_type', as_index=False)['ROAS'].mean().sort_values('ROAS', ascending=False)
    fig4 = px.bar(ct, x='campaign_type', y='ROAS', text_auto='.2f')
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.subheader("Avg ROAS by Industry")
    ind = filtered.groupby('industry', as_index=False)['ROAS'].mean().sort_values('ROAS', ascending=False)
    fig5 = px.bar(ind, x='industry', y='ROAS', text_auto='.2f')
    st.plotly_chart(fig5, use_container_width=True)

# ---------------- TOP / BOTTOM PERFORMERS ----------------
st.subheader("🏆 Top 10 Campaigns by ROAS")
top10 = filtered.nlargest(10, 'ROAS')[['date', 'platform', 'campaign_type', 'industry', 'country', 'ad_spend', 'revenue', 'ROAS']]
st.dataframe(top10, use_container_width=True, hide_index=True)

st.subheader("🚩 Bottom 10 Campaigns by ROAS (flagged for review)")
bottom10 = filtered.nsmallest(10, 'ROAS')[['date', 'platform', 'campaign_type', 'industry', 'country', 'ad_spend', 'revenue', 'ROAS']]
st.dataframe(bottom10, use_container_width=True, hide_index=True)

# ---------------- CORRELATION HEATMAP ----------------
st.subheader("Metric Correlation Matrix")
corr_cols = ['ad_spend', 'CTR', 'CPC', 'CPM', 'ROAS', 'CPA']
corr = filtered[corr_cols].corr()
fig6 = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
st.plotly_chart(fig6, use_container_width=True)

# ---------------- KEY INSIGHTS ----------------
st.subheader("📌 Key Insights")
best_platform = platform_roas.iloc[0]['platform']
worst_platform = platform_roas.iloc[-1]['platform']
spend_roas_corr = filtered[['ad_spend', 'ROAS']].corr().iloc[0, 1]

st.markdown(f"""
- **{best_platform}** delivers the highest average ROAS ({platform_roas.iloc[0]['ROAS']:.2f}x) among selected platforms, while **{worst_platform}** trails at {platform_roas.iloc[-1]['ROAS']:.2f}x — despite comparable or higher spend.
- Ad spend and ROAS show a **{'negative' if spend_roas_corr < 0 else 'positive'} correlation ({spend_roas_corr:.2f})**, suggesting {'diminishing returns at higher spend levels — budget reallocation toward efficient platforms may improve overall ROAS' if spend_roas_corr < 0 else 'scaling spend continues to improve returns in this dataset'}.
- {len(bottom10)} campaigns in the current filter are flagged with ROAS below 1x break-even and should be reviewed or paused.
""")

st.caption("Data source: Global Ads Performance dataset (Kaggle) · Built by Nishtha Sahani")