import os
import re
import subprocess


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
        remote_url = (
            subprocess.check_output(
                ["git", "remote", "get-url", "origin"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
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
        git_root = (
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
        if git_root:
            repo_name = os.path.basename(git_root)
    except Exception:
        pass

    if not repo_name:
        repo_name = os.path.basename(os.getcwd())

    # Fallback username from git config github.user
    username = None
    try:
        username = (
            subprocess.check_output(
                ["git", "config", "github.user"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except Exception:
        pass

    return username, repo_name
