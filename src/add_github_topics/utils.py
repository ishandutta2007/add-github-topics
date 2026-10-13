import re


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
