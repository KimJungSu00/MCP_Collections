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
github_token = os.getenv("GITHUB_TOKEN")
def get_github_headers() -> dict:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

def github_get(
    endpoint: str,
    params: dict | None = None,
) -> dict:
    headers = get_github_headers()

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

def github_post(
    endpoint: str,
    data: dict,
) -> dict:
    url = f"https://api.github.com{endpoint}"

    headers = headers = get_github_headers()

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10,
        )

        response_data = response.json()

    except requests.RequestException as error:
        return {
            "success": False,
            "error": str(error),
        }

    except ValueError:
        response_data = {
            "message": response.text,
        }

    if not response.ok:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response_data.get(
                "message",
                "GitHub API 요청 실패",
            ),
        }

    return {
        "success": True,
        "status_code": response.status_code,
        "data": response_data,
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


def get_github_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}"
    )

    if not result["success"]:
        return result

    pull_request = result["data"]

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "number": pull_request["number"],
        "title": pull_request["title"],
        "body": pull_request["body"],
        "state": pull_request["state"],
        "author": pull_request["user"]["login"],
        "draft": pull_request["draft"],

        "head_branch": pull_request["head"]["ref"],
        "head_sha": pull_request["head"]["sha"],

        "base_branch": pull_request["base"]["ref"],
        "base_sha": pull_request["base"]["sha"],

        "mergeable": pull_request["mergeable"], #자동 병합 가능한 상태인지 여부
        "mergeable_state": pull_request["mergeable_state"], # GitHub가 판단한 병합 상태
        "merged": pull_request["merged"], # 이미 병합됐는지
        "merged_at": pull_request["merged_at"],

        "commits": pull_request["commits"], # 해당 PR에 포함된 커밋 수
        "changed_files": pull_request["changed_files"], # 변경된 파일 수
        "additions": pull_request["additions"], # 추가된 줄 수
        "deletions": pull_request["deletions"], # 삭제된 줄 수

        "created_at": pull_request["created_at"],
        "updated_at": pull_request["updated_at"],
        "html_url": pull_request["html_url"],
    }

def create_github_pull_request(
    owner: str,
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main",
    draft: bool = False,
) -> dict:
    """GitHub 저장소에 Pull Request를 생성합니다."""

    title = title.strip()
    body = body.strip()
    head = head.strip()
    base = base.strip()

    if not title:
        return {
            "success": False,
            "error": "Pull Request 제목이 비어 있습니다.",
        }

    if not head:
        return {
            "success": False,
            "error": "head 브랜치가 비어 있습니다.",
        }

    if head == base:
        return {
            "success": False,
            "error": "head와 base 브랜치는 달라야 합니다.",
        }

    endpoint = f"/repos/{owner}/{repo}/pulls"

    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
        "draft": draft,
    }

    result = github_post(
        endpoint,
        data,
    )

    if not result["success"]:
        return result

    pull_data = result["data"]

    return {
        "success": True,
        "number": pull_data["number"],
        "title": pull_data["title"],
        "state": pull_data["state"],
        "draft": pull_data["draft"],
        "head": pull_data["head"]["ref"],
        "base": pull_data["base"]["ref"],
        "url": pull_data["html_url"],
    }


def get_github_labels(
    owner: str,
    repo: str,
) -> dict:
    result = github_get(
        f"/repos/{owner}/{repo}/labels",
        params={
            "per_page": 100,
        },
    )

    if not result["success"]:
        return result

    label_data = result["data"]
    labels = []

    for item in label_data:
        labels.append({
            "name": item["name"],
            "description": item["description"],
            "color": item["color"],
            "default": item["default"],
        })

    return {
        "success": True,
        "repository": f"{owner}/{repo}",
        "count": len(labels),
        "labels": labels,
    }


def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    labels: list[str] | None = None,
) -> dict:
    endpoint = f"/repos/{owner}/{repo}/issues"

    data = {
        "title": title,
        "body": body,
    }

    if labels:
        data["labels"] = labels

    result = github_post(
        endpoint,
        data,
    )

    if not result["success"]:
        return result

    issue_data = result["data"]

    return {
        "success": True,
        "number": issue_data["number"],
        "title": issue_data["title"],
        "state": issue_data["state"],
        "url": issue_data["html_url"],
    }