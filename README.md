# 📊 Ad Campaign Performance Dashboard

Cross-platform ad campaign analytics dashboard tracking CTR, CPC, CPM, ROAS, and CPA across Google Ads, Meta Ads, and TikTok Ads. Built to surface performance patterns, flag underperforming campaigns, and support budget-allocation decisions.

🔗 **Live App:** [https://nishtha-ad-campaign-analytics-dashboard.streamlit.app/]

---

## Overview

This project analyzes 1,800 ad campaign records across 3 platforms, 4 campaign types, 5 industries, and 8 countries. It calculates and verifies core ad metrics, identifies performance drivers through correlation analysis, and presents findings through an interactive Streamlit dashboard.

## Key Findings

- **TikTok Ads delivers the highest ROAS (9.54x)** among all platforms, more than double Google Ads (4.11x), despite Google receiving the highest total ad spend — indicating budget inefficiency on Google Ads campaigns.
- **Ad spend is negatively correlated with ROAS (-0.26)**, suggesting diminishing returns at higher spend levels rather than proportional scaling of results.
- **CPM and CPC are strongly correlated with spend (0.73 and 0.55)** but not with better outcomes — higher-cost platforms did not consistently produce better ROAS.
- 10+ campaigns identified with ROAS below 1x (spending more than they return) and flagged for review.

## Features

- Multi-dimensional filtering: platform, campaign type, industry, country, date range
- Real-time KPI summary: total spend, revenue, ROAS, CTR, CPC, CPM
- Platform and campaign-type performance comparison
- Time-series ROAS trend across platforms
- Top/bottom 10 campaign leaderboard by ROAS
- Correlation matrix across all core metrics
- Auto-generated, filter-aware insights summary

## Methodology

1. Verified all pre-existing metric columns (CTR, CPC) by independently recalculating them from raw impressions/clicks/spend data — 0 mismatches found across 1,800 records
2. Engineered CPM (not present in source data) using standard formula: (spend / impressions) × 1000
3. Conducted groupby aggregation analysis across platform, campaign type, and industry dimensions
4. Ran Pearson correlation analysis to identify which cost metrics actually drive return, versus which merely correlate with spend
5. Built interactive dashboard with cached data loading for performance

## Tech Stack

- **Python** — pandas, numpy for data processing
- **Streamlit** — interactive web dashboard
- **Plotly** — interactive charts and correlation heatmap

## Dataset

[Global Ads Performance (Google, Meta, TikTok)](https://www.kaggle.com/datasets/nudratabbas/global-ads-performance-google-meta-tiktok) — Kaggle, 1,800 campaign-level records.

## Project Structure

```
ad-campaign-analytics-dashboard/
├── app.py                          # Streamlit dashboard
├── notebooks/
│   └── ad_campaign_analysis.ipynb  # Full EDA and metric verification (Colab)
├── data/
│   └── ad_campaign_cleaned.csv     # Cleaned dataset with engineered CPM feature
├── requirements.txt
└── README.md
```

## Running Locally

```bash
git clone https://github.com/nishtha-sys/ad-campaign-analytics-dashboard.git
cd ad-campaign-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Future Improvements

- Add statistical significance testing to underperformer flags (currently threshold-based)
- Incorporate day-of-week / seasonality analysis
- Add anomaly detection for sudden ROAS drops
- Export flagged campaigns as a downloadable CSV report

## Author

**Nishtha Sahani** — [Portfolio](https://portfolio-nishthasahani.vercel.app) · [GitHub](https://github.com/nishtha-sys)