"""Upload rendered videos to YouTube as PRIVATE + scheduled (miya publishes / sets the long thumbnail and end screen in Studio).
Called by the `youtube` job of .github/workflows/render-chunked.yml after the Drive upload.
Env: SLUGS_JSON  ([{"slug":..,"n":..}, ...] from the plan job), ROOT_ID, YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
     (rclone is already configured). Never prints secrets.
Rules (2026-11-20, from the channel as miya uploaded it):
  - category 27, language en, not made for kids, license youtube, embeddable, stats public
  - long -> playlist "Deep Dives - <Life & Biology|Space & Science>", short -> "Bite-Sized Knowledge - <...>"
  - 01.* Drive folder = Life & Biology, 02.* = Space & Science
  - hashtags "#Miya's Note #tag..." ; tags = "Miya's Note" + hashtags
  - slots: Tue/Thu/Sat/Sun (KST), long 07:00, shorts 08:00 08:30 09:00 09:30 10:00; next date after the last scheduled video
  - short thumbnail (<name>_thumbnail_A.png) is set here; the LONG thumbnail and end screen stay manual (miya)
  - a title that already exists on the channel is skipped (no duplicate uploads)"""
import os, re, sys, json, glob, subprocess, datetime as dt, pathlib
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

KST = dt.timezone(dt.timedelta(hours=9))
DAYS = {1, 3, 5, 6}                       # Tue Thu Sat Sun (Mon=0)
SHORT_T = {1: (8, 0), 2: (8, 30), 3: (9, 0), 4: (9, 30), 5: (10, 0)}
creds = Credentials(None, refresh_token=os.environ["YT_REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token", client_id=os.environ["YT_CLIENT_ID"],
    client_secret=os.environ["YT_CLIENT_SECRET"], scopes=["https://www.googleapis.com/auth/youtube"])
creds.refresh(Request())
yt = build("youtube", "v3", credentials=creds)
ROOT = os.environ.get("ROOT_ID", "")

# ---- channel state ----
playlists, titles, last = {}, set(), None
for p in yt.playlists().list(part="snippet", mine=True, maxResults=50).execute()["items"]:
    playlists[p["snippet"]["title"]] = p["id"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="snippet", playlistId=p["id"], maxResults=50, pageToken=tok).execute()
        ids += [i["snippet"]["resourceId"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok: break
    for k in range(0, len(ids), 50):
        for v in yt.videos().list(part="snippet,status", id=",".join(ids[k:k+50])).execute()["items"]:
            titles.add(v["snippet"]["title"].strip().lower())
            pa = v["status"].get("publishAt")
            if pa:
                t = dt.datetime.fromisoformat(pa.replace("Z", "+00:00")).astimezone(KST)
                if last is None or t > last: last = t
tomorrow = (dt.datetime.now(KST) + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
cur = max(tomorrow, (last + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)) if last else tomorrow
def next_date():
    global cur
    while cur.weekday() not in DAYS: cur += dt.timedelta(days=1)
    d = cur; cur += dt.timedelta(days=1); return d
print("last scheduled (KST):", last, "| next free date starts at", cur.date())

def sh(*a): subprocess.run(a, check=True)
def meta(p):
    t = pathlib.Path(p).read_text(encoding="utf-8")
    m = re.search(r"=== TITLE ===\s*(.+?)\s*=== DESCRIPTION ===\s*(.*)", t, re.S)
    return m.group(1).strip(), m.group(2).strip()
def desc_tags(d):
    d = d.replace("#MiyasNote", "#Miya's Note")
    out, seen = ["Miya's Note"], {"miya's note"}
    for h in re.findall(r"#([A-Za-z0-9]+)", d):
        if h.lower() not in seen: seen.add(h.lower()); out.append(h)
    return d, out[:8]

rows = json.loads(os.environ["SLUGS_JSON"])
groups = {}
for r in rows:
    if int(r["n"]) <= 0: continue
    m = re.match(r"^(.*)-short([0-9]?)$", r["slug"])
    base, num = (m.group(1), int(m.group(2) or 1)) if m else (r["slug"], 0)
    groups.setdefault(base, []).append((num, r["slug"]))
failed = 0
for base, items in groups.items():
    day = next_date()
    for num, slug in sorted(items):
        try:
            mf = sorted(glob.glob(f"render/{slug}/deliver/*_metadata.txt"))
            if not mf: print("skip (no metadata):", slug); continue
            title, desc = meta(mf[0])
            if title.strip().lower() in titles: print("skip (title exists):", title); continue
            dest = pathlib.Path(f"render/{slug}/.dest").read_text().strip() if os.path.exists(f"render/{slug}/.dest") else base
            outn = pathlib.Path(f"render/{slug}/.outname").read_text().strip() if os.path.exists(f"render/{slug}/.outname") else slug
            cat = "Life & Biology" if "/01." in "/" + dest else "Space & Science" if "/02." in "/" + dest else None
            h, mi = SHORT_T.get(num, (10, 0)) if num else (7, 0)
            when = day.replace(hour=h, minute=mi)
            publish_at = when.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            local = f"/tmp/{slug}.mp4"
            sh("rclone", "copyto", f"gdrive:{dest}/{outn}.mp4", local, "--drive-root-folder-id", ROOT)
            d, tags = desc_tags(desc)
            body = {"snippet": {"title": title, "description": d, "tags": tags, "categoryId": "27",
                                "defaultLanguage": "en", "defaultAudioLanguage": "en"},
                    "status": {"privacyStatus": "private", "publishAt": publish_at, "selfDeclaredMadeForKids": False,
                               "embeddable": True, "publicStatsViewable": True, "license": "youtube"}}
            req = yt.videos().insert(part="snippet,status", body=body,
                                     media_body=MediaFileUpload(local, chunksize=16 * 1024 * 1024, resumable=True))
            resp = None
            while resp is None: _, resp = req.next_chunk()
            vid = resp["id"]; titles.add(title.strip().lower())
            print("uploaded:", title, "| scheduled", when.strftime("%Y-%m-%d %H:%M KST"), "|", vid)
            pl = playlists.get(("Bite-Sized Knowledge - " if num else "Deep Dives - ") + (cat or ""))
            if pl:
                yt.playlistItems().insert(part="snippet", body={"snippet": {"playlistId": pl,
                    "resourceId": {"kind": "youtube#video", "videoId": vid}}}).execute()
            else: print("  WARN no playlist for category", cat)
            if num:
                th = sorted(glob.glob(f"render/{slug}/deliver/*_thumbnail_A.png"))
                if th: yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(th[0])).execute()
            os.remove(local)
        except HttpError as e:
            failed += 1; print("API error", e.resp.status, str(e)[:300], "| slug", slug)
            if e.resp.status in (403, 429): sys.exit(1)   # quota: stop; videos not yet uploaded stay for a manual run
        except Exception as e:
            failed += 1; print("ERROR", slug, type(e).__name__, str(e)[:300])
sys.exit(1 if failed else 0)
