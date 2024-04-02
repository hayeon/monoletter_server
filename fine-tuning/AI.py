import os
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# OpenAI
def callGpt(letter):
    jobinfo = " Kotlin을 이용한 안드로이드 개발이 가능하신 분, Android Service를 이용한 어플리케이션 경험, Java, Kotlin 개발에 능숙하신 분, Custom UI Component 개발이 가능하신 분"
    ask = "삼성전자를 지원한 이유와 입사 후 회사에서 이루고 싶은 꿈을 기술하십시오"
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
                {"role": "user", "content": f"나의 자기소개서 질문은 다음과 같아. {ask}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"좋은 자기소개서를 작성하는 방법에 대해 너가 알아서 {ask}에 미리 추가해놔."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서와 질문의 의도를 파악하고, 질문의 의도에 맞지 않는 글이라면 말해줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서와 질문의 의도가 회사의 인재상인지를 확인하기 위함인지, 직무 경험이 있는지를 확인하기 위함인지파악해줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"좋은 자기소개서의 조건은 다음과 같아. {goodLetter}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"지원하려는 직무의 우대사항은 다음과 같아. {jobinfo}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서는 다음과 같아 {letter}"},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"나의 자기소개서가 몇 분단으로 구분되는지 확인해. 문단은 \\n\\n으로 구분되어야 해."},
                 {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"좋은 자기소개서의 조건과, 지원하려는 직무의 우대사항에 알맞는지 모든 문단별로 알려줘. 예시: 첫번째 문단은 두괄식으로 작성하는 게 좋습니다. 해당 자기소개서는 문항에 맞게 삼성전자를 지원하게 된 결정정인 이유와 입사 후, 목표를 뚜렷하게 작성하는 것이 좋습니다. 두번째 문단에서 대학시절의 경험을 작성을 잘 하셨습니다. 하지만 구체적으로, 앱 개발자인만큼 어떤 기술을 사용하였는지를 기술하시는 게 좋을 것 같습니다.  이런식으로 작성해줘."},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": f"문단 별로 첨삭을 해주고, 마지막에 정리 멘트 없이 마지막 문단: ~ 이런 식으로 첨삭을 마무리해줘. "},
                {"role": "assistant", "content": "네, 알겠습니다."},
                {"role": "user", "content": letter}
            ],
            stream=False,  # 수정: 실시간 스트리밍이 필요없는 경우 False로 설정
        )

        # 생성된 피드백 반환
       feedback = completion.choices[0].message
       print(feedback)
    except Exception as e:
        print(f"API 호출 중 오류가 발생했습니다: {str(e)}")

# 사용자의 자기소개서 예시
letter = "삼성전자가 전 세계에서 자사의 기기만으로 생태계를 구축할 수 있는 유일한 회사라고 생각해서 매력을 느끼고 지원하게 되었습니다.\n\n학창 시절에는 핸드폰만 사용하여 기기 간의 연동에 큰 관심이 없었지만, 대학생이 되고 개발 공부를 본격적으로 하게 되자 태블릿, 노트북, 핸드폰간의 파일 공유나 화면공유 같은 연동성의 중요성을 체감하게 되었고, 스마트기기를 벗어나 가전제품으로까지 연동을 확장하는 부분이 참신해서 삼성전자의 일원이 되고 싶다고 생각하게 되었습니다.\n\n생태계를 견고하게 현재도 퀵 쉐어, 세컨드 스크린 무선연결 등 다양한 편의 기능을 제공하고 있고, 계속해서 새로운 편리한 기능들을 만들어 내고 있는 삼성전자이기에 입사후 스마트폰 하나로 집안의 모든 가전제품을 제어하고 편리한 생활을 영위할 수 있게 해주는 스마트홈을 구현하는 일에 참여하고 싶습니다.\n\nAPP SW 프로젝트에서 냉장고 식자재 관리 앱을 개발한 적이 있습니다. 냉장고와 식자재라는 실제 생활과 관련된 프로그램을 개발하니 결과물이 실용적인게 흥미로웠고, 이 경험을 바탕으로 가전제품과 연동되는 휴대전화 앱이나 가전제품 내장 앱에도 관심을 두게 되었습니다. 그래서 삼성전자가 그리는 더욱 편리한 미래 생활의 완성을 위해 애플리케이션을 개발자로 함께하면 좋겠다는 꿈을 꾸게 되었습니다."

print(letter)

callGpt(letter)  # 함수 호출