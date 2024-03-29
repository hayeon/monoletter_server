import os
from openai import OpenAI

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def callGpt(letter):
  
    jobinfo = "typescript 개발경험, React, Angular, Vue.js와 같은 자바스크립트 프레임워크를 사용했는지, React를 사용한 경우, next js 사용 경험이 있는지"

    ask = "삼성전자를 지원한 이유와 입사 후 회사에서 이루고 싶은 꿈을 기술하십시오"

    # 자기소개서 체크 및 피드백 생성
    response = client.chat.completions.create(
      model="gpt-4-0125-preview",
      messages=[
        {"role": "system", "content": "You are an AI self-introduction assistant. Read the user's self-introduction letter and point out any conditions and mistakes"},
        {"role": "user", "content": f"나는 회사에 지원하는데 너의 도움이 필요해. 나의 직무는 Front-End developer야. "},
        {"role": "assistant", "content": "네, 당신의 직무를 확인했습니다. ."},
      {"role": "user", "content": f"해당 직무는 다음과 같은 사람을 선호해. {jobinfo}"}, 
        {"role": "assistant", "content": "네, 알겠습니다."},
        {"role": "user", "content": f"나의 자기소개서 질문은 다음과 같아. {ask}"},
        {"role": "assistant", "content": "네, 알겠습니다."},
        {"role": "user", "content": f"나의 자기소개서를 읽고,  {jobinfo} 조건을 3개 이상 만족하지 않다면, 말해줘."},
        {"role": "assistant", "content": "네, 알겠습니다."},
        {"role": "user", "content": letter}
    ],
    stream=True,
)
      

    # 생성된 피드백 반환
    feedback = response.choices[0].message.content
    print(response)

# 사용자의 자기소개서 예시
letter = "삼성전자가 가전제품 영역까지 포함한다면 전 세계에서 자사의 기기만으로 생태계를 구축할 수 있는 유일한 회사라고 생각해서 매력을 느끼고 지원하게 되었습니다. 학창 시절에는 핸드폰만 사용하여 기기 간의 연동에 큰 관심이 없었지만, 대학생이 되고 개발 공부를 본격적으로 하게 되자 태블릿, 노트북, 핸드폰간의 파일 공유나 화면공유 같은 연동성의 중요성을 체감하게 되었고, 스마트기기를 벗어나 가전제품으로까지 연동을 확장하는 부분이 참신해서 삼성전자의 일원이 되고 싶다고 생각하게 되었습니다. 생태계를 견고하게 현재도 퀵 쉐어, 세컨드 스크린 무선연결 등 다양한 편의 기능을 제공하고 있고, 계속해서 새로운 편리한 기능들을 만들어 내고 있는 삼성전자이기에 입사후 스마트폰 하나로 집안의 모든 가전제품을 제어하고 편리한 생활을 영위할 수 있게 해주는 스마트홈을 구현하는 일에 참여하고 싶습니다. 애플리케이션 개발 공개 SW 프로젝트에서 냉장고 식자재 관리 앱을 개발한 적이 있습니다. 냉장고와 식자재라는 실제 생활과 관련된 프로그램을  개발하니 결과물이 실용적인게 흥미로웠고, 이 경험을 바탕으로 가전제품과 연동되는 휴대전화 앱이나 가전제품 내장 앱에도 관심을 두게 되었습니다. 그래서 삼성전자가 그리는 더욱 편리한 미래 생활의 완성을 위해 애플리케이션을 개발자로 함께하면 좋겠다는 꿈을 꾸게 되었습니다."
