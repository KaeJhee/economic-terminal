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

## Prerequisites — What You Need to Install

Before running the dashboard locally or deploying to GitHub, you'll need some free tools. This section walks through every install for **Windows** (with Mac/Linux alternatives noted).

> **Don't have anything installed?** That's fine. Follow sections A through D in order — each one takes about 5 minutes.

---

### A. Python (for the local development server)

Python lets you spin up a simple web server in one command. This is the recommended way to view the dashboard locally.

**Download:** [https://www.python.org/downloads/](https://www.python.org/downloads/)

**Windows Install Steps:**

1. Go to the link above and click the big **"Download Python 3.x.x"** button
2. Run the `.exe` installer
3. **CRITICAL:** On the very first screen of the installer, check the box that says **"Add python.exe to PATH"** — this is at the bottom of the window. If you miss this, the `python` command won't work in your terminal.
4. Click **"Install Now"** (the default option is fine)
5. Wait for installation to complete, then click **Close**

**Verify it worked** — open Command Prompt (press `Win + R`, type `cmd`, press Enter):

```
python --version
```

You should see something like `Python 3.12.4`. If you see `'python' is not recognized`, you missed the PATH checkbox — uninstall and reinstall with it checked, or see the troubleshooting section below.

**Mac:** Python 3 is pre-installed on macOS 12.3+. Verify with `python3 --version` in Terminal. If not present, install via [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/) or `brew install python3`.

**Linux:** Pre-installed on most distros. Verify with `python3 --version`. If missing: `sudo apt install python3`.

---

### B. Node.js (alternative server + npm for package management)

Node.js is a JavaScript runtime. You don't strictly need it for this project, but it gives you access to `npm` (Node Package Manager), which is useful for installing tools and for future projects.

**Download:** [https://nodejs.org/en/download](https://nodejs.org/en/download)

**Windows Install Steps:**

1. Go to the link above
2. Click the **LTS** (Long Term Support) version — this is the stable one
3. Download the `.msi` installer for Windows
4. Run the installer — accept all defaults, click Next through every screen
5. On the "Tools for Native Modules" screen, you can **uncheck** the Chocolatey option (not needed here)
6. Click **Install**, then **Finish**

**Verify it worked** — open a **new** Command Prompt window (important — old windows don't see newly installed programs):

```
node --version
npm --version
```

You should see version numbers for both (e.g., `v20.11.0` and `10.2.4`).

**Mac:** Download the `.pkg` from the same link, or use `brew install node`.

**Linux:** `sudo apt install nodejs npm` or use the [NodeSource installer](https://github.com/nodesource/distributions).

---

### C. Visual Studio Code (code editor with Live Server)

VS Code is a free code editor from Microsoft. Its **Live Server** extension lets you edit the dashboard and see changes instantly in your browser without manually refreshing.

**Download:** [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

**Windows Install Steps:**

1. Go to the link above and click the big **Windows** button
2. Run the installer
3. **Recommended:** Check these boxes during install:
   - "Add 'Open with Code' action to Windows Explorer file context menu"
   - "Add 'Open with Code' action to Windows Explorer directory context menu"
   - "Add to PATH"
4. Click **Install**, then **Finish**
5. VS Code opens automatically

**Install the Live Server Extension:**

1. Open VS Code
2. Press `Ctrl + Shift + X` to open the Extensions panel
3. Type **"Live Server"** in the search box
4. Find the one by **Ritwick Dey** (it has millions of downloads)
5. Click **Install**
6. Done — you'll now see a "Go Live" button in the bottom-right corner of VS Code

**Mac:** Download the `.dmg` from the same link. Same extension install steps inside VS Code.

**Linux:** Download the `.deb` or `.rpm` from the same link, or `sudo snap install code --classic`.

---

### D. Git (for version control and GitHub deployment)

Git tracks changes to your files and lets you push code to GitHub.

**Download:** [https://git-scm.com/downloads](https://git-scm.com/downloads)

**Windows Install Steps:**

1. Go to the link above and click **Windows**
2. The download starts automatically (or click the link for the latest version)
3. Run the installer
4. **Accept all defaults** through every screen — the defaults are fine
5. On the "Choosing the default editor" screen, you can switch to **VS Code** if you installed it
6. Click **Install**, then **Finish**

After installation, you'll have two new programs:
- **Git Bash** — a Linux-style terminal (recommended for Git commands)
- **Git GUI** — a graphical interface (optional, most people use the command line)

**Verify it worked** — open a **new** Command Prompt or Git Bash:

```
git --version
```

You should see something like `git version 2.44.0.windows.1`.

**Configure Git (one-time setup):**

```
git config --global user.name "Your Name"
git config --global user.email "kris@ghoststrategies.io"
```

**Mac:** `git --version` in Terminal will prompt you to install Command Line Tools if Git isn't present. Click Install.

**Linux:** `sudo apt update && sudo apt install git`

---

## Run Locally — Three Options

### Option 1: Double-Click (Zero Install Required)

The dashboard is a single self-contained HTML file. Just double-click `index.html` in File Explorer and it opens in your default browser. That's it — no server, no install, nothing.

**Windows shortcut from Command Prompt:**
```
start index.html
```

**When to use this:** Quick viewing, demos, sharing with colleagues. Works perfectly for everything except `localStorage` persistence (which some browsers restrict on `file://` URLs).

---

### Option 2: server.py with CORS Proxy (Recommended for Live Data)

*Requires: Python installed (see Section A above)*

This runs a local server that **also proxies FRED and BLS API calls** to bypass CORS restrictions. This is how you get live data working locally.

1. Open **Command Prompt** (press `Win + R`, type `cmd`, press Enter)

2. Navigate to the project folder:
```
cd %USERPROFILE%\Desktop\economic-terminal
```

3. Start the proxy server:
```
python server.py
```

4. Open **http://localhost:8080** in your browser

5. Click the **API** button in the top-right, enter your FRED key, click **Save & Connect**

The server automatically detects `/api/fred` and `/api/bls` requests and forwards them to the real APIs with proper CORS headers. Static files (index.html, etc.) are served normally.

**Mac:** Same steps, but use `python3 server.py` in Terminal.

**Troubleshooting:**

| Problem | Solution |
|---------|----------|
| `'python' is not recognized` | You didn't check "Add to PATH" during install. Reinstall Python and check that box. Or try `python3 -m http.server 8080` instead. |
| `python` opens Microsoft Store | Windows sometimes redirects. Fix: Settings > Apps > App execution aliases > Turn OFF the "python.exe" and "python3.exe" aliases. |
| Port 8080 already in use | Change the number: `python -m http.server 8888` then go to `http://localhost:8888` |

---

### Option 3: VS Code + Live Server (Best for Editing)

*Requires: VS Code + Live Server extension installed (see Section C above)*

1. Open the `economic-terminal` folder in VS Code:
   - Right-click the folder in File Explorer > **"Open with Code"**
   - OR open VS Code > File > Open Folder > navigate to `economic-terminal`

2. In the VS Code file explorer (left panel), click on `index.html` to open it

3. Click the **"Go Live"** button in the bottom-right status bar (it appears after installing Live Server)

4. Your browser opens automatically at `http://127.0.0.1:5500/index.html`

5. **Hot reload:** Now edit any code in VS Code, save the file (`Ctrl + S`), and the browser refreshes automatically. This is the fastest feedback loop for development.

---

### Option 4: Node.js Server (Alternative)

*Requires: Node.js installed (see Section B above)*

1. Open **Command Prompt**

2. Install a simple HTTP server globally (one-time):
```
npm install -g http-server
```

3. Navigate to the project folder:
```
cd %USERPROFILE%\Desktop\economic-terminal
```

4. Start the server:
```
http-server -p 8080
```

5. Open **http://localhost:8080** in your browser.

---

## Deploy to GitHub Pages — Step by Step

### Step 1: Create a GitHub Account (skip if you have one)

1. Go to **https://github.com**
2. Click **Sign Up**
3. Follow the prompts — pick a username, enter your email, set a password
4. Verify your email address

### Step 2: Make Sure Git Is Installed

See **Section D** above. Verify with `git --version`.

### Step 3: Create a New Repository on GitHub

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name:** `economic-terminal`
   - **Description:** `Bloomberg-style economic indicators dashboard — CPI, PPI, Employment`
   - **Public** (must be public for free GitHub Pages)
   - **Do NOT** check "Add a README" (we already have one)
3. Click **Create repository**
4. Leave this tab open — you'll need the URL

### Step 4: Push Your Code to GitHub

Open **Git Bash** (recommended on Windows) or Command Prompt and run these commands **one at a time**:

```bash
# 1. Navigate to the project folder
cd ~/Desktop/economic-terminal

# 2. Initialize a Git repository
git init

# 3. Add all files to staging
git add .

# 4. Create your first commit
git commit -m "Initial commit: Economic Indicators Terminal v2.1"

# 5. Set the default branch to 'main'
git branch -M main

# 6. Connect to your GitHub repository
#    Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/economic-terminal.git

# 7. Push your code to GitHub
git push -u origin main
```

> **Windows path note:** In Git Bash, use forward slashes: `cd ~/Desktop/economic-terminal`. In Command Prompt, use backslashes: `cd %USERPROFILE%\Desktop\economic-terminal`.

**If GitHub asks for authentication:**

GitHub no longer accepts plain passwords. You need a **Personal Access Token**:

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token (classic)"**
3. Name it `terminal-deploy`, check the **repo** scope
4. Click **Generate token**
5. **Copy the token immediately** (you won't see it again)
6. When Git asks for your password, **paste the token instead**

### Step 5: Enable GitHub Pages

1. Go to your repository: `https://github.com/YOUR_USERNAME/economic-terminal`
2. Click **Settings** (gear icon)
3. Left sidebar: click **Pages**
4. Under Source, select **Branch: main** and **Folder: / (root)**
5. Click **Save**
6. Wait 1-2 minutes
7. Your live URL appears: **`https://YOUR_USERNAME.github.io/economic-terminal/`**

---

## Updating the Dashboard

After making edits, push to GitHub:

```bash
cd ~/Desktop/economic-terminal
git add .
git commit -m "Update: description of what you changed"
git push
```

GitHub Pages redeploys within 1-2 minutes.

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
