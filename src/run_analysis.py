from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "marketing_campaign_data.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
CHART_DIR = ROOT / "outputs" / "charts"
SQL_SCHEMA = ROOT / "sql" / "01_schema.sql"
SQL_ANALYSIS = ROOT / "sql" / "02_business_questions.sql"
DB_PATH = ROOT / "data" / "processed" / "marketing_campaigns.sqlite"


def add_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["ctr_pct"] = (df["clicks"] / df["impressions"]).fillna(0) * 100
    df["cpc_aud"] = (df["spend_aud"] / df["clicks"]).replace([float("inf")], 0).fillna(0)
    df["conversion_rate_pct"] = (df["conversions"] / df["clicks"]).replace([float("inf")], 0).fillna(0) * 100
    df["cpa_aud"] = (df["spend_aud"] / df["conversions"]).replace([float("inf")], 0).fillna(0)
    df["roas"] = (df["revenue_aud"] / df["spend_aud"]).replace([float("inf")], 0).fillna(0)
    df["aov_aud"] = (df["revenue_aud"] / df["conversions"]).replace([float("inf")], 0).fillna(0)
    df["year_week"] = df["date"].dt.strftime("%Y-%U")
    return df


def aggregate_outputs(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    channel = (
        df.groupby("channel", as_index=False)
        .agg(
            spend_aud=("spend_aud", "sum"),
            revenue_aud=("revenue_aud", "sum"),
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            leads=("leads", "sum"),
            conversions=("conversions", "sum"),
        )
    )
    channel = add_group_kpis(channel).sort_values("roas", ascending=False)

    campaign = (
        df.groupby(["campaign_name", "channel", "city", "audience_segment"], as_index=False)
        .agg(
            spend_aud=("spend_aud", "sum"),
            revenue_aud=("revenue_aud", "sum"),
            impressions=("impressions", "sum"),
            clicks=("clicks", "sum"),
            leads=("leads", "sum"),
            conversions=("conversions", "sum"),
        )
    )
    campaign = add_group_kpis(campaign).sort_values("revenue_aud", ascending=False)

    segment = (
        df.groupby("audience_segment", as_index=False)
        .agg(
            spend_aud=("spend_aud", "sum"),
            revenue_aud=("revenue_aud", "sum"),
            leads=("leads", "sum"),
            conversions=("conversions", "sum"),
            clicks=("clicks", "sum"),
            impressions=("impressions", "sum"),
        )
    )
    segment = add_group_kpis(segment).sort_values("roas", ascending=False)

    city = (
        df.groupby("city", as_index=False)
        .agg(
            spend_aud=("spend_aud", "sum"),
            revenue_aud=("revenue_aud", "sum"),
            conversions=("conversions", "sum"),
            clicks=("clicks", "sum"),
            impressions=("impressions", "sum"),
        )
    )
    city = add_group_kpis(city).sort_values("revenue_aud", ascending=False)

    weekly = (
        df.groupby("year_week", as_index=False)
        .agg(spend_aud=("spend_aud", "sum"), revenue_aud=("revenue_aud", "sum"), conversions=("conversions", "sum"))
        .sort_values("year_week")
    )
    weekly["roas"] = weekly["revenue_aud"] / weekly["spend_aud"]

    return {
        "clean_campaign_data": df,
        "channel_performance": channel,
        "campaign_performance": campaign,
        "audience_segment_performance": segment,
        "city_performance": city,
        "weekly_performance": weekly,
    }


def add_group_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ctr_pct"] = df["clicks"] / df["impressions"] * 100
    df["conversion_rate_pct"] = df["conversions"] / df["clicks"] * 100
    df["cpa_aud"] = df["spend_aud"] / df["conversions"]
    df["roas"] = df["revenue_aud"] / df["spend_aud"]
    df["aov_aud"] = df["revenue_aud"] / df["conversions"]
    return df.replace([float("inf"), -float("inf")], 0).fillna(0)


def save_sqlite(df: pd.DataFrame) -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SQL_SCHEMA.read_text())
        upload_df = df.copy()
        upload_df["date"] = upload_df["date"].dt.strftime("%Y-%m-%d")
        upload_df[
            [
                "campaign_id",
                "date",
                "campaign_name",
                "channel",
                "city",
                "audience_segment",
                "objective",
                "spend_aud",
                "impressions",
                "clicks",
                "leads",
                "conversions",
                "revenue_aud",
                "customer_rating",
            ]
        ].to_sql("marketing_campaigns", conn, if_exists="append", index=False)

        sql_text = SQL_ANALYSIS.read_text()
        query_blocks = [block.strip() for block in sql_text.split(";") if block.strip().lower().startswith("--")]
        for idx, block in enumerate(query_blocks, start=1):
            query = block.split("\n", 1)[1]
            result = pd.read_sql_query(query, conn)
            result.to_csv(PROCESSED_DIR / f"sql_result_{idx}.csv", index=False)


def make_charts(outputs: dict[str, pd.DataFrame]) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    channel = outputs["channel_performance"].sort_values("revenue_aud", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(channel["channel"], channel["revenue_aud"], color="#1d4ed8")
    ax.set_title("Revenue by Marketing Channel")
    ax.set_xlabel("Revenue AUD")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "revenue_by_channel.png", dpi=180)
    plt.close(fig)

    roas = outputs["channel_performance"].sort_values("roas", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(roas["channel"], roas["roas"], color="#0f766e")
    ax.set_title("Return on Ad Spend by Channel")
    ax.set_xlabel("ROAS")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "roas_by_channel.png", dpi=180)
    plt.close(fig)

    weekly = outputs["weekly_performance"]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(weekly["year_week"], weekly["revenue_aud"], label="Revenue", color="#1d4ed8", linewidth=2)
    ax.plot(weekly["year_week"], weekly["spend_aud"], label="Spend", color="#b91c1c", linewidth=2)
    ax.set_title("Weekly Revenue vs Spend")
    ax.set_xlabel("Week")
    ax.set_ylabel("AUD")
    ax.tick_params(axis="x", rotation=70)
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "weekly_revenue_vs_spend.png", dpi=180)
    plt.close(fig)

    campaign = outputs["campaign_performance"].head(15).sort_values("revenue_aud", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(campaign["campaign_name"], campaign["revenue_aud"], color="#7c3aed")
    ax.set_title("Top 15 Campaigns by Revenue")
    ax.set_xlabel("Revenue AUD")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "top_campaigns_by_revenue.png", dpi=180)
    plt.close(fig)

    segment = outputs["audience_segment_performance"].sort_values("roas", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(segment["audience_segment"], segment["roas"], color="#a16207")
    ax.set_title("ROAS by Audience Segment")
    ax.set_xlabel("ROAS")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "roas_by_audience_segment.png", dpi=180)
    plt.close(fig)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Missing raw data. Run src/generate_synthetic_data.py first: {RAW_PATH}")

    raw = pd.read_csv(RAW_PATH)
    clean = add_kpis(raw)
    outputs = aggregate_outputs(clean)

    for name, output_df in outputs.items():
        output_df.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)

    save_sqlite(clean)
    make_charts(outputs)

    print("Analysis complete.")
    print(f"Processed files: {PROCESSED_DIR}")
    print(f"Charts: {CHART_DIR}")


if __name__ == "__main__":
    main()

