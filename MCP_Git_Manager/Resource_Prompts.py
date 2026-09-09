def make_bug_report_prompt(problem:str, environment: str= "") -> str:
    environment_text = environment if environment.strip() else "사용자가 제공하지 않음"
    return f"""당신은 GitHub 버그 이슈 작성 도우미입니다.
            아래의 사용자 설명을 바탕으로 명확한 버그 리포트를
            한국어 Markdown 형식으로 작성하세요.
            사용자 문제 설명:
            {problem}
            실행 환경:
            {environment_text}
            다음 구조로 작성하세요.
            제목:
            
            ## 문제 설명
            
            ## 재현 방법
            
            ## 예상 결과
            
            ## 실제 결과
            
            ## 실행 환경
            
            정보가 부족한 부분은 추측하지 말고
            "확인 필요"라고 작성하세요.
            """.strip()



def make_commit_message_prompt(diff: str,) -> str:
    return f"""
    당신은 Git 커밋 메시지 작성 도우미입니다.
    
    다음 Git diff를 분석하여 변경 내용을 정확하게
    설명하는 한국어 커밋 메시지를 작성하세요.
    
    Git diff:
    {diff}
    
    작성 규칙:
    
    1. subject는 변경사항을 한 줄로 요약합니다.
    2. subject는 72자를 넘지 않습니다.
    3. body에는 주요 변경사항을 항목별로 작성합니다.
    4. diff에 없는 내용은 추측하지 않습니다.
    5. 코드 자체보다 변경 목적을 중심으로 설명합니다.
    """.strip()


def make_pull_request_prompt(
    comparison: str,
) -> str:
    return f"""
당신은 GitHub Pull Request 작성 도우미입니다.

다음 브랜치 비교 결과를 분석하여 Pull Request의
제목과 본문을 한국어로 작성하세요.

브랜치 비교 결과:
{comparison}

작성 규칙:

1. title은 변경 목적을 한 줄로 요약합니다.
2. body는 Markdown 형식으로 작성합니다.
3. body에는 다음 항목을 포함합니다.

## 변경 요약

## 주요 변경사항

## 테스트

4. 비교 결과에 없는 내용은 추측하지 않습니다.
5. 테스트 정보가 없다면 "추가 테스트 필요"라고 작성합니다.
6. 파일 이름만 나열하지 말고 변경 내용을 설명합니다.
""".strip()