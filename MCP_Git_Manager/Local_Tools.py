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
            "error": result.get(
                "stderr",
                "git add 실행에 실패했습니다.",
            ),
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
                "stderr",
                "staged 파일 조회에 실패했습니다.",
            ),
        }

    return {
        "success": True,
        "requested_paths": valid_paths,
        "staged_files": staged_result.get(
            "stdout",
            "",
        ).splitlines(),
    }