from github import Github
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("GitHub token not found. Add it in the .env file.")

g = Github(TOKEN)

repo = g.get_repo("fastapi/fastapi")

print(f"Connected to: {repo.full_name}")

os.makedirs("data", exist_ok=True)

commits = []

print("Fetching commits...")

for commit in repo.get_commits()[:100]:
    commits.append({
        "type": "commit",
        "sha": commit.sha,
        "message": commit.commit.message,
        "author": commit.commit.author.name if commit.commit.author else "Unknown",
        "date": str(commit.commit.author.date) if commit.commit.author else ""
    })

with open("data/commits.json", "w", encoding="utf-8") as f:
    json.dump(commits, f, indent=4)

print(f"Saved {len(commits)} commits")


prs = []

print("Fetching pull requests...")

for pr in repo.get_pulls(state="closed")[:50]:
    prs.append({
        "type": "pull_request",
        "number": pr.number,
        "title": pr.title,
        "body": pr.body,
        "author": pr.user.login,
        "state": pr.state,
        "created_at": str(pr.created_at),
        "merged": pr.is_merged()
    })

with open("data/pull_requests.json", "w", encoding="utf-8") as f:
    json.dump(prs, f, indent=4)

print(f"Saved {len(prs)} pull requests")


issues = []

print("Fetching issues...")

for issue in repo.get_issues(state="all")[:50]:

    # Skip pull requests
    if issue.pull_request is not None:
        continue

    issues.append({
        "type": "issue",
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "author": issue.user.login,
        "state": issue.state,
        "created_at": str(issue.created_at)
    })

with open("data/issues.json", "w", encoding="utf-8") as f:
    json.dump(issues, f, indent=4)

print(f"Saved {len(issues)} issues")

print("\n✅ Data ingestion completed successfully!")