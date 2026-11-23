"""Weekly channel stats -> stats/yt_stats_<date>.csv (per video, from 2026-10-30 to today).
Env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN. Never prints secrets.
Also writes yt_traffic_<date>.csv (traffic sources per day) and yt_impressions_<date>.csv (impressions/CTR; metric names unverified, skipped if refused)."""
import os, csv, sys, datetime as dt, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

START = "2026-10-30"
creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token", client_id=os.environ["YT_CLIENT_ID"],
    client_secret=os.environ["YT_CLIENT_SECRET"])
creds.refresh(Request())
an = build("youtubeAnalytics", "v2", credentials=creds)
yt = build("youtube", "v3", credentials=creds)
today = dt.date.today().isoformat()
METRICS = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes"
try:
    r = an.reports().query(ids="channel==MINE", startDate=START, endDate=today, metrics=METRICS,
                           dimensions="video", sort="-views", maxResults=200).execute()
except HttpError as e:
    print("API error", e.resp.status, str(e)[:300]); sys.exit(1)
rows = r.get("rows", [])
info = {}
for k in range(0, len(rows), 50):
    ids = ",".join(x[0] for x in rows[k:k+50])
    for v in yt.videos().list(part="snippet,contentDetails,status", id=ids).execute()["items"]:
        info[v["id"]] = (v["snippet"]["title"], v["contentDetails"]["duration"], v["snippet"].get("publishedAt", ""), v["status"].get("publishAt", ""))
out = pathlib.Path("stats"); out.mkdir(exist_ok=True)
f = out / f"yt_stats_{today}.csv"
with open(f, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["video_id", "title", "duration", "published", "scheduled"] + METRICS.split(","))
    for x in rows:
        t = info.get(x[0], ("", "", "", ""))
        w.writerow([x[0], t[0], t[1], t[2], t[3]] + x[1:])
print("wrote", f, len(rows), "videos")

# ---- extra reports (best effort: a failure here never stops the main CSV) ----
def extra(name, **q):
    try:
        r = an.reports().query(ids="channel==MINE", startDate=START, endDate=today, **q).execute()
    except HttpError as e:
        print(name, "NOT AVAILABLE:", e.resp.status, str(e)[:200]); return
    g = out / f"{name}_{today}.csv"
    with open(g, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([h["name"] for h in r["columnHeaders"]]); w.writerows(r.get("rows", []))
    print("wrote", g, len(r.get("rows", [])), "rows")
# channel traffic sources per day
extra("yt_traffic", metrics="views,estimatedMinutesWatched", dimensions="day,insightTrafficSourceType", sort="day")
# thumbnail impressions / CTR per video (metric names unverified; skipped if the API refuses)
extra("yt_impressions", metrics="videoThumbnailImpressions,videoThumbnailImpressionsClickRate", dimensions="video", sort="-videoThumbnailImpressions", maxResults=200)
