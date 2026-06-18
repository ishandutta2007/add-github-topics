# Add GitHub Topics

A CLI tool to add topics (tags) to a GitHub repository using the GitHub API.

## Features

- Add a topic to any GitHub repository you have access to.
- Automatically fetches existing topics to avoid overwriting them.
- Defaults to current repository information if run within a git repo.
- Supports `.env` file for secure token management.
- Installable via `pip` and usable as a command-line tool.

## Installation

You can install the package locally for development:

```bash
pip install .
```

Or install it directly from GitHub:

```bash
pip install git+https://github.com/ishandutta2007/add-github-topics.git
```

## Setup

Create a `.env` file in your current directory and add your GitHub Personal Access Token:
```env
ADMIN_TOKEN=your_github_token_here
```

## Usage

After installation, you can use the `add-github-topic` command:

```bash
add-github-topic <topic> [options]
```

### Arguments

- `topic`: (Mandatory) The topic you want to add.

### Options

- `--token`: GitHub Access Token. If not provided, it uses `ADMIN_TOKEN` from `.env`.
- `--username`: GitHub username. If not provided, it attempts to detect it from the current git configuration.
- `--reponame`: GitHub repository name. If not provided, it uses the current folder name.

### Example

```bash
add-github-topic python --username ishandutta2007 --reponame add-github-topics
```

If run inside a repository and `.env` is set up:
```bash
add-github-topic script
```

## Development

To install dependencies for development:
```bash
pip install -e .
```
