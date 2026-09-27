# Economic Indicators Terminal — Orientation

Single-file dashboard for US economic indicators (CPI, PPI, employment) plus a News & Analysis tab. CSS, markup, and JS live in `index.html` (about 3,900 lines). Chart.js and the annotation plugin are plain files in `vendor/`. No build step, no framework. `server.py` is an optional local static server with CORS proxy endpoints. It binds to `127.0.0.1` only.

## Tabs

Seven views driven by `data-view` on `.nav-tab` divs: **Overview, CPI Detail, PPI Detail, Employment, Projections, Correlation Matrix, News & Analysis**. `renderView(view)` (search `function renderView`) destroys all charts, wipes `#mainDashboard`, and calls one `renderX(container)` function per tab. Persistent shell outside the tab system: top bar (clock, connection badge, API settings modal), ticker, six summary cards, footer.

## Data model

App boots from the embedded `DATA` object (search `const DATA`). `snapshot-sources.md` records the series id, the method, and the BLS release date for the refreshed figures. October 2025 is missing at the source for CPI and unemployment, so those series omit 2025-Q4 and the 2025 annual.

`latest` is the latest monthly observation. Quarterly price figures are the year-over-year change in the 3-month average index. Live FRED uses the same aggregators (`aggregateIndexYoY`, `aggregateLevelAverage`, `aggregatePayrollChange`), so a key does not replace that definition with FRED's quarterly-frequency series.

`projected` Q3/Q4 values are the previous file's illustrative scenario. Overview charts do not plot them. The projection bands are the fixed formula `±(0.3 + 0.15 × step)` and the UI says so.

The correlation matrix is Pearson correlation of levels over the last 8 shared quarters (`quarterlyPearson`). It is not the daily-return correlation used by the News tab.

A panel "LIVE" badge comes from `liveBadge()` and renders only when `isLiveData` is true. Static mode says "Snapshot". The top-bar badge says "BEA" only when `DATA.gdp.live` is true, which happens after `applyBeaGdp()` parses NIPA T10101 line 1. A saved BEA key by itself does not.

## Data sources & fetch layer

No shared fetch wrapper; two ad hoc fetchers:

- `fetchFRED(seriesId, units, freq, start)` → `[{date, value}]`, `[]` on error. URL built by `buildFredUrl()` with proxy priority: (1) Cloudflare Worker URL from localStorage → (2) `/api/fred?...` on localhost (`server.py`) → (3) direct to `api.stlouisfed.org` (fails on CORS remotely).
- `fetchBEA(tableName, frequency, year)` → raw `BEAAPI.Results.Data` or `null`. Called direct (BEA supports CORS). `loadAllData()` passes T10101 through `applyBeaGdp()`.
- BLS: the key is stored and is not called from the browser. FRED mirrors the BLS series.
- `loadAllData()` requests monthly levels (not FRED's quarterly percent-change frequency) for the headline series, mutates `DATA` in place, and re-renders. `isLiveData` flips only if at least one series applied.

Dates are parsed from the `YYYY-MM-DD` string (`parseFredDateParts`, `quarterKeyFromDate`). `new Date('YYYY-MM-DD')` is UTC midnight and shifts the month west of UTC. Do not put that back into the aggregators.

**Known trap:** `testConnection()` duplicates the proxy-routing logic inline instead of calling `buildFredUrl()`. Changes to routing must be made in both places. API error text in that panel goes through `escapeHtml()`.

## Caching

The dashboard's FRED refresh has no response cache. Every live load and the 5-minute refresh refetches the headline series.

The News tab does cache. IndexedDB database `gs_cache`, keys `prices:{ticker}:{start}:{end}` and `fred:{id}:lin:{freq}:{start}:{end}`, 20-hour TTL. Expired rows are not evicted. That cache does not cover `loadAllData()`.

localStorage holds config only: `ghost_fred_api_key`, `ghost_bea_api_key`, `ghost_bls_api_key`, `ghost_proxy_url`, and `gs_keys` for the News tab. No API keys in the file.

## State & charts

Global mutable `DATA` plus module-scope `isLiveData`, `currentView`, `chartInstances`, `fredRefreshInterval`. Chart.js **4.4.1** and chartjs-plugin-annotation **3.0.1** load from `vendor/`. `createChart()` no-ops with a short message if `Chart` is missing, so a failed script does not blank the tables. Every chart must register in `chartInstances` keyed by canvas id — `renderView()` destroys them on tab switch; unregistered charts leak and throw "canvas already in use". Percent axes use `pctAxisTick` (one decimal).

Timers: 1-second clock, and a 5-minute refresh only while live data is loaded. There is no cosmetic flash in static mode. The footer cadence reads "off" until a live load succeeds.

## Styling

Design tokens are CSS variables in `:root`. Dark navy ink backgrounds (`#0a0e14`–`#151b23`), **orange `#ff9500` primary accent**; cyan is the News tab accent. Fonts: JetBrains Mono + IBM Plex Sans (Google Fonts). Chart colors are hardcoded hex, not tokens. `html, body` set `overflow-x: hidden`. Wide tables sit in `.matrix-scroll`.

## Deploy

Local: `python server.py` → http://127.0.0.1:8080 (proxies `/api/fred`, `/api/bea`, `/api/stooq`, POST `/api/bls`). The process binds to loopback and returns 404 for `.git` and the private spec filenames.

Remote static hosting works for the snapshot. FRED from a public host needs a user-configured Cloudflare Worker URL. The example in `cloudflare-worker-guide.html` allows only `https://economic.ghoststrategies.io`, rate-limits per isolate (about 60 requests per minute per IP), and sends `Cache-Control: private, no-store` because the URL contains `api_key`. You deploy that Worker yourself. It has no Stooq route.

Content-Security-Policy is a meta tag in `index.html` (what GitHub Pages can serve) and the same policy as a header in `vercel.json` (`frame-ancestors` only works as a header). `script-src` allows `'unsafe-inline'` because the page uses inline scripts and `onclick`.

## Tests

`runStatsTests()` in `index.html` is 37 cases: the stats helpers, the date parse, the gap-quarter rule, payroll changes, half-up rounding, and `quarterlyPearson`. Run it from the console, or `TZ=America/Chicago node scripts/run-stats-tests.mjs` (needs `puppeteer-core` and Chrome). The Chicago run also checks that `new Date('2025-01-01').getMonth()` is 11 while `quarterKeyFromDate` stays on 2025-Q1. GitHub Actions runs that job. Keep the suite passing and add a case when you change an aggregator.

`sh scripts/install-hooks.sh` points this clone at `.githooks/pre-push`. Git will not do that on clone. The Actions secret-scan job runs regardless.

## Edit carefully

1. **`loadAllData()`** — live data replaces quarterly/annual/latest via the aggregators and deletes projected keys that collide with a new actual (`dropStaleProjections`). Do not write FRED's pre-aggregated quarterly percent change back into `quarterly`.
2. **`renderView()` / `chartInstances`** — new tabs plug into the destroy-then-render cycle with unique canvas ids, and they call `createChart` rather than `new Chart`.
3. **Proxy routing duplication** — `buildFredUrl()` vs the inline copy in `testConnection()`.
4. **Date strings** — `parseFredDateParts` only. `localISODate()` for "today".

## News & Analysis tab

Self-contained module in index.html (search "NEWS & ANALYSIS TAB"). Router LLM call (default `moonshotai/kimi-k2.6`, JSON plan including `effort: fast|standard|deep`) then narrator call, tier-routed by effort: fast = `deepseek/deepseek-v4-pro:online` (4 web results, the default tier), standard = `moonshotai/kimi-k3:online` (6), deep = `anthropic/claude-sonnet-5:online` (6). All use the OpenRouter web plugin and SSE-stream into the results div. The LLM never produces charted numbers or unsourced facts. Unknown or missing effort falls back to fast. The router user message includes today's local date.

Keys and model prefs are in localStorage `gs_keys`. Monthly spend is under `gs_spend_YYYY-MM`, with a $5 warning, a $10 click-through guard, and a $20 baseline.

With no OpenRouter key and no in-memory result, `newsExampleLayout()` explains the three steps and shows a layout labeled as an example. `NEWS_RECORDED_SAMPLE` (empty string) is the slot for a real GIF, image, or MP4. See the README section "News & Analysis without a key". `newsLastHTML` is memory only and does not survive a reload.

Phase 2 data layer: `getDailyCloses(ticker, startISO, endISO)` tries Twelve Data, then Alpha Vantage `outputsize=compact` (sets `truncated` when the window starts before the first bar), then Stooq. Stooq throws a clear error on a remote host and is not requested there. Keys: `gs_keys.twelvedata`, `.alphavantage`, and optional `.stooq` for the local proxy. Comparison charts use the vendored annotation plugin for divergence-window bands. Chart config persists in `newsLastChart` for tab-switch remount via `mountNewsChart()`.

Phases 3–4 (presets, morning brief, save-as-note, event overlay, thesis watch, escalation ladder) are not built.

## Adding a new tab (safe pattern)

Four attach points: (1) new `.nav-tab` div with `data-view`, (2) new `case` in `renderView()` switch, (3) new `renderX(container)` function that owns its panels and registers charts in `chartInstances`, (4) its own data slice (new `DATA` key or separate store — `loadAllData()` will not touch it unless you add a call). Don't touch summary cards, ticker, `loadAllData()`, or proxy routing from a new tab.
