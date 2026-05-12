DROP TABLE IF EXISTS marketing_campaigns;

CREATE TABLE marketing_campaigns (
  campaign_id TEXT PRIMARY KEY,
  date TEXT NOT NULL,
  campaign_name TEXT NOT NULL,
  channel TEXT NOT NULL,
  city TEXT NOT NULL,
  audience_segment TEXT NOT NULL,
  objective TEXT NOT NULL,
  spend_aud REAL NOT NULL,
  impressions INTEGER NOT NULL,
  clicks INTEGER NOT NULL,
  leads INTEGER NOT NULL,
  conversions INTEGER NOT NULL,
  revenue_aud REAL NOT NULL,
  customer_rating REAL NOT NULL
);

CREATE INDEX idx_campaign_channel ON marketing_campaigns(channel);
CREATE INDEX idx_campaign_city ON marketing_campaigns(city);
CREATE INDEX idx_campaign_segment ON marketing_campaigns(audience_segment);
CREATE INDEX idx_campaign_date ON marketing_campaigns(date);

