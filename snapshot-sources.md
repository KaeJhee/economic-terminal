# Embedded snapshot sources

Fetched on 2026-09-27. Every headline number in the `DATA` object of `index.html` that is marked with an `asOf` of `2026-08` or `2026-07` was computed from these downloads. Nothing in that set was estimated.

The page still boots from the embedded object. A FRED key recomputes the headline series with the same functions (`aggregateIndexYoY`, `aggregateLevelAverage`, `aggregatePayrollChange`).

## Where the files came from

- FRED public graph CSV, no API key: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES`
- BLS public API v2, no registration key, POST `https://api.bls.gov/publicAPI/v2/timeseries/data/` for `CUSR0000SA0`. August 2026 value `334.131` matches FRED `CPIAUCSL` for `2026-08-01`.
- Release dates are the BLS Schedule of Selected Releases for 2026, page `https://www.bls.gov/schedule/2026/`, fetched the same day. The next release after 2026-09-27 is JOLTS for August on 2026-09-29.

## How a number was computed

Price indexes (CPI, core CPI, PPI, core PPI, average hourly earnings, and the refreshed CPI and PPI components):

- Quarterly: percent change in the 3-month average index versus the same quarter a year earlier. A quarter is stored only when it has three months.
- Annual: percent change in the 12-month average versus the prior 12-month average. A year is stored only when both years have 12 months.
- `latest`: year-over-year change of the latest month. It is not the quarterly figure.
- `mom`: change from the previous month.
- Rounded with `Math.round(v * 10) / 10`, the same `round1()` the page uses. The 2022 unemployment average is 3.65, which rounds to 3.7.

October 2025 is blank at the source for CPI (`CUSR0000SA0` / `CPIAUCSL`), core CPI, unemployment, U-6, the labor force participation rate, shelter, owners' equivalent rent, and the refreshed CPI components. BLS returns `"-"` and the FRED cell is empty. Those series omit 2025-Q4 and the 2025 annual. PPI, payrolls, average hourly earnings, and JOLTS published October 2025, so they include 2025-Q4.

Payrolls:

- Quarterly: sum of the three monthly level changes (each month minus the prior month).
- Annual: December level minus the prior December.
- `latestMonth`: the latest monthly change, in thousands.

Unemployment: quarterly and annual are averages of the monthly rate. JOLTS is the same average, divided by 1,000 so the unit is millions. JOLTS stops at July 2026 because the August release is 2026-09-29.

Real GDP is FRED `A191RL1Q225SBEA`, which is BEA's percent change at a seasonally adjusted annual rate. `gdp.live` stays false until a BEA key returns NIPA table `T10101`, line 1.

## Headline series

| Series in the page | FRED id | Reference month | BLS release date |
|---|---|---|---|
| CPI all items | CPIAUCSL | 2026-08 | 2026-09-11 |
| Core CPI | CPILFESL | 2026-08 | 2026-09-11 |
| PPI final demand | PPIFIS | 2026-08 | 2026-09-10 |
| Core PPI | PPIFES | 2026-08 | 2026-09-10 |
| Nonfarm payrolls | PAYEMS | 2026-08 | 2026-09-04 |
| Unemployment, U-6, participation | UNRATE, U6RATE, CIVPART | 2026-08 | 2026-09-04 |
| Average hourly earnings | CES0500000003 | 2026-08 | 2026-09-04 |
| JOLTS openings | JTSJOL | 2026-07 | 2026-09-01 |
| Real GDP | A191RL1Q225SBEA | 2026-Q2 | BEA via FRED, not a BLS release |

August 2026 CPI all items in this snapshot: index 334.131, 3.4% year over year, 0.4% month over month.

## Refreshed component rows

August 2026, same monthly year-over-year and month-over-month method. Weights were not re-fetched. They are the relative-importance figures already in the previous file.

| Row | FRED id |
|---|---|
| CPI Food | CPIUFDSL |
| CPI Energy | CPIENGSL |
| CPI Shelter | CUSR0000SAH1 |
| CPI Medical | CPIMEDSL |
| CPI Transportation | CPITRNSL |
| CPI Apparel | CPIAPPSL |
| Shelter chart | CUSR0000SAH1 and CUSR0000SEHC (owners' equivalent rent), August 2025 through August 2026, October null |
| PPI Food | WPSFD4111 |
| PPI Energy | WPSFD4121 |
| PPI goods ex food and energy | WPSFD413 |

## Left as the March 2026 file, and labeled that way

These could not be re-fetched in this pass. The panels say so.

- CPI Education, Recreation, and Other Goods, including their weights.
- PPI final-demand goods, services, trade, transportation, and other, including weights.
- Employment by sector.

## Not a forecast

`projected` Q3 and Q4 values, the shaded bands, and the scenario table are the previous file's illustrative scenario. They were not refreshed from FOMC, CBO, or Blue Chip, and the overview charts do not plot them. The bands are `±(0.3 + 0.15 × step)` percentage points, drawn as "illustrative / fixed formula."
