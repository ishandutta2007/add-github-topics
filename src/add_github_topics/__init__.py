"""
Add GitHub Topics - A CLI tool and Python library to manage topics on GitHub repositories.
"""

from add_github_topics.api import (
    add_topics,
    fetch_topics,
    list_topics,
    remove_topics,
    update_topics_api,
)
from add_github_topics.auth import get_auth_token
from add_github_topics.git import get_default_repo_info, parse_git_remote_url
from add_github_topics.parser import build_parser, parse_topic_args
from add_github_topics.utils import sanitize_topic

__version__ = "0.2.1"

__all__ = [
    "add_topics",
    "fetch_topics",
    "list_topics",
    "remove_topics",
    "update_topics_api",
    "get_auth_token",
    "get_default_repo_info",
    "parse_git_remote_url",
    "sanitize_topic",
    "build_parser",
    "parse_topic_args",
]
