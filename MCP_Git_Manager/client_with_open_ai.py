import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client
from openai import AsyncOpenAI


load_dotenv(override=True)

mcp_client = Client("server.py")
llm_client = AsyncOpenAI()


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
    response = await llm_client.responses.create(
        model="gpt-4o-mini",
        input=full_prompt,
    )

    # 4. 모델이 작성한 결과를 반환한다.
    return response.output_text




async def main():
    async with mcp_client:
        report = await generate_bug_report(
            problem=(
                "프로그램을 실행하면 간헐적으로 "
                "GitHub API 요청이 401 오류로 실패합니다. "
                "재실행하면 정상적으로 작동할 때도 있습니다."
            ),
            environment=(
                "Windows 11, Python 3.12, FastMCP"
            ),
        )

        print("\n생성된 GitHub 버그 리포트")
        print(report)


if __name__ == "__main__":
    asyncio.run(main())