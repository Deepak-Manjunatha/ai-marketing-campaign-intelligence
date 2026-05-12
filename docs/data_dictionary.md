# Data Dictionary

## Raw Dataset: `data/raw/marketing_campaign_data.csv`

| Column | Description |
|---|---|
| `campaign_id` | Unique campaign row identifier. |
| `date` | Campaign activity date. |
| `campaign_name` | Campaign theme and channel name. |
| `channel` | Marketing channel such as Google Search, Meta Ads, Email, Retargeting, Sponsorship, Influencer, or LinkedIn Ads. |
| `city` | Market where the campaign was active. |
| `audience_segment` | Target audience group. |
| `objective` | Campaign objective such as Awareness, Lead Generation, Ticket Sales, Sponsorship, or Retargeting. |
| `spend_aud` | Campaign spend in Australian dollars. |
| `impressions` | Number of times the campaign was shown. |
| `clicks` | Number of user clicks. |
| `leads` | Number of leads generated. |
| `conversions` | Number of final conversions. |
| `revenue_aud` | Revenue generated in Australian dollars. |
| `customer_rating` | Simulated customer satisfaction rating. |

## Engineered KPIs

| KPI | Formula | Business Meaning |
|---|---|---|
| `ctr_pct` | clicks / impressions * 100 | Measures ad engagement. |
| `cpc_aud` | spend / clicks | Average cost per click. |
| `conversion_rate_pct` | conversions / clicks * 100 | Measures how efficiently clicks become conversions. |
| `cpa_aud` | spend / conversions | Average cost to acquire one conversion. |
| `roas` | revenue / spend | Revenue generated for every dollar spent. |
| `aov_aud` | revenue / conversions | Average order value. |

