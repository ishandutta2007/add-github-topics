import os
import subprocess


def get_auth_token(cli_token=None):
    """
    Retrieve GitHub token from CLI arg or environment variables or gh CLI.
    Prioritizes:
    1. CLI argument (--token)
    2. GITHUB_TOKEN (environment / .env)
    3. GH_TOKEN (environment / .env)
    4. ADMIN_TOKEN (environment / .env)
    5. gh auth token (GitHub CLI if installed)
    Returns (token_str, source_description).
    """
    source = None
    token = None

    if cli_token:
        token = cli_token
        source = "--token CLI argument"
    elif os.getenv("GITHUB_TOKEN"):
        token = os.getenv("GITHUB_TOKEN")
        source = "environment variable GITHUB_TOKEN"
    elif os.getenv("GH_TOKEN"):
        token = os.getenv("GH_TOKEN")
        source = "environment variable GH_TOKEN"
    elif os.getenv("ADMIN_TOKEN"):
        token = os.getenv("ADMIN_TOKEN")
        source = "environment variable ADMIN_TOKEN"
    else:
        # Fallback: GitHub CLI 'gh auth token'
        try:
            gh_token = (
                subprocess.check_output(
                    ["gh", "auth", "token"],
                    stderr=subprocess.DEVNULL,
                )
                .decode()
                .strip()
            )
            if gh_token:
                token = gh_token
                source = "GitHub CLI ('gh auth token')"
        except Exception:
            pass

    if token:
        token = token.strip()
        # Strip potential surrounding quotes (single or double)
        if (token.startswith('"') and token.endswith('"')) or (
            token.startswith("'") and token.endswith("'")
        ):
            token = token[1:-1].strip()
        # Clean potential 'Bearer ' or 'token ' prefix if accidentally included
        if token.startswith("Bearer "):
            token = token[7:].strip()
        elif token.startswith("token "):
            token = token[6:].strip()

    return token, source
