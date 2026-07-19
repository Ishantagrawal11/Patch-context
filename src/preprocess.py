import json
import os

os.makedirs("data", exist_ok=True)

documents = []

with open("data/commits.json", "r", encoding="utf-8") as f:
    commits = json.load(f)

for commit in commits:
    documents.append({
        "text": f"""
Commit SHA: {commit['sha']}
Message: {commit['message']}
Author: {commit['author']}
Date: {commit['date']}
""".strip(),
        "metadata": {
            "type": "commit",
            "id": commit["sha"]
        }
    })

with open("data/pull_requests.json", "r", encoding="utf-8") as f:
    prs = json.load(f)

for pr in prs:
    documents.append({
        "text": f"""
PR #{pr['number']}
Title: {pr['title']}
Body: {pr['body'] or ""}
Author: {pr['author']}
Merged: {pr['merged']}
""".strip(),
        "metadata": {
            "type": "pull_request",
            "id": pr["number"]
        }
    })

with open("data/issues.json", "r", encoding="utf-8") as f:
    issues = json.load(f)

for issue in issues:
    documents.append({
        "text": f"""
Issue #{issue['number']}
Title: {issue['title']}
Body: {issue['body'] or ""}
Author: {issue['author']}
State: {issue['state']}
""".strip(),
        "metadata": {
            "type": "issue",
            "id": issue["number"]
        }
    })

with open("data/documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4)

print(f"✅ Created {len(documents)} documents.")