"""Runs every source and writes one draft per post into ./drafts.

Add a new content type by creating sources/<name>.py with a get_posts()
function that returns a list of dicts: {title, text, source, note}, then
add the module to SOURCES below.
"""
import sys
import pathlib
import datetime

from sources import weather, rss_news

SOURCES = [weather, rss_news]


def render(item):
    parts = ["<!-- POST_START -->", item["text"]]
    if item.get("source"):
        parts.append(f"\nSource: {item['source']}")
    parts.append("<!-- POST_END -->\n")
    parts.append("**To publish:** edit the text above if you want, then add the `approved` label.")
    parts.append("**To skip:** close this issue.")
    if item.get("note"):
        parts.append(f"\n> {item['note']}")
    return "\n".join(parts)


def main():
    out = pathlib.Path("drafts")
    out.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    n = 0
    for mod in SOURCES:
        try:
            items = mod.get_posts()
        except Exception as exc:  # one broken source should not stop the others
            print(f"{mod.__name__} failed: {exc}", file=sys.stderr)
            continue
        for item in items:
            n += 1
            (out / f"{n:02d}.md").write_text(render(item))
            (out / f"{n:02d}.title").write_text(f"{item['title']} ({today})")
    if n == 0:
        sys.exit("No drafts produced. Check the source errors above.")
    print(f"Wrote {n} draft(s).")


if __name__ == "__main__":
    main()
