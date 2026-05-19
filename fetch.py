import json
import os
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, Dimension, Metric, DateRange, OrderBy
)
from auth import get_credentials

PROPERTY_ID = "275227762"
DATE_RANGE = [DateRange(start_date="30daysAgo", end_date="today")]

credentials = get_credentials()
client = BetaAnalyticsDataClient(credentials=credentials)


def report(dimensions, metrics, limit=25, order_metric=None):
    kwargs = dict(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=DATE_RANGE,
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
        headers = dimensions + metrics
        return {"headers": headers, "rows": rows}
    except Exception as e:
        return {"headers": dimensions + metrics, "rows": [], "error": str(e)}


print("Fetching GA4 data...")

data = {
    "generated": datetime.now().strftime("%d %B %Y, %H:%M"),
    "geo_country":   report(["country"],              ["sessions", "activeUsers", "averageSessionDuration"], order_metric="sessions"),
    "geo_city":      report(["city", "country"],       ["sessions", "activeUsers"], order_metric="sessions"),
    "age":           report(["userAgeBracket"],        ["activeUsers", "sessions"], order_metric="activeUsers"),
    "gender":        report(["userGender"],            ["activeUsers", "sessions"], order_metric="activeUsers"),
    "device":        report(["deviceCategory"],        ["sessions", "activeUsers", "averageSessionDuration"], order_metric="sessions"),
    "os":            report(["operatingSystem"],       ["sessions", "activeUsers"], order_metric="sessions"),
    "browser":       report(["browser"],               ["sessions", "activeUsers"], order_metric="sessions"),
    "channel":       report(["sessionDefaultChannelGroup"], ["sessions", "activeUsers", "bounceRate", "averageSessionDuration"], order_metric="sessions"),
    "source":        report(["sessionSource", "sessionMedium"], ["sessions", "activeUsers"], order_metric="sessions"),
    "landing_pages": report(["landingPage"],           ["sessions", "activeUsers", "bounceRate", "averageSessionDuration"], order_metric="sessions"),
    "search_terms":  report(["searchTerm"],            ["sessions", "activeUsers"], order_metric="sessions"),
    "engagement":    report(["date"],                  ["activeUsers", "sessions", "averageSessionDuration", "engagementRate"], limit=30, order_metric="activeUsers"),
}

with open(os.path.join(os.path.dirname(__file__), "ga_data.json"), "w") as f:
    json.dump(data, f, indent=2)

print("Done — ga_data.json written")
