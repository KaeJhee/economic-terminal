# GHOST STRATEGIES — Economic Indicators Terminal

A Bloomberg terminal-style dashboard for tracking CPI, PPI, and employment data with quarterly/annual views, projections, correlation matrices, and scenario analysis.

Built by **Ghost Strategies LLC**

---

## Features

- **Real-Time Layout** — Scrolling ticker bar, auto-refresh cycle with flash updates, and a live clock
- **6 Navigation Views** — Overview, CPI Detail, PPI Detail, Employment, Projections, Correlation Matrix
- **Quarterly + Annual Data** — Full data tables spanning 2020–2026 with projected quarters highlighted
- **Charts** — CPI/PPI trend lines with projection dashes, NFP bar charts, shelter deep dive, wage vs. inflation, PPI-to-CPI pipeline spread, confidence bands
- **Heat Maps & Matrices** — CPI component intensity map, cross-indicator correlation matrix, directional change matrix, Z-score deviation heat map
- **Scenario Analysis** — Base / Upside / Downside projections for all key indicators through Q4 2026
- **BLS Release Calendar** — Upcoming data release dates with status indicators
- **Dark Terminal Aesthetic** — JetBrains Mono + IBM Plex Sans, dark background, orange accent system

## Indicators Covered

| Category | Indicators |
|----------|-----------|
| **CPI** | All Items (YoY, MoM), Core (ex Food & Energy), 9 sub-components with weights |
| **PPI** | Final Demand (YoY, MoM), Core (ex F&E&T), Goods vs Services breakdown |
| **Employment** | Nonfarm Payrolls, Unemployment Rate (U-3), U-6, LFPR, Avg Hourly Earnings, JOLTS, 10 sector breakdowns |

---

## Project Structure

```
economic-terminal/
├── index.html                                    # The dashboard (open this!)
├── server.py                                     # Local dev server with FRED/BLS CORS proxy
├── api-guide.html                                # Interactive API key tester + connection guide
├── Economic_Terminal_Instructional_Guide.pdf     # 43-page teaching guide
├── README.md                                     # This file
├── LICENSE                                       # MIT License
└── .gitignore                                    # Git ignore rules
```

## Getting Started — Recommended Reading Order

1. **`Economic_Terminal_Instructional_Guide.pdf`** — Read this first if you want to deeply understand how the dashboard is built. 36 pages covering HTML/CSS/JavaScript fundamentals, the data model, Chart.js, API integration, and deployment. Written for someone with zero web development background.
2. **`index.html`** — Open in any browser to see the dashboard immediately.
3. **`api-guide.html`** — Open in a browser to test your FRED API key and follow the live data integration walkthrough.
4. **`README.md`** (this file) — Quick reference for running locally and deploying to GitHub Pages.

---


## Download Links — Quick Reference

| Tool | Download Link | What It's For |
|------|--------------|---------------|
| **Python** | [python.org/downloads](https://www.python.org/downloads/) | Local dev server (`python -m http.server`) |
| **Node.js** | [nodejs.org/en/download](https://nodejs.org/en/download) | Alternative server, npm package manager |
| **VS Code** | [code.visualstudio.com/download](https://code.visualstudio.com/download) | Code editor with Live Server extension |
| **Git** | [git-scm.com/downloads](https://git-scm.com/downloads) | Version control, push to GitHub |
| **GitHub** | [github.com](https://github.com) | Repository hosting, GitHub Pages |
| **FRED API Key** | [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html) | Live economic data |
| **BLS API Key** | [data.bls.gov/registrationEngine](https://data.bls.gov/registrationEngine/) | Same-day BLS release data |

---

## Connecting Live Data

The dashboard has a built-in **API** button in the top-right corner. Click it to open the settings panel where you enter your API keys. Keys are stored in your browser's `localStorage` — they never appear in your source code, Git history, or GitHub repository.

**No code editing required.** Just paste your keys, click Save & Connect, and the dashboard switches from static to live data automatically.

| API | What It Powers | Browser Support | Registration |
|-----|---------------|------|-------------|
| **FRED** (primary) | CPI, PPI, Employment, all indicators | Needs proxy (no CORS) | [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html) |
| **BEA** | GDP, PCE, National Accounts | Direct (CORS OK) | [apps.bea.gov/api/signup](https://apps.bea.gov/api/signup/) |
| **BLS** | Same-day release data | Needs proxy (no CORS) | [data.bls.gov/registrationEngine](https://data.bls.gov/registrationEngine/) |

**CORS and proxies explained:** FRED and BLS do not return CORS headers, which means browsers block direct JavaScript calls to their APIs. The solution:
- **Locally:** Run `python server.py` instead of `python -m http.server`. It proxies API calls automatically.
- **GitHub Pages:** Deploy a free Cloudflare Worker (see `api-guide.html`) and paste its URL in the settings panel.
- **BEA** works directly in the browser with no proxy needed.

---

## Tech Stack

- **HTML5 / CSS3 / Vanilla JavaScript** — Zero dependencies, no build step
- **Chart.js 4.4.1** — Loaded from CDN for all visualizations
- **Google Fonts** — JetBrains Mono + IBM Plex Sans loaded from CDN

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Ghost Strategies LLC** | Economic Indicators Terminal v2.1
