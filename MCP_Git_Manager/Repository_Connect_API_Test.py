import os

import requests
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")
github_owner = os.getenv("GITHUB_OWNER")
github_repo = os.getenv("GITHUB_REPO")

if not github_token:
    raise ValueError("GITHUB_TOKEN이 설정되지 않았습니다.")

if not github_owner:
    raise ValueError("GITHUB_OWNER가 설정되지 않았습니다.")

if not github_repo:
    raise ValueError("GITHUB_REPO가 설정되지 않았습니다.")

url = f"https://api.github.com/repos/{github_owner}/{github_repo}"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2026-03-10",
}

response = requests.get(
    url,
    headers=headers,
    timeout=10,
)

print("상태 코드:", response.status_code)


if response.status_code == 200:
    repository = response.json()

    print("저장소 이름:", repository["name"])
    print("전체 이름:", repository["full_name"])
    print("설명:", repository["description"])
    print("기본 브랜치:", repository["default_branch"])
    print("공개 여부:", not repository["private"])
    print("열린 이슈 수:", repository["open_issues_count"])
    print("저장소 주소:", repository["html_url"])

else:
    error = response.json()

    print("API 호출 실패")
    print("오류 내용:", error.get("message"))