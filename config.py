"""Settings you are likely to edit. Everything here is free to use."""
import os

CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "contact@example.com")
UA = f"LubbockTodayBot ({CONTACT_EMAIL})"

# Free RSS feeds to pull headlines from: (display name, feed URL).
# Find a feed by looking for an RSS icon on a site, or try adding /feed or /rss
# to the site address. Leave empty to post weather only.
FEEDS = [
    # ("City of Lubbock", "https://example.com/feed.xml"),
    # ("Visit Lubbock", "https://example.com/rss"),
]

MAX_NEWS_POSTS = 2      # max headline drafts per day
LOOKBACK_HOURS = 26     # only items published in this window (avoids repeats)

# Headlines containing any of these are skipped automatically. Sarcasm and
# tragedy never mix on this page. Add more words as you see fit.
SKIP_WORDS = [
    "killed", "dies", "died", "dead", "death", "fatal", "homicide", "murder",
    "shot", "shooting", "stabbing", "stabbed", "crash", "collision", "wreck",
    "arrest", "charged", "suspect", "missing", "amber alert", "silver alert",
    "abuse", "assault", "rape", "suicide", "overdose", "drowned", "drowning",
    "body found", "injured", "injury", "victim", "fire", "explosion",
]
