from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def generate_campaign_data(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    channels = {
        "Google Search": {"ctr": 0.052, "cvr": 0.024, "aov": 245, "spend": 1250},
        "Meta Ads": {"ctr": 0.027, "cvr": 0.014, "aov": 185, "spend": 980},
        "LinkedIn Ads": {"ctr": 0.014, "cvr": 0.011, "aov": 360, "spend": 840},
        "Email": {"ctr": 0.092, "cvr": 0.033, "aov": 175, "spend": 320},
        "Influencer": {"ctr": 0.031, "cvr": 0.01, "aov": 210, "spend": 760},
        "Sponsorship": {"ctr": 0.018, "cvr": 0.015, "aov": 460, "spend": 1450},
        "Retargeting": {"ctr": 0.071, "cvr": 0.038, "aov": 205, "spend": 680},
    }
    cities = ["Melbourne", "Sydney", "Brisbane", "Bangalore", "Delhi", "Mumbai"]
    segments = [
        "Students",
        "Young Professionals",
        "Corporate Buyers",
        "Families",
        "Music Enthusiasts",
        "Premium Experience Seekers",
    ]
    objectives = ["Awareness", "Lead Generation", "Ticket Sales", "Sponsorship", "Retargeting"]
    campaign_themes = [
        "Summer Launch",
        "Festival Push",
        "Early Bird",
        "VIP Upgrade",
        "Weekend Boost",
        "Corporate Outreach",
        "Student Offer",
        "Last Mile Sales",
    ]

    rows = []
    for i in range(520):
        channel = rng.choice(list(channels.keys()), p=[0.22, 0.2, 0.08, 0.14, 0.11, 0.1, 0.15])
        params = channels[channel]
        city = rng.choice(cities, p=[0.26, 0.2, 0.11, 0.18, 0.11, 0.14])
        segment = rng.choice(segments)
        objective = rng.choice(objectives, p=[0.2, 0.18, 0.35, 0.1, 0.17])
        theme = rng.choice(campaign_themes)
        date = rng.choice(dates)

        city_factor = {
            "Melbourne": 1.12,
            "Sydney": 1.08,
            "Brisbane": 0.86,
            "Bangalore": 1.18,
            "Delhi": 0.94,
            "Mumbai": 1.03,
        }[city]
        segment_factor = {
            "Students": 0.82,
            "Young Professionals": 1.08,
            "Corporate Buyers": 1.34,
            "Families": 0.9,
            "Music Enthusiasts": 1.16,
            "Premium Experience Seekers": 1.42,
        }[segment]
        objective_factor = {
            "Awareness": 0.72,
            "Lead Generation": 0.94,
            "Ticket Sales": 1.24,
            "Sponsorship": 1.38,
            "Retargeting": 1.3,
        }[objective]

        spend = max(80, rng.normal(params["spend"], params["spend"] * 0.28))
        impressions = int(max(1000, spend * rng.normal(20, 4)))
        ctr = max(0.004, rng.normal(params["ctr"], params["ctr"] * 0.18))
        clicks = int(impressions * ctr)
        lead_rate = max(0.05, rng.normal(0.18, 0.035))
        leads = int(clicks * lead_rate)
        conversion_rate = max(0.004, rng.normal(params["cvr"], params["cvr"] * 0.25))
        conversions = int(clicks * conversion_rate * city_factor * objective_factor)
        aov = max(45, rng.normal(params["aov"], params["aov"] * 0.22))
        revenue = conversions * aov * segment_factor
        rating = float(np.clip(rng.normal(4.2, 0.35), 2.8, 5.0))

        rows.append(
            {
                "campaign_id": f"CMP-{i + 1:04d}",
                "date": pd.Timestamp(date).strftime("%Y-%m-%d"),
                "campaign_name": f"{theme} - {channel}",
                "channel": channel,
                "city": city,
                "audience_segment": segment,
                "objective": objective,
                "spend_aud": round(float(spend), 2),
                "impressions": impressions,
                "clicks": clicks,
                "leads": max(leads, 0),
                "conversions": max(conversions, 0),
                "revenue_aud": round(float(revenue), 2),
                "customer_rating": round(rating, 2),
            }
        )

    return pd.DataFrame(rows).sort_values(["date", "campaign_id"])


def main() -> None:
    df = generate_campaign_data()
    output_path = RAW_DIR / "marketing_campaign_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows: {output_path}")


if __name__ == "__main__":
    main()
