from Git_Command import *

def get_status() -> dict:
    result = run_git_command([
        "status",
        "--short",
        "--branch",
    ])

    if not result["success"]:
        return result

    return {
        "success": True,
        "repository": repository_path.name,
        "status": result["output"],
    }


def get_different() -> dict:
    unstaged = run_git_command([
        "diff",
        "--no-color"])
    #co color : 터미널용 색상 문자 결과를 제거

    if not unstaged["success"]:
        return unstaged


    #diff - cached : 마지막 커밋과 stage 영역을 비교
    staged = run_git_command([
        "diff",
        "--cached",
        "--no-color"
    ])

    if not staged["success"]:
        return staged

    return{
        "success": True,
        "repository" : repository_path.name,
        "unstaged": unstaged["output"],
        "staged": staged["output"],
    }


def get_branches():
    current_result = run_git_command([
        "branch",
        "--show-current",
    ])

    if not current_result["success"]:
        return current_result

    local_result = run_git_command([
        "branch",
        "--format=%(refname:short)", #브랜치의 전체 이름대신 짧은 이름만 출력
    ])

    if not local_result["success"]:
        return local_result

    remote_result = run_git_command([
        "branch",
        "--remotes", #원격 브랜치를 조회
        "--format=%(refname:short)",
    ])

    if not remote_result["success"]:
        return remote_result

    local_branches = local_result["output"].split("\n")
    remote_branches = remote_result["output"].split("\n")

    return{
        "success": True,
        "repository": repository_path.name,
        "current_branch": current_result["output"],
        "local_branches": local_branches,
        "remote_branches": remote_branches,
    }

def get_recent_commits():
    result = run_git_command([
        "log", # 커밋 기록 조회
        "-10", # 최근 커밋 10개
        "--pretty=format:%h|%an|%ad|%s", # 출력 형식 지정
        "--date=iso-strict", # 날짜를 일정한 ISO 형식으로 출력
    ])

    if not result["success"]:
        return result

    commits = []

    for line in result["output"].splitlines():
        #라인 출력 방식 : "a582179|김정수|2026-09-01T17:14:17+09:00|idea 제외"
        parts = line.split("|", 3)

        if len(parts) != 4:
            continue

        commits.append({
            "hash": parts[0],
            "author": parts[1],
            "date": parts[2],
            "message": parts[3],
        })

    return {
        "success": True,
        "repository": repository_path.name,
        "count": len(commits),
        "commits": commits,
    }


