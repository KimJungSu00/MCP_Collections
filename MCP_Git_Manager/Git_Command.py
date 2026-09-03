import subprocess
import os
from pathlib import Path
import requests

# server.py가 들어 있는 폴더를 관리할 Git 저장소로 사용
repository_path = Path(__file__).resolve().parent

github_token = os.getenv("GITHUB_TOKEN")
github_api_url = "https://api.github.com"


def run_git_command(arguments: list[str]) -> dict:
    """현재 저장소에서 Git 명령을 실행합니다."""

    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=repository_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    except FileNotFoundError:
        return {
            "success": False,
            "error": "Git이 설치되어 있지 않거나 PATH에 등록되지 않았습니다.",
        }

    if result.returncode != 0:
        return {
            "success": False,
            "error": result.stderr.strip(),
        }

    return {
        "success": True,
        "output": result.stdout.strip(),
    }


def github_get(endpoint: str) -> dict:
    """GitHub REST API에 GET 요청을 보냅니다."""

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    try:
        response = requests.get(
            f"{github_api_url}{endpoint}",
            headers=headers,
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
            "error": error_data.get("message", "GitHub API 요청 실패"),
        }

    return {
        "success": True,
        "data": response.json(),
    }


