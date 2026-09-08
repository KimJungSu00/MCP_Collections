import Git_Command


def stage_files(
    paths: list[str],
) -> dict:
    """지정한 파일들을 Git staging 영역에 추가합니다."""

    valid_paths = [
        path.strip()
        for path in paths
        if path.strip()
    ]

    if not valid_paths:
        return {
            "success": False,
            "error": "스테이징할 파일이 없습니다.",
        }

    result = Git_Command.run_git_command(
        [
            "add",
            "--",
            *valid_paths,
        ]
    )

    if not result["success"]:
        return {
            "success": False,
            "error": (
                result.get("error")
                or result.get("output")
                or "git add 실행에 실패했습니다."
            ),
            "git_result": result,
        }

    staged_result = Git_Command.run_git_command(
        [
            "diff",
            "--cached",
            "--name-only",
        ]
    )

    if not staged_result["success"]:
        return {
            "success": False,
            "error": (
                staged_result.get("error")
                or staged_result.get("output")
                or "staged 파일 조회에 실패했습니다."
            ),
            "git_result": staged_result,
        }

    return {
        "success": True,
        "requested_paths": valid_paths,
        "staged_files": staged_result.get(
            "output",
            "",
        ).splitlines(),
    }



def commit_changes(subject: str, body: str = "") -> dict:


    subject = subject.strip()
    body = body.strip()

    if not subject:
        return {
            "success": False,
            "error": "커밋 제목이 비어 있습니다.",
        }

    staged_result = Git_Command.run_git_command(
        [
            "diff",
            "--cached",
            "--name-only",
        ]
    )

    if not staged_result["success"]:
        return {
            "success": False,
            "error": staged_result.get(
                "error",
                "staged 파일 확인에 실패했습니다.",
            ),
        }

    staged_files = staged_result.get(
        "output",
        "",
    ).splitlines()

    if not staged_files:
        return {
            "success": False,
            "error": "커밋할 staged 파일이 없습니다.",
        }

    command = [
        "commit",
        "-m",
        subject,
    ]

    if body:
        command.extend([
            "-m",
            body,
        ])

    commit_result = Git_Command.run_git_command(
        command
    )

    if not commit_result["success"]:
        return {
            "success": False,
            "error": commit_result.get(
                "error",
                "Git 커밋에 실패했습니다.",
            ),
        }

    hash_result = Git_Command.run_git_command(
        [
            "rev-parse",
            "--short",
            "HEAD",
        ]
    )

    if not hash_result["success"]:
        return {
            "success": False,
            "error": hash_result.get(
                "error",
                "커밋 해시 확인에 실패했습니다.",
            ),
        }

    return {
        "success": True,
        "commit_hash": hash_result.get(
            "output",
            "",
        ),
        "subject": subject,
        "body": body,
        "committed_files": staged_files,
        "output": commit_result.get(
            "output",
            "",
        ),
    }


def push_current_branch(remote: str = "origin") -> dict:
    branch_result = Git_Command.run_git_command(
        [
            "branch",
            "--show-current",
        ]
    )

    if not branch_result["success"]:
        return {
            "success": False,
            "error": branch_result.get(
                "error",
                "현재 브랜치 확인에 실패했습니다.",
            ),
        }

    branch = branch_result.get(
        "output",
        "",
    ).strip()

    if not branch:
        return{
            "success": False,
            "error":(
                "현재 브랜치를 확인할 수 없습니다"
                "detached HEAD 상태일 수 있습니다"
            )
        }

    remote_result = Git_Command.run_git_command(
        [
            "remote",
            "get-url",
            remote,
        ]
    )

    if not remote_result["success"]:
        return {
            "success": False,
            "error": remote_result.get(
                "error",
                f"원격 저장소 '{remote}'를 찾을 수 없습니다.",
            ),
        }


    remote_url = remote_result.get(
        "output",
        "",
    ).strip()

    # 현재 브랜치 push
    push_result = Git_Command.run_git_command(
        [

            "push",
            "-u", # -u : 로컬 브랜치와 원격 브랜치의 추적 관계 설정
            remote,
            branch,
        ]
        # 현재 브랜치가 feature일 경우 위의 명령어는 다음과 같음
        # git push -u origin feature

    )

    if not push_result["success"]:
        return {
            "success": False,
            "branch": branch,
            "remote": remote,
            "error": push_result.get(
                "error",
                "Git push에 실패했습니다.",
            ),
        }

    return {
        "success": True,
        "branch": branch,
        "remote": remote,
        "remote_url": remote_url,
        "output": push_result.get(
            "output",
            "",
        ),
    }


def pull_current_branch(remote: str = "origin") -> dict:

    # 현재 브랜치 확인
    branch_result = Git_Command.run_git_command(
        [
            "branch",
            "--show-current",
        ]
    )

    if not branch_result["success"]:
        return {
            "success": False,
            "error": branch_result.get(
                "error",
                "현재 브랜치 확인에 실패했습니다.",
            ),
        }

    branch = branch_result.get(
        "output",
        "",
    ).strip()

    if not branch:
        return {
            "success": False,
            "error": (
                "현재 브랜치를 확인할 수 없습니다. "
                "detached HEAD 상태일 수 있습니다."
            ),
        }

    # 로컬 변경사항 확인
    status_result = Git_Command.run_git_command(
        [
            "status",
            "--porcelain",
        ]
    )

    if not status_result["success"]:
        return {
            "success": False,
            "error": status_result.get(
                "error",
                "Git 상태 확인에 실패했습니다.",
            ),
        }

    changed_files = status_result.get(
        "output",
        "",
    ).strip()

    if changed_files:
        return {
            "success": False,
            "branch": branch,
            "error": (
                "커밋되지 않은 로컬 변경사항이 있습니다. "
                "먼저 commit하거나 변경사항을 정리해 주세요."
            ),
            "changed_files": changed_files.splitlines(),
        }

    # 원격 저장소 확인
    remote_result = Git_Command.run_git_command(
        [
            "remote",
            "get-url",
            remote,
        ]
    )

    if not remote_result["success"]:
        return {
            "success": False,
            "error": remote_result.get(
                "error",
                f"원격 저장소 '{remote}'를 찾을 수 없습니다.",
            ),
        }

    # 현재 브랜치 pull
    # ff-only : 브랜치를 단순히 앞으로 이동할 수 있을때만 pull 한다
    pull_result = Git_Command.run_git_command(
        [
            "pull",
            "--ff-only",
            remote,
            branch,
        ]
    )

    if not pull_result["success"]:
        return {
            "success": False,
            "branch": branch,
            "remote": remote,
            "error": pull_result.get(
                "error",
                "Git pull에 실패했습니다.",
            ),
        }

    return {
        "success": True,
        "branch": branch,
        "remote": remote,
        "remote_url": remote_result.get(
            "output",
            "",
        ),
        "output": pull_result.get(
            "output",
            "",
        ),
    }


def create_and_switch_branch(branch_name: str) -> dict:

    branch_name = branch_name.strip()

    if not branch_name:
        return {
            "success": False,
            "error": "브랜치 이름이 비어 있습니다.",
        }

    # 현재 브랜치 확인
    current_result = Git_Command.run_git_command(
        [
            "branch",
            "--show-current",
        ]
    )

    if not current_result["success"]:
        return {
            "success": False,
            "error": current_result.get(
                "error",
                "현재 브랜치 확인에 실패했습니다.",
            ),
        }

    previous_branch = current_result.get(
        "output",
        "",
    ).strip()

    # 브랜치 이름 유효성 확인
    check_result = Git_Command.run_git_command(
        [
            "check-ref-format",
            "--branch",
            branch_name,
        ]
    )

    if not check_result["success"]:
        return {
            "success": False,
            "error": check_result.get(
                "error",
                "사용할 수 없는 브랜치 이름입니다.",
            ),
        }

    # 새 브랜치 생성 후 이동
    switch_result = Git_Command.run_git_command(
        [
            "switch",
            "-c",
            branch_name,
        ]
    )

    if not switch_result["success"]:
        return {
            "success": False,
            "error": switch_result.get(
                "error",
                "브랜치 생성에 실패했습니다.",
            ),
        }

    return {
        "success": True,
        "previous_branch": previous_branch,
        "current_branch": branch_name,
        "output": switch_result.get(
            "output",
            "",
        ),
    }

