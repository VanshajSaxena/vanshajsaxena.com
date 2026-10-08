#!/usr/bin/env python3
"""Package a Hugo build for direct file browsing without publishing it."""
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

if len(sys.argv) != 3:
    raise SystemExit("Usage: python3 scripts/package-preview.py BUILD_DIR OUTPUT.zip")
source = Path(sys.argv[1]).resolve()
archive = Path(sys.argv[2]).resolve()
if not (source / "index.html").is_file():
    raise SystemExit("A complete Hugo build is required")

with tempfile.TemporaryDirectory(prefix="portfolio-preview-") as temp:
    root = Path(temp) / "site"
    shutil.copytree(source, root)
    # Original demo files remain in the repository, but the case studies use
    # smaller, fast-start web encodes. Do not duplicate the large originals.
    for name in ["FableForMembersandUsers.mp4", "FableForAdminsandLibrarians.mp4"]:
        path = root / "projects" / "fable" / name
        if path.exists():
            path.unlink()
    entries = json.loads((root / "index.json").read_text())
    for entry in entries:
        path = urlsplit(entry["permalink"]).path.lstrip("/")
        target = root / path
        if target.is_dir() or path.endswith("/"):
            target /= "index.html"
        entry["previewPath"] = os.path.relpath(target, root / "search")
    search_data = json.dumps(entries).replace("</", "<\\/")

    class PortableHTML(HTMLParser):
        def __init__(self, page):
            super().__init__(convert_charrefs=False)
            self.page = page
            self.output = []
        def handle_starttag(self, tag, attrs):
            rewritten = []
            for key, value in attrs:
                if value is not None and key in ["href", "src", "poster", "data-index"] and value.startswith("/") and not value.startswith("//"):
                    url = urlsplit(value)
                    target = root / unquote(url.path.lstrip("/"))
                    if target.is_dir() or url.path.endswith("/"):
                        target /= "index.html"
                    value = os.path.relpath(target, self.page.parent)
                    if url.query:
                        value += "?" + url.query
                    if url.fragment:
                        value += "#" + url.fragment
                rewritten.append(key if value is None else f'{key}="{escape(value, quote=True)}"')
            self.output.append("<" + tag + (" " + " ".join(rewritten) if rewritten else "") + ">")
        def handle_startendtag(self, tag, attrs):
            self.handle_starttag(tag, attrs)
        def handle_endtag(self, tag):
            if tag == "head" and self.page.parent.name == "search":
                self.output.append("<script>window.__PORTFOLIO_SEARCH_INDEX__=" + search_data + ";</script>")
            self.output.append(f"</{tag}>")
        def handle_data(self, data):
            self.output.append(data)
        def handle_entityref(self, name):
            self.output.append("&" + name + ";")
        def handle_charref(self, name):
            self.output.append("&#" + name + ";")
        def handle_decl(self, decl):
            self.output.append("<!" + decl + ">")
        def handle_comment(self, data):
            self.output.append("<!--" + data + "-->")

    for page in root.rglob("*.html"):
        parser = PortableHTML(page)
        parser.feed(page.read_text())
        page.write_text("".join(parser.output))
    for css in root.rglob("*.css"):
        text = css.read_text()
        def font_url(match):
            return 'url("' + os.path.relpath(root / match.group(1).lstrip("/"), css.parent) + '")'
        text = re.sub(r'url\([\"\']?(/fonts/[^)\"\']+)[\"\']?\)', font_url, text)
        css.write_text(text)
    # Portable-only enhancement uses embedded search data under file://.
    js_source = Path(__file__).resolve().parent.parent / "assets/js/portfolio.js"
    text = js_source.read_text().replace("let entries;", "let entries = window.__PORTFOLIO_SEARCH_INDEX__;")
    text = text.replace("link.href = url.pathname + url.search + url.hash;", "link.href = entry.previewPath || (url.pathname + url.search + url.hash);")
    for js in (root / "js").glob("portfolio*.js"):
        js.write_text(text)
    # Rewriting assets invalidates original fingerprints; the live site keeps
    # its integrity attributes, but portable files do not use network SRI.
    for page in root.rglob("*.html"):
        page.write_text(re.sub(r' integrity="[^"]*"', "", page.read_text()))
    (root / "PREVIEW-README.txt").write_text("Unzip this archive, then open index.html in a browser. Project pages, writing, navigation, local fonts, videos, and search work without deployment. Contact links open external services. This is a review artifact, not a deployment.\n")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
        for file in root.rglob("*"):
            if file.is_file():
                package.write(file, file.relative_to(root))
print(f"Preview saved: {archive} ({archive.stat().st_size / 1024 / 1024:.1f} MiB)")
