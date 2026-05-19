import json
import os
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, Dimension, Metric, DateRange, OrderBy
)
from auth import get_credentials

PROPERTY_ID = "275227762"

credentials = get_credentials()
client = BetaAnalyticsDataClient(credentials=credentials)


def fetch_range(date_range, engagement_limit):
    def report(dimensions, metrics, limit=25, order_metric=None):
        kwargs = dict(
            property=f"properties/{PROPERTY_ID}",
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            date_ranges=[DateRange(start_date=date_range, end_date="today")],
            limit=limit,
        )
        if order_metric:
            kwargs["order_bys"] = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric), desc=True)]
        try:
            resp = client.run_report(RunReportRequest(**kwargs))
            rows = []
            for row in resp.rows:
                dims = [d.value for d in row.dimension_values]
                mets = [m.value for m in row.metric_values]
                rows.append(dims + mets)
            return {"headers": dimensions + metrics, "rows": rows}
        except Exception as e:
            return {"headers": dimensions + metrics, "rows": [], "error": str(e)}

    return {
        "geo_country":   report(["country"],                   ["sessions", "activeUsers", "averageSessionDuration"], order_metric="sessions"),
        "geo_city":      report(["city", "country"],            ["sessions", "activeUsers"], order_metric="sessions"),
        "age":           report(["userAgeBracket"],             ["activeUsers", "sessions"], order_metric="activeUsers"),
        "gender":        report(["userGender"],                 ["activeUsers", "sessions"], order_metric="activeUsers"),
        "device":        report(["deviceCategory"],             ["sessions", "activeUsers", "averageSessionDuration"], order_metric="sessions"),
        "os":            report(["operatingSystem"],            ["sessions", "activeUsers"], order_metric="sessions"),
        "browser":       report(["browser"],                    ["sessions", "activeUsers"], order_metric="sessions"),
        "channel":       report(["sessionDefaultChannelGroup"], ["sessions", "activeUsers", "bounceRate", "averageSessionDuration"], order_metric="sessions"),
        "source":        report(["sessionSource", "sessionMedium"], ["sessions", "activeUsers"], order_metric="sessions"),
        "landing_pages": report(["landingPage"],                ["sessions", "activeUsers", "bounceRate", "averageSessionDuration"], order_metric="sessions"),
        "search_terms":  report(["searchTerm"],                 ["sessions", "activeUsers"], order_metric="sessions"),
        "engagement":    report(["date"],                       ["activeUsers", "sessions", "averageSessionDuration", "engagementRate"], limit=engagement_limit, order_metric="sessions"),
    }


print("Fetching 6-month data...")
six_months = fetch_range("180daysAgo", 180)

print("Fetching 12-month data...")
twelve_months = fetch_range("365daysAgo", 365)

data = {
    "generated": datetime.now().strftime("%d %B %Y, %H:%M"),
    "6m": six_months,
    "12m": twelve_months,
}

with open(os.path.join(os.path.dirname(__file__), "ga_data.json"), "w") as f:
    json.dump(data, f, indent=2)

print("Done — ga_data.json written")
