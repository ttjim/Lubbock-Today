# Lubbock Today (automation)

Every morning, GitHub Actions builds draft posts and opens one GitHub Issue per
draft. Add the `approved` label to an issue and it posts to your Facebook Page.
Close the issue to skip it. Cost: $0 (GitHub Actions free tier, NWS API,
Facebook Graph API, RSS feeds).

## What gets drafted
- Weather: every day, from the NWS API, with templated sarcasm. Active weather
  alerts produce a straight post with no jokes.
- Headlines: from the RSS feeds you list in config.py (up to 2 per day, last 26
  hours only). Sensitive stories are skipped via SKIP_WORDS. Only the headline,
  outlet, and link are used. Add your own sarcasm in the issue before approving.

## Setup
1. Create a PRIVATE GitHub repo and upload these files. (Private matters: only
   people with repo access can label an issue and trigger a post.)
2. Repo > Settings > Secrets and variables > Actions > New repository secret:
   - CONTACT_EMAIL  (your email, required by api.weather.gov)
   - FB_PAGE_ID
   - FB_PAGE_TOKEN  (long-lived Page access token)
3. Facebook: create an app at developers.facebook.com, add the Pages
   permissions (pages_manage_posts, pages_read_engagement), and generate a
   long-lived Page token for your own Page. Development mode is fine for a Page you admin.
4. Actions tab > "Daily drafts" > Run workflow to test. Approve a draft and
   confirm it posts.
5. Turn on GitHub mobile notifications so you can approve from your phone.

## Adding new content types later
Create sources/<name>.py with a get_posts() function returning a list of
{title, text, source, note} dicts, then add it to SOURCES in generate_draft.py.
Ideas: TxDOT road closures, city council agendas, events calendars, a
"this day in Lubbock history" list you write yourself.

## Notes
- Cron runs in UTC and does not shift for daylight saving.
- Check Meta's current Graph API version and set GRAPH_VERSION if needed.
