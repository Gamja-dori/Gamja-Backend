import json
from openai import OpenAI
import environ, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

def create_intro(resume):
    resume = json.dumps(resume)
    OpenAI.api_key = env('GPT_SECRET_KEY')
    client = OpenAI(api_key=env('GPT_SECRET_KEY'))

    command = '주어진 JSON 형식의 이력서 정보를 바탕으로 이 사람의 자기 소개를 다음의 구조대로 HTML 문법에 맞게 써줘. 일반적인 이야기 말고 이 사람의 개성이 보이게 작성해줘. HTML 문법은 최대한 다양하게 사용해줘. 자기소개(전문가를 소개할 수 있는 요약 한 줄), 이런 기업을 도와줄 수 있어요(전문가를 필요로하는 기업의 수요와 전문가가 도와줄 수 있는 부분에 대해 최대한 구체적으로 서술), 자신 있는 분야(전문가가 참여할 수 있는 자신 있는 분야의 프로젝트에 대해 최대한 구체적으로 서술), 예상 산출물(전문가가 기업과 협업하면 낼 수 있는 결과물에 대해 최대한 구체적으로 서술) 총 4가지 항목에 대해 작성해줘. HTML 문법은 최대한 다양하게, 서술형과 목록형을 섞어서 사용해줘.'

    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"{command}:\n{resume}",
        temperature=0,
        max_tokens=1024,
    )

    result = completion.choices[0].text

    return result