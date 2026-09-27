// Run the embedded runStatsTests() suite in headless Chrome.
// TZ=America/Chicago node scripts/run-stats-tests.mjs
// Requires puppeteer-core (npm install --no-save puppeteer-core) and Chrome.

import http from 'http';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function contentType(file) {
  if (file.endsWith('.html')) return 'text/html; charset=utf-8';
  if (file.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (file.endsWith('.css')) return 'text/css; charset=utf-8';
  if (file.endsWith('.png')) return 'image/png';
  if (file.endsWith('.svg')) return 'image/svg+xml';
  if (file.endsWith('.ico')) return 'image/vnd.microsoft.icon';
  return 'application/octet-stream';
}

const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
  const rel = urlPath === '/' ? 'index.html' : urlPath.replace(/^\/+/, '');
  const file = path.resolve(root, rel);
  if (file !== root && !file.startsWith(root + path.sep)) {
    res.writeHead(403);
    res.end();
    return;
  }
  fs.readFile(file, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end();
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType(file) });
    res.end(data);
  });
});

function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  for (const c of ['google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser']) {
    try {
      const found = execSync(`command -v ${c}`, { encoding: 'utf8' }).trim();
      if (found) return found;
    } catch { /* next candidate */ }
  }
  throw new Error('Chrome not found. Set CHROME_PATH.');
}

const port = await new Promise(resolve => {
  server.listen(0, '127.0.0.1', () => resolve(server.address().port));
});

let browser;
try {
  const puppeteer = await import('puppeteer-core');
  browser = await puppeteer.default.launch({
    executablePath: findChrome(),
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', err => errors.push(String(err)));
  await page.goto(`http://127.0.0.1:${port}/`, { waitUntil: 'networkidle0', timeout: 30000 });
  const report = await page.evaluate(() => {
    const suite = runStatsTests();
    return {
      pass: suite.pass,
      fail: suite.fail,
      failed: suite.results.filter(r => !r.pass).map(r => ({ name: r.name, actual: r.actual, expected: r.expected })),
      monthOfJan1: new Date('2025-01-01').getMonth(),
      quarter: quarterKeyFromDate('2025-01-01'),
      zone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    };
  });
  console.log(JSON.stringify({ zone: report.zone, monthOfJan1: report.monthOfJan1, quarter: report.quarter, pass: report.pass, fail: report.fail }, null, 2));
  if (errors.length) {
    console.error(errors.join('\n'));
    process.exitCode = 1;
  }
  if (report.quarter !== '2025-Q1') {
    console.error('quarterKeyFromDate shifted January off 2025-Q1');
    process.exitCode = 1;
  }
  if (process.env.TZ === 'America/Chicago' && report.monthOfJan1 !== 11) {
    console.error('Expected new Date("2025-01-01").getMonth() === 11 in America/Chicago, got ' + report.monthOfJan1);
    process.exitCode = 1;
  }
  if (report.fail !== 0) {
    console.error(JSON.stringify(report.failed, null, 2));
    process.exitCode = 1;
  }
} finally {
  if (browser) await browser.close();
  server.close();
}
