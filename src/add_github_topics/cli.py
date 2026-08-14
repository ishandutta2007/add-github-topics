import argparse
import os
import re
import subprocess
import sys
import requests
from dotenv import load_dotenv


def parse_git_remote_url(url: str):
    """
    Extract (owner, repo) from a GitHub remote URL.
    Supports HTTPS, SSH, and git protocol URLs.
    """
    if not url:
        return None, None

    url = url.strip()
    # Match HTTPS: https://github.com/owner/repo.git or https://user@github.com/owner/repo
    # Match SSH: git@github.com:owner/repo.git or ssh://git@github.com/owner/repo.git
    pattern = r"(?:https?://(?:[^@]+@)?github\.com/|git@github\.com:|ssh://(?:git@)?github\.com[:/])(?P<owner>[^/]+)/(?P<repo>[^/\s]+?)(?:\.git)?(?:\s.*)?$"
    match = re.search(pattern, url)
    if match:
        owner = match.group("owner")
        repo = match.group("repo")
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo
    return None, None


def get_default_repo_info():
    """
    Get the default (owner, repo) from git remote or local git configuration.
    Prioritizes git remote origin URL so that GitHub owner/handle is extracted accurately,
    avoiding the mistake of using local commit author git config user.name.
    """
    # 1. Try git remote get-url origin
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        owner, repo = parse_git_remote_url(remote_url)
        if owner and repo:
            return owner, repo
    except Exception:
        pass

    # 2. Try parsing all git remotes from git remote -v
    try:
        remote_v = subprocess.check_output(
            ["git", "remote", "-v"],
            stderr=subprocess.DEVNULL,
        ).decode()
        for line in remote_v.splitlines():
            if "github.com" in line:
                owner, repo = parse_git_remote_url(line)
                if owner and repo:
                    return owner, repo
    except Exception:
        pass

    # 3. Fallback: repo name from git root directory or current directory
    repo_name = None
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if git_root:
            repo_name = os.path.basename(git_root)
    except Exception:
        pass

    if not repo_name:
        repo_name = os.path.basename(os.getcwd())

    # Fallback username from git config github.user
    username = None
    try:
        username = subprocess.check_output(
            ["git", "config", "github.user"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        pass

    return username, repo_name


def sanitize_topic(topic: str) -> str:
    """
    Sanitize and validate a topic according to GitHub rules:
    - Lowercase
    - Only lowercase alphanumeric and hyphens
    - Cannot start with a hyphen
    - Max 50 characters
    """
    topic = topic.strip().lower()
    # Replace spaces and underscores with hyphens
    topic = re.sub(r"[\s_]+", "-", topic)
    # Remove any invalid characters (keep a-z, 0-9, and -)
    topic = re.sub(r"[^a-z0-9-]", "", topic)
    # Strip leading/trailing hyphens
    topic = topic.strip("-")
    # Truncate to 50 characters max
    return topic[:50]


def get_auth_token(cli_token=None):
    """
    Retrieve GitHub token from CLI arg or environment variables.
    Supports ADMIN_TOKEN, GITHUB_TOKEN, and GH_TOKEN.
    """
    token = (
        cli_token
        or os.getenv("ADMIN_TOKEN")
        or os.getenv("GITHUB_TOKEN")
        or os.getenv("GH_TOKEN")
    )
    if token:
        token = token.strip()
        # Clean potential 'Bearer ' or 'token ' prefix if user accidentally included it
        if token.startswith("Bearer "):
            token = token[7:].strip()
        elif token.startswith("token "):
            token = token[6:].strip()
    return token


def get_api_headers(token: str):
    """
    Return modern GitHub REST API headers:
    - Bearer authentication (required for Fine-grained PATs & modern REST API)
    - Accept: application/vnd.github+json
    - X-GitHub-Api-Version: 2022-11-28
    - User-Agent header (required by GitHub API)
    """
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "add-github-topics-cli",
    }


def handle_api_error(response, owner: str, repo: str):
    """
    Provide user-friendly, actionable error messages based on HTTP status code.
    """
    status = response.status_code
    try:
        err_json = response.json()
        msg = err_json.get("message", response.text)
    except Exception:
        msg = response.text

    if status == 401:
        print("❌ Error 401 (Unauthorized): Authentication failed.")
        print("   Please verify that your token is valid and not expired.")
    elif status == 403:
        print(f"❌ Error 403 (Forbidden): Access denied for repository '{owner}/{repo}'.")
        print("   If using a Fine-grained Personal Access Token (github_pat_*):")
        print("   1. Ensure the token has access to this repository.")
        print("   2. Ensure Repository Permissions -> 'Administration' is set to 'Read and write'.")
    elif status == 404:
        print(f"❌ Error 404 (Not Found): Repository '{owner}/{repo}' not found.")
        print("   Please check the username/owner and repository name.")
        print("   Ensure your token has permission to access private repositories if applicable.")
    elif status == 422:
        print(f"❌ Error 422 (Unprocessable Entity): {msg}")
        print("   Topics must contain only lowercase letters, numbers, and hyphens (max 50 chars, max 20 topics).")
    else:
        print(f"❌ Error {status}: {msg}")


def fetch_topics(owner: str, repo: str, headers: dict) -> list:
    """
    Fetch current topics from GitHub API for a repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        handle_api_error(response, owner, repo)
        sys.exit(1)
    return response.json().get("names", [])


def update_topics_api(owner: str, repo: str, headers: dict, topics: list) -> list:
    """
    Replace topics for a repository on GitHub API.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    response = requests.put(url, headers=headers, json={"names": topics})
    if response.status_code != 200:
        handle_api_error(response, owner, repo)
        sys.exit(1)
    return response.json().get("names", topics)


def add_topics(topics: list, token: str, owner: str, repo: str):
    """
    Add one or more topics to the repository.
    """
    headers = get_api_headers(token)
    current_topics = fetch_topics(owner, repo, headers)

    sanitized_new = []
    for t in topics:
        clean_t = sanitize_topic(t)
        if not clean_t:
            print(f"⚠️ Warning: Skipping invalid topic name '{t}'")
            continue
        if clean_t in current_topics or clean_t in sanitized_new:
            print(f"ℹ️ Topic '{clean_t}' already exists in {owner}/{repo}")
        else:
            sanitized_new.append(clean_t)

    if not sanitized_new:
        print(f"No new topics to add. Current topics: {', '.join(current_topics) if current_topics else '(none)'}")
        return

    updated_topics = current_topics + sanitized_new
    if len(updated_topics) > 20:
        print(f"❌ Error: GitHub limits repositories to 20 topics max. Current ({len(current_topics)}) + New ({len(sanitized_new)}) = {len(updated_topics)}.")
        sys.exit(1)

    result = update_topics_api(owner, repo, headers, updated_topics)
    print(f"✅ Successfully added topic(s) [{', '.join(sanitized_new)}] to {owner}/{repo}")
    print(f"🏷️  Current topics ({len(result)}): {', '.join(result)}")


def remove_topics(topics: list, token: str, owner: str, repo: str):
    """
    Remove one or more topics from the repository.
    """
    headers = get_api_headers(token)
    current_topics = fetch_topics(owner, repo, headers)

    sanitized_to_remove = [sanitize_topic(t) for t in topics]
    topics_to_keep = [t for t in current_topics if t not in sanitized_to_remove]

    removed = [t for t in current_topics if t in sanitized_to_remove]
    if not removed:
        print(f"ℹ️ None of the specified topics {sanitized_to_remove} were found in {owner}/{repo}.")
        print(f"Current topics: {', '.join(current_topics) if current_topics else '(none)'}")
        return

    result = update_topics_api(owner, repo, headers, topics_to_keep)
    print(f"✅ Successfully removed topic(s) [{', '.join(removed)}] from {owner}/{repo}")
    print(f"🏷️  Current topics ({len(result)}): {', '.join(result) if result else '(none)'}")


def list_topics(token: str, owner: str, repo: str):
    """
    List current topics for the repository.
    """
    headers = get_api_headers(token)
    topics = fetch_topics(owner, repo, headers)
    print(f"🏷️  Topics for {owner}/{repo} ({len(topics)}):")
    if topics:
        for t in topics:
            print(f"  • {t}")
    else:
        print("  (No topics found)")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Add, list, or manage topics for a GitHub repository.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  add-github-topic python
  add-github-topic machine-learning deep-learning ai
  add-github-topic --list
  add-github-topic --remove old-topic
  add-github-topic web-dev --owner ishandutta2007 --repo my-app
""",
    )
    parser.add_argument(
        "topics",
        nargs="*",
        help="One or more topics to add (or remove)",
    )
    parser.add_argument(
        "-t",
        "--token",
        help="GitHub Access Token (default: ADMIN_TOKEN / GITHUB_TOKEN in .env or environment)",
    )
    parser.add_argument(
        "-u",
        "--username",
        "--owner",
        dest="username",
        help="GitHub repository owner/username (default: auto-detected from git remote origin)",
    )
    parser.add_argument(
        "-r",
        "--reponame",
        "--repo",
        dest="reponame",
        help="GitHub repository name (default: auto-detected from git remote origin)",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List current topics for the repository",
    )
    parser.add_argument(
        "-d",
        "--remove",
        "--delete",
        action="store_true",
        dest="remove",
        help="Remove specified topic(s) instead of adding",
    )

    args = parser.parse_args()

    # Determine default owner & repo from git
    default_owner, default_repo = get_default_repo_info()
    owner = args.username or default_owner
    repo = args.reponame or default_repo
    token = get_auth_token(args.token)

    if not token:
        print("❌ Error: GitHub Access Token is required.")
        print("   Provide it via --token, or set ADMIN_TOKEN / GITHUB_TOKEN / GH_TOKEN in .env or environment.")
        sys.exit(1)

    if not owner:
        print("❌ Error: GitHub repository owner/username is required.")
        print("   Provide it via --username/--owner, or run within a git repo with a GitHub remote configured.")
        sys.exit(1)

    if not repo:
        print("❌ Error: Repository name is required.")
        print("   Provide it via --reponame/--repo, or run within a git repository.")
        sys.exit(1)

    # Flatten comma-separated or space-separated topics
    raw_topics = []
    for item in args.topics:
        if "," in item:
            raw_topics.extend([t.strip() for t in item.split(",") if t.strip()])
        else:
            raw_topics.append(item.strip())

    if args.list:
        list_topics(token, owner, repo)
    elif args.remove:
        if not raw_topics:
            print("❌ Error: Specify at least one topic to remove.")
            sys.exit(1)
        remove_topics(raw_topics, token, owner, repo)
    else:
        if not raw_topics:
            parser.print_help()
            print("\n❌ Error: Please provide at least one topic to add, or use --list (-l) to view topics.")
            sys.exit(1)
        add_topics(raw_topics, token, owner, repo)


if __name__ == "__main__":
    main()
