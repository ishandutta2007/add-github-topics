# Add GitHub Topics

A simple Python script to add topics (tags) to a GitHub repository using the GitHub API.

## Features

- Add a topic to any GitHub repository you have access to.
- Automatically fetches existing topics to avoid overwriting them.
- Defaults to current repository information if run within a git repo.
- Supports `.env` file for secure token management.

## Prerequisites

- Python 3.x
- `requests`
- `python-dotenv`

Install dependencies:
```bash
pip install requests python-dotenv
```

## Setup

Create a `.env` file in the project root and add your GitHub Personal Access Token:
```env
ADMIN_TOKEN=your_github_token_here
```

## Usage

```bash
python add_topics.py <topic> [options]
```

### Arguments

- `topic`: (Mandatory) The topic you want to add.

### Options

- `--token`: GitHub Access Token. If not provided, it uses `ADMIN_TOKEN` from `.env`.
- `--username`: GitHub username. If not provided, it attempts to detect it from the current git configuration.
- `--reponame`: GitHub repository name. If not provided, it uses the current folder name.

### Example

```bash
python add_topics.py python --username ishandutta2007 --reponame add-github-topics
```

If run inside the repository and `.env` is set up:
```bash
python add_topics.py script
```
