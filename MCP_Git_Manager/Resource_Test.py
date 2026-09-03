import asyncio
import json

from fastmcp import Client

import os
import json

from dotenv import load_dotenv

mcp_client = Client("Server.py")
load_dotenv(override=True)

github_owner = os.getenv("GITHUB_OWNER")
github_repo = os.getenv("GITHUB_REPO")



async def main():
    async with mcp_client:
        await show_github_pull_requests()

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

if __name__ == "__main__":
    asyncio.run(main())
