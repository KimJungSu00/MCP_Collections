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
