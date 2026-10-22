"""Publishes the approved text from an issue body to the Facebook Page.

Env vars:
  ISSUE_BODY   the issue body (set by the workflow)
  PAGE_ID      Facebook Page ID
  PAGE_TOKEN   long-lived Page access token
  GRAPH_VERSION (optional, defaults to v21.0; check Meta's current version)
"""
import os
import re
import sys
import requests

body = os.environ.get("ISSUE_BODY", "")
m = re.search(r"<!-- POST_START -->\s*(.*?)\s*<!-- POST_END -->", body, re.S)
if not m or not m.group(1).strip():
    sys.exit("No post text found between the markers.")

text = m.group(1).strip()
version = os.environ.get("GRAPH_VERSION", "v21.0")
r = requests.post(
    f"https://graph.facebook.com/{version}/{os.environ['PAGE_ID']}/feed",
    data={"message": text, "access_token": os.environ["PAGE_TOKEN"]},
    timeout=30,
)
print(r.status_code, r.text)
r.raise_for_status()
