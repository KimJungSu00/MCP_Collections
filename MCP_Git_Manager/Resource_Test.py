import asyncio
import json

from fastmcp import Client


mcp_client = Client("server.py")


async def main():
    async with mcp_client:
        resources = await mcp_client.list_resources()

        print("등록된 Resources")

        for resource in resources:
            print(f"- {resource.uri}")

        await show_diff()



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

if __name__ == "__main__":
    asyncio.run(main())