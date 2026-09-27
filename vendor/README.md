# Vendored front-end libraries

GitHub Pages serves these files as-is. There is no build step.

| File | Package | Version | License |
|---|---|---|---|
| `chart.umd.min.js` | Chart.js | 4.4.1 | MIT |
| `chartjs-plugin-annotation.min.js` | chartjs-plugin-annotation | 3.0.1 | MIT |

Downloaded 2026-09-27 from cdnjs:

- https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js
  sha256 `81ffafe13c37e1b25793b020d446f4d9739b949dadb7f9f79d709a0cad781c2f`
- https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-annotation/3.0.1/chartjs-plugin-annotation.min.js
  sha256 `f010c3c42842c98381f34ffa5613a99abeea2391080f20cfcf1b1678f3c555fa`

`index.html` loads both from this directory. The page no longer depends on cdnjs for charts. If these files are missing, the tables still render and each chart panel says the library did not load.
