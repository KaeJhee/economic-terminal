# Economic Indicators Terminal — Orientation

Single-file dashboard for US economic indicators (CPI, PPI, employment). Everything —
CSS, markup, JS — lives in `index.html` (~2,370 lines). No build step, no framework.
`server.py` is an optional local static server with CORS proxy endpoints.

## Tabs

Seven views driven by `data-view` on `.nav-tab` divs: **Overview, CPI Detail, PPI Detail,
Employment, Projections, Correlation Matrix, News & Analysis**. `renderView(view)` destroys all charts,
wipes `#mainDashboard`, and calls one `renderX(container)` function per tab. Persistent
shell outside the tab system: top bar (clock, connection badge, API settings modal),
ticker, six summary cards, footer.

## Data model

App boots from a hardcoded static `DATA` object (~line 696). Live data loads only if a
FRED key is saved, and only overwrites the headline `quarterly`/`annual`/`latest` series —
`projected`, components, sector tables, shelter chart, and correlation matrix stay static.
"LIVE" panel badges are hardcoded decoration, shown even in static mode.

## Data sources & fetch layer

No shared fetch wrapper; two ad hoc fetchers:

- `fetchFRED(seriesId, units = 'pc1', freq = 'q', start = '2020-01-01')` → `[{date, value}]`,
  `[]` on error. URL built by `buildFredUrl()` with proxy priority:
  (1) Cloudflare Worker URL from localStorage → (2) `/api/fred?...` on localhost
  (server.py) → (3) direct to `api.stlouisfed.org` (fails on CORS remotely).
- `fetchBEA(tableName, frequency = 'Q', year = 'X')` → raw `BEAAPI.Results.Data` or `null`.
  Called direct (BEA supports CORS). Currently fetched but only console-logged — no BEA
  data renders in the UI.
- BLS: key is collected/stored but never called from the browser. FRED mirrors BLS data.
- `loadAllData()` fires 16 parallel `fetchFRED` calls, mutates `DATA` in place, re-renders.

**Known trap:** `testConnection()` duplicates the proxy-routing logic inline instead of
calling `buildFredUrl()`. Changes to routing must be made in both places.

## Caching

**None.** No response caching, no TTL — every load and 5-min refresh refetches all series.
localStorage holds config only: `ghost_fred_api_key`, `ghost_bea_api_key`,
`ghost_bls_api_key`, `ghost_proxy_url`. No API keys in the file; safe to push public.

## State & charts

Global mutable `DATA` plus module-scope `isLiveData`, `currentView`, `chartInstances`,
`fredRefreshInterval`. Chart.js **4.4.1** from cdnjs CDN; configs inline in each render
function. Every chart must register in `chartInstances` keyed by canvas id — `renderView()`
destroys them all on tab switch; unregistered charts leak and throw "canvas already in use".
Timers: 1s clock, 60s cosmetic flash (static mode), 5-min live refresh.

## Styling

Design tokens are CSS variables in `:root` (~line 10). Dark navy ink backgrounds
(`#0a0e14`–`#151b23`), **orange `#ff9500` primary accent**; cyan is minor. Fonts:
JetBrains Mono + IBM Plex Sans (Google Fonts). Chart colors are hardcoded hex, not tokens.

## Deploy

Local: `python server.py` → http://localhost:8080 (proxies `/api/fred`, `/api/bea`,
POST `/api/bls`). Remote (e.g. GitHub Pages): static hosting works, but FRED requires a
user-configured Cloudflare Worker proxy URL (see `cloudflare-worker-guide.html`).

## Edit carefully

1. **`loadAllData()` static/live merge (~2237–2344)** — live data wholesale-replaces
   quarterly/annual maps; charts bridge actual→projected via array-length math that
   depends on quarterly and projected keys staying disjoint and ordered.
2. **`renderView()` / `chartInstances` lifecycle (~1027–1058)** — new tabs must plug into
   the destroy-then-render cycle with unique canvas ids.
3. **Proxy routing duplication** — `buildFredUrl()` vs the inline copy in `testConnection()`.

## News & Analysis tab (Phase 1 of news-analysis-tab-build-spec.md)

Self-contained module in index.html (search "NEWS & ANALYSIS TAB"). Router LLM call
(default `moonshotai/kimi-k2.6`, JSON plan incl. `effort: fast|standard|deep`) then
narrator call, tier-routed by effort: fast = `deepseek/deepseek-v4-pro:online` (4 web
results, the default tier), standard = `moonshotai/kimi-k3:online` (6), deep =
`anthropic/claude-sonnet-5:online` (6); all use the OpenRouter web plugin and
SSE-stream into the results div — the LLM never produces charted numbers or unsourced
facts. Unknown/missing effort falls back to fast. Keys/model
prefs in localStorage `gs_keys` (JSON object);
monthly spend under `gs_spend_YYYY-MM`, $5 warn / $10 click-through guard, $20 baseline.
Uses cyan (`--accent-cyan`) as its signature accent within the existing palette (a
deliberate call: the spec's ink/teal house style was set aside to match the terminal).

Phase 2 (data layer) is built: `getDailyCloses(ticker, startISO, endISO)` wraps
Stooq (proxied via `/api/stooq` on localhost; CORS-blocked remotely) then Twelve Data
then Alpha Vantage (keys in `gs_keys.twelvedata`/`.alphavantage`); IndexedDB cache
db `gs_cache`, keys `prices:{ticker}:{start}:{end}` and `fred:{id}:lin:d:{start}`,
20h TTL. Pure stats module (normalizeSeries, totalReturnPct, cagrPct, maxDrawdown,
annualizedVolPct, rollingRelative, divergenceWindows, correlationDaily) has embedded
fixture tests: run `runStatsTests()` in the console, must stay 20/20. Comparison
charts use chartjs-plugin-annotation (CDN) for divergence-window bands; chart config
persists in `newsLastChart` for tab-switch remount via `mountNewsChart()`.
Phases 3-4 (presets, morning brief, save-as-note, event overlay, thesis watch,
escalation ladder) not built yet.

## Adding a new tab (safe pattern)

Four attach points: (1) new `.nav-tab` div with `data-view`, (2) new `case` in
`renderView()` switch, (3) new `renderX(container)` function that owns its panels and
registers charts in `chartInstances`, (4) its own data slice (new `DATA` key or separate
store — `loadAllData()` won't touch it). Don't touch summary cards, ticker,
`loadAllData()`, or proxy routing from a new tab.
