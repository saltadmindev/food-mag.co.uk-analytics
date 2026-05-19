import json
import os
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, Dimension, Metric, DateRange, OrderBy,
    FilterExpression, Filter
)
from auth import get_credentials

PROPERTY_ID = "275227762"

credentials = get_credentials()
client = BetaAnalyticsDataClient(credentials=credentials)

GB_FILTER = FilterExpression(
    filter=Filter(
        field_name="country",
        string_filter=Filter.StringFilter(
            match_type=Filter.StringFilter.MatchType.EXACT,
            value="United Kingdom"
        )
    )
)


def fetch_range(date_range, engagement_limit, country_filter=None):
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
        if country_filter:
            kwargs["dimension_filter"] = country_filter
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


print("Fetching worldwide 6-month...")
ww_6m = fetch_range("180daysAgo", 180)

print("Fetching worldwide 12-month...")
ww_12m = fetch_range("365daysAgo", 365)

print("Fetching GB 6-month...")
gb_6m = fetch_range("180daysAgo", 180, GB_FILTER)

print("Fetching GB 12-month...")
gb_12m = fetch_range("365daysAgo", 365, GB_FILTER)

data = {
    "generated": datetime.now().strftime("%d %B %Y, %H:%M"),
    "ww_6m": ww_6m,
    "ww_12m": ww_12m,
    "gb_6m": gb_6m,
    "gb_12m": gb_12m,
}

with open(os.path.join(os.path.dirname(__file__), "ga_data.json"), "w") as f:
    json.dump(data, f, indent=2)

print("Done — ga_data.json written")
