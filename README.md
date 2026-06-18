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

Create a `.env` file in your project root or home directory to store your GitHub token:

```env
ADMIN_TOKEN=your_personal_access_token_here
```

### 3. Basic Usage 🛠️

Run the command from within any git repository:

```bash
add-github-topic python
```

## 📖 Detailed Usage Guide

```bash
add-github-topic <topic> [options]
```

### Options Explained

| Option | Shortcut | Description | Default |
| :--- | :--- | :--- | :--- |
| `topic` | - | **(Mandatory)** The topic string to add. | - |
| `--token` | - | Your GitHub Personal Access Token. | `ADMIN_TOKEN` from `.env` |
| `--username` | - | Your GitHub username. | Detected from `git config` |
| `--reponame` | - | Target repository name. | Current folder name |

### Examples 📝

**Add multiple tags sequentially:**
```bash
add-github-topic automation
add-github-topic cli-tool
```

**Target a specific repository and user:**
```bash
add-github-topic machine-learning --username ishandutta2007 --reponame awesome-ml-project
```

## 🛠️ Development & Contributions

Contributions are welcome! If you'd like to improve this tool:

1. Clone the repo: `git clone https://github.com/ishandutta2007/add-github-topics.git`
2. Install in editable mode: `pip install -e .`
3. Submit a Pull Request!

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
