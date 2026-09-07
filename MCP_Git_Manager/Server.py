from fastmcp import FastMCP

import GitHUB_API_Resources
import Local_Resources
import Resource_Prompts
import Local_Tools


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

@mcp.resource(
    "github://repos/{owner}/{repo}/pulls/{pull_number}",
    mime_type="application/json",
)
def get_github_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
) -> dict:
    """특정 Pull Request의 상세 정보를 반환합니다."""

    return GitHUB_API_Resources.get_github_pull_request(
        owner,
        repo,
        pull_number,
    )

@mcp.resource(
    "github://repos/{owner}/{repo}/labels",
    mime_type="application/json",
)
def get_github_labels(
    owner: str,
    repo: str,
) -> dict:
    """GitHub 저장소에 등록된 라벨 목록을 반환합니다."""

    return GitHUB_API_Resources.get_github_labels(
        owner,
        repo,
    )

@mcp.prompt
def write_bug_report(problem:str, environment:str = "") -> str:
    """사용자의 문제 설명으로 GitHub 버그 리포트 작성 지침을 생성합니다."""
    return Resource_Prompts.make_bug_report_prompt(
        problem,
        environment,
    )

@mcp.tool
def create_github_issue(
    owner: str,
    repo: str,
    title: str,
    body: str,
    labels: list[str] | None = None,
) -> dict:
    """GitHub 저장소에 새로운 Issue를 생성합니다."""
    return GitHUB_API_Resources.create_github_issue(
        owner=owner,
        repo=repo,
        title=title,
        body=body,
        labels=labels,
    )

@mcp.prompt
def write_commit_message(
    diff: str,
) -> str:
    """Git diff를 분석하는 커밋 메시지 작성 지침을 생성합니다."""
    return Resource_Prompts.make_commit_message_prompt(
        diff
    )

@mcp.tool
def stage_files(
    paths: list[str],
) -> dict:
    """지정한 파일들을 Git staging 영역에 추가합니다."""
    return Local_Tools.stage_files(paths)

@mcp.tool
def commit_changes(
    subject: str,
    body: str = "",
) -> dict:
    """현재 staged 변경사항을 새로운 Git 커밋으로 생성합니다."""
    return Local_Tools.commit_changes(
        subject,
        body,
    )

@mcp.tool
def push_current_branch(remote: str = "origin") -> dict:
    """현재 브랜치의 커밋을 원격 Git 저장소로 push합니다."""
    return Local_Tools.push_current_branch(
        remote
    )

@mcp.tool
def pull_current_branch(remote: str = "origin") -> dict:
    """원격 저장소에서 현재 브랜치의 변경사항을 가져옵니다."""
    return Local_Tools.pull_current_branch(remote)


if __name__ == "__main__":
    mcp.run()