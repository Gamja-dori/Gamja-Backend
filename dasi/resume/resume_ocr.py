import requests
import uuid
import time
import base64
import json
import re
from openai import OpenAI
import environ, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

# naver ocr
def resume_ocr(image_file, image_file_name):
    file_data = image_file.read()
    if image_file_name[-3:] == 'jpg':
        request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo',
                'data': base64.b64encode(file_data).decode()
                #'url': image_url
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
        }

        payload = json.dumps(request_json).encode('UTF-8')
        headers = {
        'X-OCR-SECRET':  env('OCR_SECRET_KEY'),
        'Content-Type': 'application/json'
        }
    else: 
        request_json = {
            'images': [
                {
                    'format': 'pdf',
                    'name': 'demo',
                    'data': base64.b64encode(file_data).decode()
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = json.dumps(request_json).encode('UTF-8')
        headers = {
        'X-OCR-SECRET': env('OCR_SECRET_KEY'),
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", env('OCR_API_URL'), headers=headers, data = payload)

    res = json.loads(response.text)

    grouped_texts = {}
    # y축 오차 범위
    y_error_range = 5

    for field in res["images"][0]["fields"]:
        height = field["boundingPoly"]["vertices"][0]["y"]
        infer_text = field["inferText"]

        # 오차범위 이내의 같은 y축에 있는 값 같은 열로 취급하기
        closest_height = next((h for h in grouped_texts if abs(height - h) <= y_error_range), None)

        if closest_height is not None:
            grouped_texts[closest_height].append(infer_text)
        else:
            grouped_texts[height] = [infer_text]

    result_string = ''
    for height, texts in sorted(grouped_texts.items()):
        result_string += ' '.join(texts) + '\n'

    return result_string

# 개인 정보 가려내기
def mask_personal_info(text, resume):
    # 이름, 전화번호, 이메일 주소를 가려냄
    name_pattern = re.compile(re.escape(resume.user.name))
    phone_number_pattern = re.compile(r'\b\d{3}[-.]?\d{4}[-.]?\d{4}\b')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    birthdate_pattern = re.compile(r'\b(\d{4})[년./\s-]?[\s]?(\d{1,2})[월./\s-]?[\s]?(\d{1,2})[일]?[생]?\b')
	# 도로명 주소, 몇동몇호만 마스킹
    # address_pattern = re.compile("(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+)")

    # 호부터 다 남아있음
    address_pattern = re.compile("(([가-힣A-Za-z·\d~\-\.]{2,}(도|시))|([가-힣A-Za-z·\d~\-\.]{2,}(시|군|구))|([가-힣A-Za-z·\d~\-\.]{2,}(읍|면))|([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+)")

    # 호부터 다 없어짐 ex) 101호(명륜2가~~) -> 호(명륜2가~~) 없어짐
    # address_pattern = re.compile("(([가-힣A-Za-z·\d~\-\.]{2,}(도|시))|([가-힣A-Za-z·\d~\-\.]{2,}(시|군|구))|([가-힣A-Za-z·\d~\-\.]{2,}(읍|면))|([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+)|([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d]+.*)")

    # 개인 정보 마스킹
    masked_text = name_pattern.sub('이름', text)
    masked_text = phone_number_pattern.sub('번호', masked_text)
    masked_text = email_pattern.sub('메일', masked_text)
    #masked_text = birthdate_pattern.sub('생년월일', masked_text)
    masked_text = address_pattern.sub('주소', masked_text)
    return masked_text

def formatting_career(text):
    OpenAI.api_key = env('GPT_SECRET_KEY')
    client = OpenAI(api_key=env('GPT_SECRET_KEY'))

    command = '경력사항(careers)과 학력사항(educations)만 추출해줘. careers는 duration, company_name, job_name에 대한 정보를 JSON 형식으로 추출해줘. educations는 duration, education_name, education_info에 대한 정보를 JSON 형식으로 추출해줘. duration은 duration: yyyy.MM-yyyy.MM 형식이야. yyyy년-yyyy년으로 입력이 들어온다면 yyyy.03-yyyy.02으로 만들어줘. 만약 없다면 빈 JSON으로 반환해줘'

    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"{command}:\n{text}",
        temperature=0,
        max_tokens=1024,
    )

    result_json = completion.choices[0].text
    result = json.loads(result_json)

    return result
     