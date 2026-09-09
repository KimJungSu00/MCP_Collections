import asyncio
import json

from fastmcp import Client

import os
import json
from openai import AsyncOpenAI

from dotenv import load_dotenv
from pydantic import BaseModel, Field


mcp_client = Client("Server.py")
load_dotenv(override=True)

github_owner = os.getenv("GITHUB_OWNER")
github_repo = os.getenv("GITHUB_REPO")
llm_client = AsyncOpenAI()


class BugReport(BaseModel):
    title: str
    body: str


async def show_branches():
    branches = await mcp_client.read_resource(
        "git://repository/branches"
    )
    print("Git Branches")
    print(branches)

async def show_commits():
    content = await mcp_client.read_resource(
        "git://repository/commits"
    )

    commit_data = json.loads(content[0].text)

    print("\nGit Commits")
    print(json.dumps(
        commit_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_diff():
    content = await mcp_client.read_resource(
        "git://repository/diff"
    )
    print("diff")
    diff_data = json.loads(content[0].text)

    print("\nUnstaged 변경사항")
    print(diff_data["unstaged"] or "변경사항 없음")

    print("\nStaged 변경사항")
    print(diff_data["staged"] or "변경사항 없음")

async def github_summary():
    templates = await mcp_client.list_resource_templates()

    print("\n등록된 Resource Templates")

    for template in templates:
        print(f"- {template.uri_template}")

    summary_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/summary"
    )

    content = await mcp_client.read_resource(
        summary_uri
    )

    summary_data = json.loads(
        content[0].text
    )

    print("\nGitHub Repository Summary")

    print(json.dumps(
        summary_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_github_branches():
    branches_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/branches"
    )

    branches_content = await mcp_client.read_resource(
        branches_uri
    )

    branches_data = json.loads(
        branches_content[0].text
    )

    print("\nGitHub Branches")

    print(json.dumps(
        branches_data,
        ensure_ascii=False,
        indent=2,
    ))


async def show_github_commits():
    commits_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/commits"
    )

    content = await mcp_client.read_resource(
        commits_uri
    )

    commit_data = json.loads(
        content[0].text
    )

    print("\nGitHub Commits")

    print(json.dumps(
        commit_data,
        ensure_ascii=False,
        indent=2,
    ))


async def show_github_issues():
    issues_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/issues"
    )

    content = await mcp_client.read_resource(
        issues_uri
    )

    issue_data = json.loads(
        content[0].text
    )

    print("\nGitHub Issues")

    print(json.dumps(
        issue_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_github_issue(
    issue_number: int,
):
    issue_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/issues/"
        f"{issue_number}"
    )

    content = await mcp_client.read_resource(
        issue_uri
    )

    issue_data = json.loads(
        content[0].text
    )

    print(f"\nGitHub Issue #{issue_number}")

    print(json.dumps(
        issue_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_github_pull_requests():
    pulls_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/pulls"
    )

    content = await mcp_client.read_resource(
        pulls_uri
    )

    pull_request_data = json.loads(
        content[0].text
    )

    print("\nGitHub Pull Requests")

    print(json.dumps(
        pull_request_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_github_pull_request(
    pull_number: int,
):
    pull_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/pulls/"
        f"{pull_number}"
    )

    content = await mcp_client.read_resource(
        pull_uri
    )

    pull_data = json.loads(
        content[0].text
    )

    print(f"\nGitHub Pull Request #{pull_number}")

    print(json.dumps(
        pull_data,
        ensure_ascii=False,
        indent=2,
    ))

async def show_github_labels():
    labels_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/labels"
    )

    content = await mcp_client.read_resource(
        labels_uri
    )

    label_data = json.loads(
        content[0].text
    )

    print("\nGitHub Labels")

    print(json.dumps(
        label_data,
        ensure_ascii=False,
        indent=2,
    ))

async def test_bug_report_prompt():
    prompts = await mcp_client.list_prompts()

    print("\n등록된 Prompts")

    for prompt in prompts:
        print(f"- {prompt.name}")

    result = await mcp_client.get_prompt(
        "write_bug_report",
        {
            "problem": (
                "프로그램을 실행하면 간헐적으로 "
                "GitHub API 요청이 실패합니다."
            ),
            "environment": (
                "Windows 11, Python 3.12"
            ),
        },
    )

    print("\n생성된 Prompt")

    for message in result.messages:
        print(f"\nrole: {message.role}")

        if hasattr(message.content, "text"):
            print(message.content.text)
        else:
            print(message.content)

async def generate_bug_report_preset():
    result = await create_issue_from_problem(
            problem=(
                "프로그램을 실행하면 간헐적으로 "
                "GitHub API 요청이 401 오류로 실패합니다. "
                "재실행하면 정상적으로 작동할 때도 있습니다."
            ),
            environment=(
                "Windows 11, Python 3.12, FastMCP"
            ),)
    print("\n생성된 GitHub 버그 리포트")
    print(result)

async def create_issue_from_problem(
    problem: str,
    environment: str = "",
):
    # Prompt와 LLM을 이용해 리포트 작성
    bug_report = await generate_bug_report(
        problem=problem,
        environment=environment,
    )

    print("\n생성된 제목")
    print(bug_report.title)

    print("\n생성된 본문")
    print(bug_report.body)

    # 작성된 리포트로 실제 GitHub Issue 생성
    result = await mcp_client.call_tool(
        "create_github_issue",
        {
            "owner": github_owner,
            "repo": github_repo,
            "title": bug_report.title,
            "body": bug_report.body,
            "labels": ["bug"],
        },
    )

    print("\nGitHub Issue 생성 결과")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)

async def generate_bug_report(
    problem: str,
    environment: str = "",
) -> str:
    # 1. MCP 서버에서 완성된 Prompt를 가져온다.
    prompt_result = await mcp_client.get_prompt(
        "write_bug_report",
        {
            "problem": problem,
            "environment": environment,
        },
    )

    # 2. Prompt 메시지에서 텍스트를 꺼낸다.
    prompt_texts = []

    for message in prompt_result.messages:
        if hasattr(message.content, "text"):
            prompt_texts.append(message.content.text)

    full_prompt = "\n\n".join(prompt_texts)

    # 3. Prompt를 실제 LLM에 전달한다.
    # 받은 값을 클래스를 지정하여 파싱
    # 지정하지 않을 경우에는 텍스트를 분리해야 함
    # 이때 LLM이 값을 조금만 다르게 준다면 문제가 커짐
    response = await llm_client.responses.parse(
        model="gpt-4o-mini",
        input=full_prompt,
        text_format=BugReport,
    )


    bug_report = response.output_parsed

    if bug_report is None:
        raise RuntimeError(
            "버그 리포트 생성에 실패했습니다."
        )
    # 4. 파싱된 결과를 반환
    return bug_report

async def test_create_issue():
    result = await mcp_client.call_tool(
        "create_github_issue",
        {
            "owner": github_owner,
            "repo": github_repo,
            "title": "[테스트] MCP Issue 생성",
            "body": """
## 문제 설명

MCP Tool을 통한 Issue 생성 테스트입니다.

## 실행 환경

- Windows 11
- Python 3.12
- FastMCP
""".strip(),
            "labels": ["bug"],
        },
    )

    print("\nGitHub Issue 생성 결과")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)

class CommitMessage(BaseModel):
    subject: str = Field(
        description = "72자 이하의 커밋 제목",
        min_length=1,
        max_length=72,
    )
    body : str = Field(
        description="Markdown 항목 형식의 변경사항 설명"
    )


async def generate_commit_message() -> CommitMessage:
    contents = await mcp_client.read_resource(
        "git://repository/diff"
    )

    diff_data = json.loads(
        contents[0].text
    )

    staged_diff = diff_data.get(
        "staged",
        "",
    )

    if not staged_diff:
        raise RuntimeError(
            "커밋 메시지를 생성할 staged 변경사항이 없습니다."
        )

    prompt_result = await mcp_client.get_prompt(
        "write_commit_message",
        {
            "diff": staged_diff,
        },
    )

    full_prompt = get_prompt_text(
        prompt_result
    )

    response = await llm_client.responses.parse(
        model="gpt-4o-mini",
        input=full_prompt,
        text_format=CommitMessage,
    )

    commit_message = response.output_parsed

    if commit_message is None:
        raise RuntimeError(
            "커밋 메시지 생성에 실패했습니다."
        )

    return commit_message


async def test_commit_message():
    commit_message = (
        await generate_commit_message()
    )

    print("\n커밋 제목")
    print(commit_message.subject)

    print("\n커밋 본문")
    print(commit_message.body)


def get_prompt_text(prompt_result) -> str:
    prompt_texts = []

    for message in prompt_result.messages:
        if hasattr(message.content, "text"):
            prompt_texts.append(
                message.content.text
            )

    return "\n\n".join(prompt_texts)

async def test_stage_files():
    result = await mcp_client.call_tool(
        "stage_files",
        {
            "paths": [
                "Server.py",
                "Local_Tools.py",
            ],
        },
    )

    print("\nGit Staging 결과")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)


async def test_commit_changes():
    result = await mcp_client.call_tool(
        "commit_changes",
        {
            "subject": "Git staging Tool 추가",
            "body": (
                "- 지정한 파일 staging 기능 추가\n"
                "- staged 파일 목록 반환 기능 추가"
            ),
        },
    )

    print("\nGit Commit 결과")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)

def get_tool_result_data(tool_result) -> dict:
    for content in tool_result.content:
        if hasattr(content, "text"):
            return json.loads(content.text)

    return {
        "success": False,
        "error": "Tool 결과가 없습니다.",
    }


async def run_commit_workflow(
    paths: list[str],
) -> dict:
    # 1. 지정한 파일 staging
    stage_result = await mcp_client.call_tool(
        "stage_files",
        {
            "paths": paths,
        },
    )

    stage_data = get_tool_result_data(
        stage_result
    )

    if not stage_data["success"]:
        return {
            "success": False,
            "step": "stage",
            "error": stage_data.get(
                "error",
                "파일 staging 실패",
            ),
        }

    print("\nStaged 파일")

    for path in stage_data["staged_files"]:
        print(f"- {path}")

    # 2. staged diff를 기반으로 커밋 메시지 생성
    commit_message = (
        await generate_commit_message()
    )

    print("\n생성된 커밋 메시지")
    print(commit_message.subject)
    print()
    print(commit_message.body)

    # 3. 실제 Git commit Tool 호출
    commit_result = await mcp_client.call_tool(
        "commit_changes",
        {
            "subject": commit_message.subject,
            "body": commit_message.body,
        },
    )

    commit_data = get_tool_result_data(
        commit_result
    )

    if not commit_data["success"]:
        return {
            "success": False,
            "step": "commit",
            "error": commit_data.get(
                "error",
                "Git commit 실패",
            ),
        }

    return {
        "success": True,
        "commit_hash": commit_data["commit_hash"],
        "subject": commit_data["subject"],
        "committed_files": commit_data[
            "committed_files"
        ],
    }


async def test_push_current_branch():
    result = await mcp_client.call_tool(
        "push_current_branch",
        {
            "remote": "origin",
        },
    )

    push_data = get_tool_result_data(
        result
    )

    print("\nGit Push 결과")
    print(json.dumps(
        push_data,
        ensure_ascii=False,
        indent=2,
    ))

async def test_pull():
    result = await mcp_client.call_tool(
        "pull_current_branch",
        {"remote": "origin"},
    )

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)

async def test_create_branch():
    result = await mcp_client.call_tool(
        "create_and_switch_branch",
        {
            "branch_name": (
                "feature-mcp-prompt-workflow"
            ),
        },
    )

    print("\n브랜치 생성 결과")

    for content in result.content:
        if hasattr(content, "text"):
            print(content.text)

async def test_create_pull_request():
    result = await mcp_client.call_tool(
        "create_github_pull_request",
        {
            "owner": github_owner,
            "repo": github_repo,
            "title": "MCP Git 작업 Tool 추가",
            "body": (
                "## 변경사항\n\n"
                "- Git staging Tool 추가\n"
                "- AI 커밋 메시지 생성 기능 추가\n"
                "- commit, pull, push Tool 추가\n"
                "- 브랜치 생성 및 이동 Tool 추가"
            ),
            "head": "feature-mcp-prompt-workflow",
            "base": "main",
            "draft": False,
        },
    )

    pull_data = get_tool_result_data(
        result
    )

    print("\nPull Request 생성 결과")
    print(json.dumps(
        pull_data,
        ensure_ascii=False,
        indent=2,
    ))


async def test_github_comparison():
    comparison_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/"
        f"compare/main/"
        f"feature-mcp-prompt-workflow"
    )

    contents = await mcp_client.read_resource(
        comparison_uri
    )

    comparison_data = json.loads(
        contents[0].text
    )

    print("\nGitHub 브랜치 비교 결과")
    print(json.dumps(
        comparison_data,
        ensure_ascii=False,
        indent=2,
    ))

class PullRequestDraft(BaseModel):
    title: str = Field(
        description="Pull Request 제목",
        min_length=1,
        max_length=120,
    )

    body: str = Field(
        description="Markdown 형식의 Pull Request 본문",
        min_length=1,
    )

async def generate_pull_request_draft(
    base: str,
    head: str,
) -> PullRequestDraft:
    comparison_uri = (
        f"github://repos/"
        f"{github_owner}/"
        f"{github_repo}/"
        f"compare/{base}/{head}"
    )

    contents = await mcp_client.read_resource(
        comparison_uri
    )

    comparison_data = json.loads(
        contents[0].text
    )

    if not comparison_data["success"]:
        raise RuntimeError(
            comparison_data.get(
                "error",
                "브랜치 비교에 실패했습니다.",
            )
        )

    if comparison_data["total_commits"] == 0:
        raise RuntimeError(
            "Pull Request에 포함할 커밋이 없습니다."
        )

    comparison_text = json.dumps(
        comparison_data,
        ensure_ascii=False,
        indent=2,
    )

    prompt_result = await mcp_client.get_prompt(
        "write_pull_request",
        {
            "comparison": comparison_text,
        },
    )

    full_prompt = get_prompt_text(
        prompt_result
    )

    response = await llm_client.responses.parse(
        model="gpt-4o-mini",
        input=full_prompt,
        text_format=PullRequestDraft,
    )

    pull_request = response.output_parsed

    if pull_request is None:
        raise RuntimeError(
            "Pull Request 내용 생성에 실패했습니다."
        )

    return pull_request

async def test_pull_request_draft():
    pull_request = (
        await generate_pull_request_draft(
            base="main",
            head="feature-mcp-prompt-workflow",
        )
    )

    print("\n생성된 PR 제목")
    print(pull_request.title)

    print("\n생성된 PR 본문")
    print(pull_request.body)

async def update_pull_request_from_comparison():
    # Resource → Prompt → LLM
    pull_request = (
        await generate_pull_request_draft(
            base="main",
            head="feature-mcp-prompt-workflow",
        )
    )

    print("\n생성된 PR 제목")
    print(pull_request.title)

    print("\n생성된 PR 본문")
    print(pull_request.body)

    # LLM 결과 → MCP Tool → GitHub PATCH
    result = await mcp_client.call_tool(
        "update_github_pull_request",
        {
            "owner": github_owner,
            "repo": github_repo,
            "pull_number": 5,
            "title": pull_request.title,
            "body": pull_request.body,
        },
    )

    update_data = get_tool_result_data(
        result
    )

    print("\nPull Request 수정 결과")
    print(json.dumps(
        update_data,
        ensure_ascii=False,
        indent=2,
    ))

async def test_merge_pull_request():
    result = await mcp_client.call_tool(
        "merge_github_pull_request",
        {
            "owner": github_owner,
            "repo": github_repo,
            "pull_number": 5,
            "merge_method": "squash",
            "commit_title": (
                "MCP Git 작업 Tool 및 기능 추가"
            ),
            "commit_message": (
                "Git 조회, 변경, Prompt 기반 "
                "문서 생성 기능을 추가합니다."
            ),
        },
    )

    merge_data = get_tool_result_data(
        result
    )

    print("\nPull Request Merge 결과")
    print(json.dumps(
        merge_data,
        ensure_ascii=False,
        indent=2,
    ))

async def main():
    async with mcp_client:
        await update_pull_request_from_comparison()

if __name__ == "__main__":
    asyncio.run(main())
