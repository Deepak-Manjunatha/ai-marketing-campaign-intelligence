# AI Marketing Campaign Intelligence

An end-to-end business analytics project that turns raw marketing campaign data into executive decisions using SQL, Python, visualization, and AI-style business recommendations.

## Project Summary

This project simulates a realistic multi-channel marketing campaign portfolio for a growing event and lifestyle brand. The goal is to help management understand which channels, campaigns, audiences, and cities are driving revenue, conversions, and return on ad spend.

The project is designed for analytics, business intelligence, marketing analytics, and AI-driven analyst roles.

## Business Problem

Marketing teams often spend across Google Ads, Meta, LinkedIn, email, influencer campaigns, offline events, and sponsorship promotions without a clear view of which investments create measurable business value.

This project answers:

- Which marketing channels generate the highest revenue and ROAS?
- Which campaigns convert efficiently?
- Which audience segments should receive more budget?
- Which cities and customer groups show the strongest commercial opportunity?
- What should a business manager do next based on the data?

## What I Built

- Created a synthetic but realistic marketing campaign dataset.
- Designed a SQL database schema for campaign analytics.
- Wrote SQL queries for channel performance, campaign ROI, city performance, and audience segmentation.
- Built a Python analytics pipeline for cleaning, feature engineering, KPI calculation, and visualization.
- Created dashboard-ready processed datasets.
- Produced executive-level insights and recommendations.
- Documented the full workflow for GitHub and LinkedIn portfolio use.

## Tools and Skills Demonstrated

- SQL
- Python
- pandas
- matplotlib
- SQLite
- Data cleaning
- KPI engineering
- Marketing analytics
- Campaign ROI analysis
- Customer segmentation
- Executive storytelling
- GitHub project documentation

## Repository Structure

```text
.
├── dashboard/
│   ├── dashboard.html
│   └── dashboard_wireframe.md
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── data_dictionary.md
│   └── executive_report.md
├── assets/
│   └── profile/
│       ├── deepak-m-github-avatar.png
│       └── deepak-m-github-avatar.svg
├── notebooks/
│   └── analysis_walkthrough.ipynb
├── outputs/
│   └── charts/
├── sql/
│   ├── 01_schema.sql
│   └── 02_business_questions.sql
├── src/
│   ├── generate_synthetic_data.py
│   └── run_analysis.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Key KPIs

- Revenue
- Spend
- Conversions
- Leads
- Impressions
- Clicks
- CTR
- CPC
- Conversion rate
- Cost per acquisition
- Return on ad spend
- Average order value

## How to Run This Project

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Generate raw synthetic data:

```bash
python src/generate_synthetic_data.py
```

3. Run the analytics pipeline:

```bash
python src/run_analysis.py
```

4. Open the outputs:

- `data/processed/channel_performance.csv`
- `data/processed/campaign_performance.csv`
- `data/processed/audience_segment_performance.csv`
- `outputs/charts/`
- `docs/executive_report.md`

## Main Findings

The generated analysis identifies:

- Retargeting produced the strongest ROAS at approximately 14.44x.
- Email was the most efficient low-cost channel with approximately 14.39x ROAS.
- Google Search was the strongest scalable acquisition channel with approximately AUD 1.19M revenue.
- Melbourne generated the highest city-level revenue, while Bangalore produced the strongest city-level ROAS.
- LinkedIn Ads and Influencer campaigns need sharper targeting or should be measured as awareness channels.

## Recommended Business Actions

1. Increase budget for high-ROAS search, email, and retargeting campaigns.
2. Use social and influencer channels for top-of-funnel reach, but connect them to remarketing journeys.
3. Build city-level campaign playbooks for Melbourne, Sydney, Bangalore, and other high-performing markets.
4. Track campaign performance weekly using a dashboard instead of waiting until campaign end.
5. Use AI-assisted reporting to convert KPI tables into executive summaries.

## Files to Review First

If you are reviewing this project quickly, start here:

1. `docs/executive_report.md`
2. `sql/02_business_questions.sql`
3. `src/run_analysis.py`
4. `outputs/charts/`
5. `dashboard/dashboard.html`

## Suggested LinkedIn Post

I built an end-to-end AI Marketing Campaign Intelligence project using SQL, Python, and dashboard-ready datasets.

The project analyzes campaign spend, revenue, conversions, ROAS, city performance, and audience segments, then converts the results into executive recommendations.

This helped me practice the full analytics workflow: business problem framing, data preparation, SQL analysis, Python KPI engineering, visualization, and insight storytelling.

## Portfolio Positioning

This project supports roles such as:

- Data Analyst
- Business Analyst
- Marketing Analyst
- BI Analyst
- Product Analyst
- Analytics Consultant
- AI-enabled Business Analyst
