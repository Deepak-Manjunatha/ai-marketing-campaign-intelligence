-- 1. Channel performance: which channels generate the strongest commercial returns?
SELECT
  channel,
  ROUND(SUM(spend_aud), 2) AS total_spend_aud,
  ROUND(SUM(revenue_aud), 2) AS total_revenue_aud,
  SUM(conversions) AS conversions,
  ROUND(SUM(revenue_aud) / NULLIF(SUM(spend_aud), 0), 2) AS roas,
  ROUND(SUM(spend_aud) / NULLIF(SUM(conversions), 0), 2) AS cpa_aud,
  ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2) AS ctr_pct,
  ROUND(100.0 * SUM(conversions) / NULLIF(SUM(clicks), 0), 2) AS conversion_rate_pct
FROM marketing_campaigns
GROUP BY channel
ORDER BY roas DESC;

-- 2. Top campaigns by revenue.
SELECT
  campaign_name,
  channel,
  city,
  audience_segment,
  ROUND(SUM(revenue_aud), 2) AS total_revenue_aud,
  ROUND(SUM(spend_aud), 2) AS total_spend_aud,
  ROUND(SUM(revenue_aud) / NULLIF(SUM(spend_aud), 0), 2) AS roas,
  SUM(conversions) AS conversions
FROM marketing_campaigns
GROUP BY campaign_name, channel, city, audience_segment
ORDER BY total_revenue_aud DESC
LIMIT 10;

-- 3. City opportunity: where should expansion budget go?
SELECT
  city,
  ROUND(SUM(revenue_aud), 2) AS revenue_aud,
  ROUND(SUM(spend_aud), 2) AS spend_aud,
  SUM(conversions) AS conversions,
  ROUND(SUM(revenue_aud) / NULLIF(SUM(spend_aud), 0), 2) AS roas
FROM marketing_campaigns
GROUP BY city
ORDER BY revenue_aud DESC;

-- 4. Audience segment performance.
SELECT
  audience_segment,
  ROUND(SUM(spend_aud), 2) AS spend_aud,
  ROUND(SUM(revenue_aud), 2) AS revenue_aud,
  SUM(leads) AS leads,
  SUM(conversions) AS conversions,
  ROUND(SUM(revenue_aud) / NULLIF(SUM(spend_aud), 0), 2) AS roas,
  ROUND(100.0 * SUM(conversions) / NULLIF(SUM(leads), 0), 2) AS lead_to_conversion_pct
FROM marketing_campaigns
GROUP BY audience_segment
ORDER BY roas DESC;

-- 5. Weekly trend for dashboarding.
SELECT
  strftime('%Y-%W', date) AS year_week,
  ROUND(SUM(spend_aud), 2) AS spend_aud,
  ROUND(SUM(revenue_aud), 2) AS revenue_aud,
  SUM(conversions) AS conversions,
  ROUND(SUM(revenue_aud) / NULLIF(SUM(spend_aud), 0), 2) AS roas
FROM marketing_campaigns
GROUP BY year_week
ORDER BY year_week;

