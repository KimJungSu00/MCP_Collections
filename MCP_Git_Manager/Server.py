from fastmcp import FastMCP

import GitHUB_API_Resources
import Local_Resources


mcp = FastMCP(name ="Git Manager")


@mcp.resource(
    "git://repository/status",
    mime_type="application/json",
)
def get_git_status() -> dict:
    """현재 Git 저장소의 브랜치와 변경 파일 상태를 반환합니다."""
    return Local_Resources.get_status()


@mcp.resource(
    "git://repository/diff",
    mime_type="application/json",
)
def get_git_different() -> dict:
    """현재 Git 저장소의 staged와 unstaged 변경 내용을 반환합니다"""
    return Local_Resources.get_different()


@mcp.resource(
    "git://repository/branches",
    mime_type="application/json",
)
def get_git_branches() -> dict:
    """현재 Git 저장소의 로컬,원격 브랜치 목록을 반환 합니다"""
    return Local_Resources.get_branches()

@mcp.resource(
    "git://repository/commits",
    mime_type="application/json",
)
def get_recent_commits() -> dict:
    """현재 Git 저장소의 최근 커밋 목록 (최대 10개)를 반환합니다"""
    return Local_Resources.get_recent_commits()

@mcp.resource(
    "git://repository/remotes",
    mime_type="application/json",
)
def git_remote() ->dict:
    """Git 저장소에 등록된 원격 저장소 정보를 반환합니다"""
    return Local_Resources.get_git_remotes()


@mcp.resource(
    "github://repos/{owner}/{repo}/summary",
    mime_type="application/json",
)
def get_github_repository_summary(
    owner: str,
    repo: str,
) -> dict:
    """GitHub 저장소의 요약 정보를 반환합니다."""
    return GitHUB_API_Resources.get_github_repository_summary(owner, repo)

@mcp.resource(
    "github://repos/{owner}/{repo}/branches",
    mime_type="application/json",
)
def get_github_branches(owner:str, repo:str) -> dict:
    """GitHub 저장소의 브랜치 목록을 반환합니다"""
    # get_git_branches와 차이점
    # github서버의 api를 통해 서버 내의 브랜치목록을 반환함
    return GitHUB_API_Resources.get_github_branches(owner, repo)

@mcp.resource(
    "github://repos/{owner}/{repo}/commits",
    mime_type="application/json",
)
def get_github_commits(
    owner: str,
    repo: str,
) -> dict:
    """GitHub 저장소의 최근 커밋 목록을 반환합니다."""

    return GitHUB_API_Resources.get_github_commits(
        owner,
        repo,
    )

@mcp.resource(
    "github://repos/{owner}/{repo}/issues",
    mime_type="application/json",
)
def get_github_issues(
    owner: str,
    repo: str,
) -> dict:
    """GitHub 저장소의 열린 이슈 목록을 반환합니다."""

    return GitHUB_API_Resources.get_github_issues(
        owner,
        repo,
    )

@mcp.resource(
    "github://repos/{owner}/{repo}/issues/{issue_number}",
    mime_type="application/json",
)
def get_github_issue(
    owner: str,
    repo: str,
    issue_number: int,
) -> dict:
    """특정 GitHub 이슈의 상세 정보를 반환합니다."""

    return GitHUB_API_Resources.get_github_issue(
        owner,
        repo,
        issue_number,
    )

@mcp.resource(
    "github://repos/{owner}/{repo}/pulls",
    mime_type="application/json",
)
def get_github_pull_requests(
    owner: str,
    repo: str,
) -> dict:
    """GitHub 저장소의 열린 Pull Request 목록을 반환합니다."""

    return GitHUB_API_Resources.get_github_pull_requests(
        owner,
        repo,
    )

if __name__ == "__main__":
    mcp.run()