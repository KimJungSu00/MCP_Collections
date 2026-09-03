from Git_Command import *
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(
    dotenv_path=env_path,
    override=True,
)

github_api_url = "https://api.github.com"

def github_get(
    endpoint: str,
    params: dict | None = None,
) -> dict:
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    try:
        response = requests.get(
            f"{github_api_url}{endpoint}",
            headers=headers,
            params=params,
            timeout=10,
        )

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error),
        }

    if not response.ok:
        error_data = response.json()

        return {
            "success": False,
            "status_code": response.status_code,
            "error": error_data.get(
                "message",
                "GitHub API 요청 실패",
            ),
        }

    return {
        "success": True,
        "data": response.json(),
    }

def get_github_repository_summary(owner: str,
    repo: str) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}"
    )

    if not result["success"]:
        return result

    repository = result["data"]

    return {
        "success": True,
        "name": repository["name"],
        "full_name": repository["full_name"],
        "description": repository["description"],
        "private": repository["private"],
        "default_branch": repository["default_branch"],
        "language": repository["language"],
        "open_issues_count": repository["open_issues_count"],
        "created_at": repository["created_at"],
        "updated_at": repository["updated_at"],
        "html_url": repository["html_url"],
    }


def get_github_branches(owner: str,
    repo: str) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}/branches"
    )

    if not result["success"]:
        return result

    branch_data = result["data"]
    branches = []

    for branch in branch_data:
        branches.append({
            "name": branch["name"],
            "protected": branch["protected"],
            "commit_sha": branch["commit"]["sha"],
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "count": len(branches),
        "branches": branches,
    }



def get_github_commits(
    owner: str,
    repo: str,
) -> dict:

    result = github_get(
        f"/repos/{owner}/{repo}/commits",
        params={
            "per_page": 10,
        },
    )

    if not result["success"]:
        return result

    commit_data = result["data"]
    commits = []

    for item in commit_data:
        commit = item["commit"]
        author = commit["author"]

        commits.append({
            "sha": item["sha"],
            "short_sha": item["sha"][:7],
            "author": author["name"],
            "date": author["date"],
            "message": commit["message"],
            "html_url": item["html_url"],
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "count": len(commits),
        "commits": commits,
    }


def get_github_issues(
    owner: str,
    repo: str,
) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}/issues",
        params={
            "state": "open",
            "per_page": 20,
        },
    )

    if not result["success"]:
        return result

    issue_data = result["data"]
    issues = []

    for item in issue_data:
        # GitHub Issues API에는 Pull Request도 포함되므로 제외
        if "pull_request" in item:
            continue

        labels = []

        for label in item["labels"]:
            labels.append(label["name"])

        issues.append({
            "number": item["number"],
            "title": item["title"],
            "state": item["state"],
            "author": item["user"]["login"],
            "labels": labels,
            "comments": item["comments"],
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "html_url": item["html_url"],
        })

        return {
            "success": True,
            "repository": f"{owner}/{repo}",
            "count": len(issues),
            "issues": issues,
        }


def get_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict:

    result = github_get(
        f"/repos/{owner}/{repo}/issues/{issue_number}"
    )

    if not result["success"]:
        return result

    issue = result["data"]

    labels = []

    for label in issue["labels"]:
        labels.append(label["name"])

    assignees = []

    for assignee in issue["assignees"]:
        assignees.append(assignee["login"])

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"],
        "state": issue["state"],
        "author": issue["user"]["login"],
        "assignees": assignees,
        "labels": labels,
        "comments": issue["comments"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "closed_at": issue["closed_at"],
        "html_url": issue["html_url"],
        "is_pull_request": "pull_request" in issue,
    }


def get_github_pull_requests(
    owner: str,
    repo: str,
) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}/pulls",
        params={
            "state": "open",
            "per_page": 20,
        },
    )

    if not result["success"]:
        return result

    pull_request_data = result["data"]
    pull_requests = []


    for item in pull_request_data:
        pull_requests.append({
            "number": item["number"],
            "title": item["title"],
            "state": item["state"],
            "author": item["user"]["login"],
            "draft": item["draft"],
            "head_branch": item["head"]["ref"], # 변경사항이 들어있는 브랜치
            "base_branch": item["base"]["ref"], # 변경사항을 합칠 브랜치
            "created_at": item["created_at"],
            "updated_at": item["updated_at"],
            "html_url": item["html_url"],
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "count": len(pull_requests),
        "pull_requests": pull_requests,
    }