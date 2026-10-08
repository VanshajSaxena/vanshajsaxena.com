#!/usr/bin/env python3
"""Validate a generated Hugo site using only the Python standard library."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
if not root.is_dir():
    raise SystemExit(f"Build directory does not exist: {root}")

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.h1 = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        for name in ("href", "src", "poster", "data-index"):
            if attrs.get(name):
                self.links.append(attrs[name])

pages = {}
for path in root.rglob("*.html"):
    parser = Links()
    parser.feed(path.read_text())
    pages[path] = parser
errors = []
checked = 0
for page, parser in pages.items():
    if parser.h1 != 1:
        errors.append(f"{page.relative_to(root)}: expected one h1, found {parser.h1}")
    for link in parser.links:
        parsed = urlsplit(link)
        if parsed.scheme or parsed.netloc:
            continue
        path = unquote(parsed.path)
        target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
        if not path:
            target = page
        if target.is_dir() or path.endswith("/"):
            target = target / "index.html"
        target = target.resolve()
        checked += 1
        if not target.is_file():
            errors.append(f"{page.relative_to(root)}: missing target {link}")
        elif parsed.fragment and target in pages and parsed.fragment not in pages[target].ids:
            errors.append(f"{page.relative_to(root)}: missing anchor {link}")
index = json.loads((root / "index.json").read_text())
assert index and all(entry.get("title") and entry.get("content") for entry in index), "Search entries must have titles and content"
for expected in ["/projects/mypay/", "/projects/printit/", "/projects/auction-system/", "/projects/fable/", "/projects/carenote/", "/about/", "/posts/", "/search/"]:
    if not (root / expected.lstrip("/") / "index.html").is_file():
        errors.append(f"Required route missing: {expected}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"Passed: {len(pages)} HTML pages, {checked} local links/assets/anchors, {len(index)} searchable entries.")
