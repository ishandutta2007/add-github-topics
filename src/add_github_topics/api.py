import sys
import requests

from add_github_topics.utils import sanitize_topic


def get_api_headers(token: str) -> dict:
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


def handle_api_error(
    response, owner: str, repo: str, token: str = None, token_source: str = None
):
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
        if token_source:
            masked = (
                f"{token[:4]}...{token[-4:]}" if token and len(token) > 8 else "***"
            )
            print(
                f"   Token used: {masked} (length: {len(token) if token else 0}, source: {token_source})"
            )
    elif status == 403:
        print(
            f"❌ Error 403 (Forbidden): Access denied for repository '{owner}/{repo}'."
        )
        print("   If using a Fine-grained Personal Access Token (github_pat_*):")
        print("   1. Ensure the token has access to this repository.")
        print(
            "   2. Ensure Repository Permissions -> 'Administration' is set to 'Read and write'."
        )
    elif status == 404:
        print(f"❌ Error 404 (Not Found): Repository '{owner}/{repo}' not found.")
        print("   Please check the username/owner and repository name.")
        print(
            "   Ensure your token has permission to access private repositories if applicable."
        )
    elif status == 422:
        print(f"❌ Error 422 (Unprocessable Entity): {msg}")
        print(
            "   Topics must contain only lowercase letters, numbers, and hyphens (max 50 chars, max 20 topics)."
        )
    else:
        print(f"❌ Error {status}: {msg}")


def fetch_topics(
    owner: str, repo: str, headers: dict, token: str = None, token_source: str = None
) -> list:
    """
    Fetch current topics from GitHub API for a repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        handle_api_error(response, owner, repo, token, token_source)
        sys.exit(1)
    return response.json().get("names", [])


def update_topics_api(
    owner: str,
    repo: str,
    headers: dict,
    topics: list,
    token: str = None,
    token_source: str = None,
) -> list:
    """
    Replace topics for a repository on GitHub API.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    response = requests.put(url, headers=headers, json={"names": topics})
    if response.status_code != 200:
        handle_api_error(response, owner, repo, token, token_source)
        sys.exit(1)
    return response.json().get("names", topics)


def add_topics(
    topics: list, token: str, owner: str, repo: str, token_source: str = None
):
    """
    Add one or more topics to the repository.
    """
    headers = get_api_headers(token)
    current_topics = fetch_topics(owner, repo, headers, token, token_source)

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
        print(
            f"No new topics to add. Current topics: {', '.join(current_topics) if current_topics else '(none)'}"
        )
        return

    updated_topics = current_topics + sanitized_new
    if len(updated_topics) > 20:
        print(
            f"❌ Error: GitHub limits repositories to 20 topics max. Current ({len(current_topics)}) + New ({len(sanitized_new)}) = {len(updated_topics)}."
        )
        sys.exit(1)

    result = update_topics_api(
        owner, repo, headers, updated_topics, token, token_source
    )
    print(
        f"✅ Successfully added topic(s) [{', '.join(sanitized_new)}] to {owner}/{repo}"
    )
    print(f"🏷️  Current topics ({len(result)}): {', '.join(result)}")


def remove_topics(
    topics: list, token: str, owner: str, repo: str, token_source: str = None
):
    """
    Remove one or more topics from the repository.
    """
    headers = get_api_headers(token)
    current_topics = fetch_topics(owner, repo, headers, token, token_source)

    sanitized_to_remove = [sanitize_topic(t) for t in topics]
    topics_to_keep = [t for t in current_topics if t not in sanitized_to_remove]

    removed = [t for t in current_topics if t in sanitized_to_remove]
    if not removed:
        print(
            f"ℹ️ None of the specified topics {sanitized_to_remove} were found in {owner}/{repo}."
        )
        print(
            f"Current topics: {', '.join(current_topics) if current_topics else '(none)'}"
        )
        return

    result = update_topics_api(
        owner, repo, headers, topics_to_keep, token, token_source
    )
    print(
        f"✅ Successfully removed topic(s) [{', '.join(removed)}] from {owner}/{repo}"
    )
    print(
        f"🏷️  Current topics ({len(result)}): {', '.join(result) if result else '(none)'}"
    )


def list_topics(token: str, owner: str, repo: str, token_source: str = None):
    """
    List current topics for the repository.
    """
    headers = get_api_headers(token)
    topics = fetch_topics(owner, repo, headers, token, token_source)
    print(f"🏷️  Topics for {owner}/{repo} ({len(topics)}):")
    if topics:
        for t in topics:
            print(f"  • {t}")
    else:
        print("  (No topics found)")
