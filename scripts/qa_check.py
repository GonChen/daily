#!/usr/bin/env python3
"""Daily brief QA gate. Usage: python3 scripts/qa_check.py YYYY-MM-DD

Checks structure, anchors, local links, index wiring for the dated archive
page before commit. Exits 1 with a FAIL list on any hard error.
Content quality is NOT checked here -- that stays an editorial judgment.
"""
import os
import re
import sys
import urllib.parse

REQUIRED_IDS = [
    "summary", "top5", "chips", "frameworks", "kernels", "models",
    "tools", "acceleration", "papers", "macro", "deep", "watch",
]


def main() -> int:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        print("usage: qa_check.py YYYY-MM-DD")
        return 2
    date = sys.argv[1]
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    errors, warns = [], []

    page = os.path.join(root, "docs", "archive", f"{date}.html")
    if not os.path.exists(page):
        print(f"FAIL missing {page}")
        return 1
    html = open(page, encoding="utf-8").read()

    # strip script/style blocks: JS template literals like ${href} are not HTML links
    scan = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)

    ids = set(re.findall(r'id="([^"]+)"', scan))
    for rid in REQUIRED_IDS:
        if rid not in ids:
            errors.append(f"missing required section id={rid}")

    for href in sorted(set(re.findall(r'href="#([^"]+)"', scan))):
        if href not in ids:
            errors.append(f"broken internal anchor #{href}")

    for href in set(re.findall(r'href="([^"]+)"', scan)):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = urllib.parse.unquote(href.split("#")[0])
        if not path:
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(page), path))
        if not os.path.exists(target):
            errors.append(f"broken local link {href}")

    for href in set(re.findall(r'href="(http[^"]+)"', scan)):
        if not href.startswith("https://"):
            warns.append(f"non-https external link {href}")

    if "viewport" not in scan:
        errors.append("missing mobile viewport meta")

    if "index.html" not in scan:
        errors.append("archive page has no link back to archive index")

    aidx = os.path.join(root, "docs", "archive", "index.html")
    if not os.path.exists(aidx):
        errors.append("missing docs/archive/index.html")
    else:
        ai = open(aidx, encoding="utf-8").read()
        if f"{date}.html" not in ai:
            errors.append("archive index has no entry for this date")

    home = os.path.join(root, "docs", "index.html")
    if not os.path.exists(home):
        errors.append("missing docs/index.html")
    else:
        hi = open(home, encoding="utf-8").read()
        # home is a full copy of the current issue (date in title/body) or links to it
        if f"archive/{date}.html" not in hi and date not in hi:
            errors.append("docs/index.html does not reference today's issue")

    ledger = os.path.join(root, "research", f"{date}-product-facts.md")
    if not os.path.exists(ledger):
        errors.append(f"missing research ledger {os.path.basename(ledger)}")

    for w in warns:
        print("WARN", w)
    if errors:
        for e in errors:
            print("FAIL", e)
        return 1
    print(f"OK {date}: {len(REQUIRED_IDS)} sections, anchors, local links, "
          f"index wiring, ledger all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
