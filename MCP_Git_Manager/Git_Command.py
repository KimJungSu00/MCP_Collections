import subprocess
from pathlib import Path

# server.py가 들어 있는 폴더를 관리할 Git 저장소로 사용
repository_path = Path(__file__).resolve().parent


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


