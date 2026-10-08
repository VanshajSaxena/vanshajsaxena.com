# Vanshaj Saxena — portfolio

A custom Hugo portfolio with a responsive editorial layout, project case studies, technical writing, and local search. No Node build step is required. The PaperMod submodule supplies the existing Markdown shortcodes and search-index output; custom templates and assets own the visible design.

## Develop and preview

Use Hugo **Extended 0.155.3**, matching `netlify.toml`.

```sh
git submodule update --init --recursive
hugo server --environment development --disableFastRender
```

In the prepared cloud environment, Hugo is at `/workspace/.cloud-tools/hugo-0.155.3/hugo`. To keep generated resource caches outside tracked directories:

```sh
HUGO_RESOURCEDIR=/workspace/.cloud-cache/vanshajsaxena.com/resources \
  /workspace/.cloud-tools/hugo-0.155.3/hugo server \
  --environment development --bind 127.0.0.1 --port 1314 \
  --cacheDir /workspace/.cloud-cache/vanshajsaxena.com/hugo \
  --noBuildLock --disableFastRender
```

The browser preview runs locally; nothing is deployed. If a branch-connected Netlify project already exists, an eventual pull request can use its deploy-preview configuration. No deployment or remote publication was performed in this change.

## Build and validate

```sh
hugo --minify --environment production --enableGitInfo
python3 scripts/check-site.py public
```

The checker validates local navigation, anchors, media, required routes, one primary heading per page, and the search index. Browser validation also covers mobile navigation, search states, the event-loop model, mobile overflow, and representative accessibility checks.

## Share a preview without deployment

```sh
hugo --minify --environment production
python3 scripts/package-preview.py public portfolio-preview.zip
```

Unzip the archive and open `index.html`. The package rewrites local paths for direct file browsing and embeds the search index. The source website remains a normal Hugo site; the portable changes only affect the preview archive. Legacy full-size demo videos are omitted from the archive because case studies use optimized copies.

## Edit content

- `data/portfolio.json`: project summaries, contributions, technologies, technical decisions, and links.
- `content/projects/`: original project URLs and searchable descriptions; keep these aligned with the case-study data.
- `content/posts/`: technical writing. Existing article URLs are preserved.
- `content/about.md`: current role and background.
- `layouts/`: custom page templates and shared site shell.
- `assets/css/portfolio.css`, `assets/js/portfolio.js`: visual design and progressive interactions.
- `static/fonts/`: self-hosted Space Grotesk and DM Sans, with their OFL licenses.

## Content verification

The repository’s About page, project pages, and writing were reviewed. Current public source was read for Auction Hub (`96ff72c`), Fable’s staff app (`4dd8070`), and CareNote (`f32bb6b`). The owner confirmed their current SWE role at MyPay, end-to-end ownership of the website editor and employee system, the ongoing frontend rewrite, the modern merchant-portal tooling, Printit’s dormant status and lack of users, and their CareNote OCR scanner and PR-maintenance work.

No adoption metrics, current hiring availability, migration-completion claim, or internal MyPay source/screenshots are invented. CareNote images are labeled design prototypes. The Printit event-loop interaction is explicitly an illustrative model. Fable’s book artwork and Auction Hub’s contract card are original editorial illustrations, not product screenshots; the bid fields match the public API contract. MyPay’s tooling description comes from the owner-provided manifest, not a claim that its private test suites were executed here.

Direct inspection of the live portfolio and external web/API links was blocked by the environment’s egress policy. Public project Git access succeeded. GitHub and LinkedIn contact URLs were retained; their signed-in behavior was not tested.
