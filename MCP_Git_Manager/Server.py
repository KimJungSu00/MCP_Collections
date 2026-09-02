from fastmcp import FastMCP

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


if __name__ == "__main__":
    mcp.run()