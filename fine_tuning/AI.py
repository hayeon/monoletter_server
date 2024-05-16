import os
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# OpenAI
def callGpt(letter,title):
    jobinfo = " Kotlin을 이용한 안드로이드 개발이 가능하신 분, Android Service를 이용한 어플리케이션 경험, Java, Kotlin 개발에 능숙하신 분, Custom UI Component 개발이 가능하신 분"
    goodLetter = "글의 주제로 이야기를 시작하는가? 한 문장 당 띄어쓰기 제외 60글자 이내로 작성하였는가? , 구체적인 경험의 예시를 보여주는가?"
    job = "안드로이드 개발자"
    try:
        # 자기소개서 체크 및 피드백 생성
       completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a kind AI assistant for self-introduction letters. Your task is to read the user's self-introduction letter and provide revisions detail."},
                {"role": "user", "content": f"나는 회사에 지원하는데 너의 도움이 필요해. 나의 직무는 {job} "},
                {"role": "assistant", "content": "네, 당신의 직무를 확인했습니다."},
                {"role": "user", "content": f"해당 직무는 다음과 같은 사람을 선호해. {jobinfo}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서 질문은 다음과 같아. {title}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"좋은 자기소개서를 작성하는 방법에 대해 너가 알아서 {goodLetter}에 미리 추가해놔."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서와 질문의 의도를 파악하고, 질문의 의도에 맞지 않는 글이라면 말해줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"지원하려는 직무의 우대사항은 다음과 같아. {jobinfo}. 우대사항을 추가할 게 있다면 너가 찾아서 추가해줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서는 다음과 같아 {letter}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서가 몇 분단으로 구분되는지 확인해. 문단은 \\n\\n으로 구분되어야 해."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"좋은 자기소개서의 조건과, 지원하려는 직무의 우대사항에 알맞는지 문단별로 말해야돼. 예시: 첫번째 문단: 두괄식으로 작성하는 게 좋습니다. 해당 자기소개서는 문항에 맞게 삼성전자를 지원하게 된 결정정인 이유와 입사 후, 목표를 뚜렷하게 작성하는 것이 좋습니다. 두번째 문단: 대학시절의 경험을 작성을 잘 하셨습니다. 하지만 구체적으로, 앱 개발자인만큼 어떤 기술을 사용하였는지를 기술하시는 게 좋을 것 같습니다.  반드시 문단별로 알려줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"무조건 첫 문장은 첫번째 문단: 으로 시작해야돼. 절대로 다른 말로 시작하지마."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"문단 별로 첨삭을 해주고, 마지막에 내 자소서가 어떤지 한문장으로 정리해줘 딱 한문장으로만. "},
                {"role": "assistant", "content": "네, 알겠습니다."},
            ],
            stream=False,  # 수정: 실시간 스트리밍이 필요없는 경우 False로 설정
        )

        # 생성된 피드백 반환
       feedback = completion.choices[0].message.content
       return feedback
    except Exception as e:
        print(f"API 호출 중 오류가 발생했습니다: {str(e)}")
