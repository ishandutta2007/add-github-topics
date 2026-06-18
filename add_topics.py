import os
import sys
import argparse
import requests
import subprocess
from dotenv import load_dotenv

def get_default_username():
    try:
        # Try getting from git config
        username = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        if username:
            return username
    except Exception:
        pass

    try:
        # Try getting from git remote
        remote_v = subprocess.check_output(['git', 'remote', '-v']).decode()
        # Typical HTTPS: origin  https://github.com/username/repo.git (fetch)
        # Typical SSH: origin git@github.com:username/repo.git (fetch)
        if 'github.com' in remote_v:
            if 'github.com/' in remote_v:
                parts = remote_v.split('github.com/')
                if len(parts) > 1:
                    username = parts[1].split('/')[0]
                    return username
            elif 'github.com:' in remote_v:
                parts = remote_v.split('github.com:')
                if len(parts) > 1:
                    username = parts[1].split('/')[0]
                    return username
    except Exception:
        pass
    
    return None

def get_default_reponame():
    return os.path.basename(os.getcwd())

def add_topic(topic, token, username, reponame):
    if not token:
        print("Error: GitHub Access Token is required. Provide it as an argument or set ADMIN_TOKEN in .env")
        sys.exit(1)
    if not username:
        print("Error: Username is required. Provide it as an argument or ensure git is configured.")
        sys.exit(1)
    if not reponame:
        print("Error: Repository name is required.")
        sys.exit(1)

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Get current topics
    url = f"https://api.github.com/repos/{username}/{reponame}/topics"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching current topics: {response.status_code} {response.text}")
        sys.exit(1)
    
    current_topics = response.json().get('names', [])
    
    if topic in current_topics:
        print(f"Topic '{topic}' already exists in {username}/{reponame}")
        return

    # 2. Add new topic
    new_topics = current_topics + [topic]
    response = requests.put(url, headers=headers, json={"names": new_topics})
    
    if response.status_code == 200:
        print(f"Successfully added topic '{topic}' to {username}/{reponame}")
        print(f"Current topics: {', '.join(new_topics)}")
    else:
        print(f"Error adding topic: {response.status_code} {response.text}")
        sys.exit(1)

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Add a topic to a GitHub repository.")
    parser.add_argument("topic", help="The topic to add")
    parser.add_argument("--token", help="GitHub Access Token (default: ADMIN_TOKEN from .env)")
    parser.add_argument("--username", help="GitHub username (default: current git username)")
    parser.add_argument("--reponame", help="GitHub repository name (default: current folder name)")
    
    args = parser.parse_args()
    
    topic = args.topic
    token = args.token or os.getenv("ADMIN_TOKEN")
    username = args.username or get_default_username()
    reponame = args.reponame or get_default_reponame()
    
    add_topic(topic, token, username, reponame)

if __name__ == "__main__":
    main()
