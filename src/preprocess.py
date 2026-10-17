import json
import os

os.makedirs("data", exist_ok=True)

REPO_URL = "https://github.com/fastapi/fastapi"
documents = []

with open("data/commits.json", "r", encoding="utf-8") as f:
    commits = json.load(f)

for commit in commits:
    documents.append({
        "text": (
            f"Commit SHA: {commit['sha']}\n"
            f"Message: {commit['message']}\n"
            f"Author: {commit['author']}\n"
            f"Date: {commit['date']}"
        ),
        "metadata": {
            "type": "commit",
            "id": commit["sha"],
            "source": f"{REPO_URL}/commit/{commit['sha']}",
        },
    })

with open("data/pull_requests.json", "r", encoding="utf-8") as f:
    prs = json.load(f)

for pr in prs:
    documents.append({
        "text": (
            f"Pull Request #{pr['number']}\n"
            f"Title: {pr['title']}\n"
            f"Body: {pr['body'] or ''}\n"
            f"Author: {pr['author']}\n"
            f"State: {pr['state']}\n"
            f"Created: {pr['created_at']}\n"
            f"Merged: {pr['merged']}"
        ),
        "metadata": {
            "type": "pull_request",
            "id": pr["number"],
            "source": f"{REPO_URL}/pull/{pr['number']}",
        },
    })

with open("data/issues.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

for issue in issues:
    documents.append({
        "text": (
            f"Issue #{issue['number']}\n"
            f"Title: {issue['title']}\n"
            f"Body: {issue['body'] or ''}\n"
            f"Author: {issue['author']}\n"
            f"State: {issue['state']}\n"
            f"Created: {issue['created_at']}"
        ),
        "metadata": {
            "type": "issue",
            "id": issue["number"],
            "source": f"{REPO_URL}/issues/{issue['number']}",
        },
    })

with open("data/documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4, ensure_ascii=False)

print(f"Created {len(documents)} documents.")
