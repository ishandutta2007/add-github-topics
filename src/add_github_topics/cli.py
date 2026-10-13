import sys
from dotenv import load_dotenv

from add_github_topics.api import (
    add_topics,
    fetch_topics,
    get_api_headers,
    handle_api_error,
    list_topics,
    remove_topics,
    update_topics_api,
)
from add_github_topics.auth import get_auth_token
from add_github_topics.git import get_default_repo_info, parse_git_remote_url
from add_github_topics.parser import build_parser, parse_topic_args
from add_github_topics.utils import sanitize_topic

__all__ = [
    "main",
    "build_parser",
    "parse_topic_args",
    "get_auth_token",
    "get_default_repo_info",
    "parse_git_remote_url",
    "sanitize_topic",
    "get_api_headers",
    "handle_api_error",
    "fetch_topics",
    "update_topics_api",
    "add_topics",
    "remove_topics",
    "list_topics",
]


def main():
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()

    # Determine default owner & repo from git
    default_owner, default_repo = get_default_repo_info()
    owner = args.username or default_owner
    repo = args.reponame or default_repo
    token, token_source = get_auth_token(args.token)

    if not token:
        print("❌ Error: GitHub Access Token is required.")
        print(
            "   Provide it via --token, or set GITHUB_TOKEN / GH_TOKEN in environment / .env, or login via 'gh auth login'."
        )
        sys.exit(1)

    if not owner:
        print("❌ Error: GitHub repository owner/username is required.")
        print(
            "   Provide it via --username/--owner, or run within a git repo with a GitHub remote configured."
        )
        sys.exit(1)

    if not repo:
        print("❌ Error: Repository name is required.")
        print("   Provide it via --reponame/--repo, or run within a git repository.")
        sys.exit(1)

    raw_topics = parse_topic_args(args.topics)

    if args.list:
        list_topics(token, owner, repo, token_source=token_source)
    elif args.remove:
        if not raw_topics:
            print("❌ Error: Specify at least one topic to remove.")
            sys.exit(1)
        remove_topics(raw_topics, token, owner, repo, token_source=token_source)
    else:
        if not raw_topics:
            parser.print_help()
            print(
                "\n❌ Error: Please provide at least one topic to add, or use --list (-l) to view topics."
            )
            sys.exit(1)
        add_topics(raw_topics, token, owner, repo, token_source=token_source)


if __name__ == "__main__":
    main()
