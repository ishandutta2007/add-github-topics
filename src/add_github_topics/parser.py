import argparse


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argument parser for the CLI.
    """
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
        help="GitHub Access Token (default: GITHUB_TOKEN / GH_TOKEN / ADMIN_TOKEN in .env or environment, or gh CLI)",
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
    return parser


def parse_topic_args(raw_topics_list: list) -> list:
    """
    Flatten and extract topic strings from space-separated or comma-separated inputs.
    """
    topics = []
    for item in raw_topics_list:
        if "," in item:
            topics.extend([t.strip() for t in item.split(",") if t.strip()])
        else:
            if item.strip():
                topics.append(item.strip())
    return topics
