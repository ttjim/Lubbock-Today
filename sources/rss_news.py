"""Headline drafts from free RSS feeds listed in config.FEEDS.

Only the headline, outlet name, and a link are used. Article text is never
copied. Sensitive stories are skipped by config.SKIP_WORDS. Add your own
sarcastic take by editing the draft in the review issue before approving.
"""
import time
import random
import calendar
import datetime

import feedparser

import config

INTROS = [
    "Worth knowing in Lubbock today:",
    "File this under things that might affect you:",
    "Public service announcement, delivered with minimal enthusiasm:",
    "Someone had to read the press release so you do not have to:",
]


def too_dark(text):
    t = text.lower()
    return any(w in t for w in config.SKIP_WORDS)


def get_posts():
    cutoff = time.time() - config.LOOKBACK_HOURS * 3600
    rng = random.Random(datetime.date.today().toordinal() + 7)
    found = []
    for name, url in config.FEEDS:
        feed = feedparser.parse(url, agent=config.UA)
        for e in feed.entries:
            if not e.get("published_parsed"):
                continue
            ts = calendar.timegm(e.published_parsed)
            title = (e.get("title") or "").strip()
            if ts < cutoff or not title or not e.get("link"):
                continue
            if too_dark(title + " " + (e.get("summary") or "")):
                continue
            found.append((ts, name, title, e.link))
    found.sort(reverse=True)

    posts = []
    for ts, name, title, link in found[: config.MAX_NEWS_POSTS]:
        posts.append({
            "title": f"News: {title[:60]}",
            "text": f"{rng.choice(INTROS)}\n\n{title} ({name})",
            "source": link,
            "note": "Edit the intro to add your own sarcasm. Keep the facts exactly as the source states them.",
        })
    return posts
