# Economic Indicators Terminal

A Bloomberg terminal-style dashboard for CPI, PPI, employment, and a News & Analysis tab. The page boots from an embedded snapshot and can switch to live FRED data when you save a key.

Built by **Ghost Strategies LLC**

---

## Features

- **Seven views** — Overview, CPI Detail, PPI Detail, Employment, Projections, Correlation Matrix, News & Analysis
- **Embedded snapshot** — August 2026 BLS/BEA figures where a release was actually fetched, with the source and date in `snapshot-sources.md`. October 2025 was not published for CPI and unemployment, so those quarters are blank
- **Live FRED** — optional. A saved key recomputes headline quarterly, annual, and latest values from monthly levels. "LIVE" badges appear only after that load succeeds
- **BEA GDP** — the snapshot shows BEA's real GDP series as carried on FRED. The badge says BEA only after the BEA API itself returns a table
- **Charts** — Chart.js 4.4.1 and the annotation plugin are in `vendor/`, so the charts do not depend on a CDN
- **Correlation matrix** — Pearson correlation of the levels of the last 8 shared quarters in the data the page is showing
- **Projections** — the Q3/Q4 paths and the scenario table are an illustrative scenario from the previous file. The bands use a fixed formula and are labeled that way. They are not a statistical interval and not an FOMC or CBO forecast
- **News & Analysis** — with an OpenRouter key, a router picks a tier, the page computes any charted statistic, and a narrator writes from those facts plus web results. Without a key, the tab explains that design and shows a labeled example layout
- **BLS release calendar** — 2026 dates from the BLS schedule, with upcoming rows still upcoming

## Indicators Covered

| Category | Indicators |
|----------|-----------|
| **CPI** | All Items (YoY, MoM), Core (ex Food & Energy), component rows. Education, Recreation, and Other Goods are still the March 2026 rows and are labeled |
| **PPI** | Final Demand, Core, and the refreshed food / energy / ex-food-and-energy rows. The other PPI rows are March 2026 and labeled |
| **Employment** | Nonfarm Payrolls, Unemployment (U-3), U-6, LFPR, Avg Hourly Earnings, JOLTS. The sector table is the March 2026 snapshot and is labeled |
| **GDP** | Real GDP, quarterly percent change, seasonally adjusted annual rate |

---

## Project Structure

```
economic-terminal/
├── index.html                                    # The dashboard
├── vendor/                                       # Chart.js and the annotation plugin
├── server.py                                     # Localhost-only static server and API proxy
├── snapshot-sources.md                           # Series, method, and release date for the snapshot
├── cloudflare-worker-guide.html                  # Example Worker (you deploy it yourself)
├── api-guide.html                                # API key tester
├── scripts/run-stats-tests.mjs                   # Headless run of the embedded test suite
├── scripts/scan-secrets.sh                       # Credential-pattern scan
├── scripts/install-hooks.sh                      # Opt in to the pre-push scan
├── .githooks/pre-push                            # Used only after install-hooks.sh
├── .github/workflows/tests.yml                   # Runs the suite and the scanner
├── README.md
├── LICENSE
└── .gitignore
```

## Getting Started

1. Open `index.html` in a browser, or run `python server.py` and open http://127.0.0.1:8080.
2. `Economic_Terminal_Instructional_Guide.pdf` is the longer teaching guide. It predates the News tab and this refresh, so where it disagrees with this README, the README and `snapshot-sources.md` are the current description.
3. `api-guide.html` walks through saving a FRED key.

The dashboard has an **API** button in the top-right. Keys stay in this browser's `localStorage`. They are not in the source file.

| API | What it powers | How the browser reaches it |
|-----|----------------|----------------------------|
| **FRED** | CPI, PPI, employment, the headline series | `server.py` on localhost, or a Cloudflare Worker URL you paste in settings. Direct calls fail CORS on a public host |
| **BEA** | Real GDP, when the request succeeds | Direct. CORS works. A saved key that does not return data does not flip the badge to BEA |
| **BLS** | Stored for same-day use | The page does not call BLS from the browser. FRED carries the BLS series |
| **OpenRouter** | News & Analysis | Direct, from the News settings drawer |
| **Twelve Data** | News price history. This is the provider that works | Direct. Set the key in News settings |
| **Alpha Vantage** | Fallback prices | `outputsize=compact` (about 100 sessions). `outputsize=full` is a paid plan and is not requested |
| **Stooq** | Last-resort prices | Only through `server.py` on localhost. On the public site the page does not call Stooq, because the browser is blocked by CORS. Stooq also requires its own key |

`server.py` listens on `127.0.0.1` only. It does not serve `.git` or the private spec filenames.

## News & Analysis without a key

Open the News tab. It describes the router, the in-page statistics, and the narrator, and it shows an example layout. The example table uses dashes. The paragraph is marked EXAMPLE. It is not a model answer.

To drop in a real recording later:

1. Save a GIF, PNG, or MP4 of a real run next to `index.html`, for example `news-sample.gif`.
2. In `index.html`, set `NEWS_RECORDED_SAMPLE` to that filename. It is near the top of the News script.
3. Commit the media file with the change.

Leave the constant empty until the file is a real session. The example layout stays labeled either way.

## Tests

The checks live in `runStatsTests()` inside `index.html`. From the page console that returns the pass/fail counts.

Headless, in a US timezone:

```
npm install --no-save puppeteer-core
TZ=America/Chicago node scripts/run-stats-tests.mjs
```

GitHub Actions runs that command and `scripts/scan-secrets.sh`.

## Secret scan

`scripts/scan-secrets.sh` flags credential-shaped strings. It does not flag the `sk-or-...` placeholder in the settings form.

The hook in `.githooks/pre-push` runs only after:

```
sh scripts/install-hooks.sh
```

Git does not set `core.hooksPath` on clone. The Actions workflow runs the scanner even if you never install the hook.

## Tech stack

- HTML, CSS, and JavaScript in one file. No build step. GitHub Pages can serve the tree as-is
- Chart.js 4.4.1 and chartjs-plugin-annotation 3.0.1 from `vendor/`
- Google Fonts for JetBrains Mono and IBM Plex Sans. If that request is blocked, the browser uses its own sans and monospace fonts. The layout still renders
- A Content-Security-Policy meta tag in `index.html`. `vercel.json` sends the same policy as a header, which is what makes `frame-ancestors` take effect on Vercel. GitHub Pages uses the meta tag

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Ghost Strategies LLC** | Economic Indicators Terminal v2.2
