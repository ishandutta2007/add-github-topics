<p align="center">
  <img src="assets/banner.svg" alt="Add GitHub Topics Banner" width="800">
</p>

<h1 align="center">🚀 Add GitHub Topics CLI 🏷️</h1>

<p align="center">
  <b>Automate your GitHub repository tagging process with a single command!</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/add-github-topics/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/add-github-topics.svg?color=blue" /></a>
  <a href="https://pypi.org/project/add-github-topics/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/add-github-topics.svg" /></a>
  <a href="https://github.com/ishandutta2007/add-github-topics/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
  <a href="https://github.com/ishandutta2007/add-github-topics/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ishandutta2007/add-github-topics?style=social" /></a>
  <a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow&style=social" /></a>
</p>

---

## 🌟 Overview

`add-github-topics` is a powerful and lightweight **Python CLI tool** designed to help developers and maintainers programmatically manage their GitHub repository topics. Whether you are managing a single project or automating a large-scale migration, this tool simplifies the process of adding descriptive tags to your repositories.

Topics are essential for **SEO on GitHub**, making your projects more discoverable to the community! 🔍

## ✨ Key Features

- ✅ **Smart Appending:** Fetches existing topics first to avoid accidental overwrites.
- ✅ **Zero Config Defaults:** Automatically detects username and repository name from your local git environment.
- ✅ **Secure Token Handling:** Supports `.env` files for managing your GitHub Personal Access Token (PAT).
- ✅ **Global CLI:** Once installed, use it from any directory in your terminal.
- ✅ **Cross-Platform:** Works seamlessly on Windows, macOS, and Linux.

## 🚀 Quick Start

### 1. Installation 📦

Install the tool directly from PyPI:

```bash
pip install add-github-topics
```

### 2. Configuration ⚙️

Set your GitHub token in any of the following ways (in order of priority):

1. **CLI Argument:**
   ```bash
   add-github-topic python --token ghp_your_token_here
   ```

2. **Environment Variable:**
   - **Bash / Zsh:**
     ```bash
     export GITHUB_TOKEN=ghp_your_token_here
     ```
   - **PowerShell:**
     ```powershell
     $env:GITHUB_TOKEN = "ghp_your_token_here"
     ```

3. **`.env` File:**
   Create a `.env` file in your repository or home directory:
   ```env
   GITHUB_TOKEN=ghp_your_token_here
   ```
   *(Also supports `GH_TOKEN` and legacy `ADMIN_TOKEN`)*

4. **GitHub CLI (`gh`):**
   If you already have [GitHub CLI](https://cli.github.com/) installed and logged in (`gh auth login`), the CLI will automatically fallback to `gh auth token` with zero manual configuration!

### 3. Basic Usage 🛠️

Run the command from within any git repository:

```bash
add-github-topic python
```

## 📚 Documentation & Guides

---

### 👤 For Users

#### 1. Installation 📦

Install the latest release directly from PyPI:

```bash
pip install add-github-topics
```

#### 2. Configuration ⚙️

Set your GitHub token using any of the following methods (listed in order of evaluation priority):

1. **CLI Flag:**
   ```bash
   add-github-topic python --token ghp_your_token_here
   ```
2. **Environment Variable:**
   - **Linux / macOS (Bash/Zsh):**
     ```bash
     export GITHUB_TOKEN=ghp_your_token_here
     ```
   - **Windows (PowerShell):**
     ```powershell
     $env:GITHUB_TOKEN = "ghp_your_token_here"
     ```
3. **Local `.env` File:**
   Create a `.env` file in your repository or home directory:
   ```env
   GITHUB_TOKEN=ghp_your_token_here
   ```
   *(Supports `GITHUB_TOKEN`, `GH_TOKEN`, and `ADMIN_TOKEN`)*
4. **GitHub CLI Integration:**
   If logged into the [GitHub CLI (`gh`)](https://cli.github.com/), `add-github-topic` automatically obtains credentials via `gh auth token`.

#### 3. Common Commands 🛠️

```bash
# Add single or multiple topics
add-github-topic python machine-learning devops

# List current repository topics
add-github-topic --list

# Remove existing topics
add-github-topic --remove legacy-tag

# Target a specific remote repository
add-github-topic python --owner ishandutta2007 --repo awesome-project
```

---

### 💻 For Developers & Contributors

We welcome contributions to `add-github-topics`!

#### 1. Local Development Setup 🛠️

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ishandutta2007/add-github-topics.git
   cd add-github-topics
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   # On Linux/macOS:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```

3. **Install Editable Package:**
   ```bash
   pip install -e .
   ```

#### 2. Code Structure & Guidelines 📐

- Main entrypoint CLI: `src/add_github_topics/cli.py`
- Follow PEP 8 style guidelines.
- Test your changes locally before submitting a PR.

---

### 🚀 For Package Publishers & DevOps

#### Automated PyPI Publishing 📦

The project uses GitHub Actions with **PyPI Trusted Publishing (OIDC)** for automated releases.

#### How Version Release & Auto-Publishing Works:

1. **Version Bump Workflow (Automated on Push):**
   - Whenever you increment the version in `pyproject.toml` (e.g. `version = "0.2.2"`) and push your commit to `main` or `master`:
     ```toml
     [project]
     version = "0.2.2"
     ```
   - The `.github/workflows/publish.yml` workflow triggers automatically.
   - It builds the package source & wheel and attempts to publish to PyPI.
   - **Idempotency (`skip-existing: true`):** If the version has already been published to PyPI, the publish action skips safely without failing.

2. **Git Tag Workflow:**
   - Tagged releases (e.g. `v0.2.2`) pushed to GitHub will also trigger auto-publishing:
     ```bash
     git tag v0.2.2
     git push origin v0.2.2
     ```

3. **Manual Trigger (`workflow_dispatch`):**
   - You can also trigger a release manually via the **Actions** tab in GitHub.

#### DevOps Initial Setup Checklist (One-time):

- Configure PyPI Trusted Publisher for repository `ishandutta2007/add-github-topics`.
- Create environment `pypi` under GitHub Repository Settings -> Environments.

---

## 📈 Star History
<div align="center">
   <a href="https://www.star-history.com/repos=ishandutta2007%2Fadd-github-topics&type=date&legend=bottom-right">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/add-github-topics&type=date&theme=dark&legend=bottom-right" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/add-github-topics&type=date&legend=bottom-right" />
      <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/add-github-topics&type=date&legend=bottom-right" />
    </picture>
   </a>
</div>

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/ishandutta2007">Ishan Dutta</a>
</p>
