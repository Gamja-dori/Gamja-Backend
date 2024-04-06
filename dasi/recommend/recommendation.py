from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Hannanum
from resume.models import *
import numpy as np
import pickle
import nltk

hannanum = Hannanum()
nltk.download("punkt")

def extract_keywords(text):
    # 텍스트에서 키워드 추출
    keywords = hannanum.nouns(text)
    eng_lower = text.lower()
    eng_keywords = nltk.word_tokenize(eng_lower)
    return " ".join(keywords + eng_keywords)  # 단어 리스트를 다시 문자열로 변환하여 반환


def calculate_cosine(a, b):
    # 직무와 직접적으로 관련 없는 stop words
    general_stopwords = ['경험', '능력', '경력', '기술', '업무', '작업', '능숙', '풍부', '향상', '다양', '다양한', '완료', '관련', '특화', '역량', '보유', '담당',
                         '성공', '성공적', '프로젝트', '분야', '활용', '스킬', '목표', '도전', '기록', '노력', '수행', '참여', '참가', '달성', '적용', '적응', '배움',
                         '기여', '협력', '활동', '향상', '성장', '발전']

    # 두 문서 벡터화
    vectorizer = TfidfVectorizer(stop_words=general_stopwords)
    tfidf_matrix = vectorizer.fit_transform([a, b])

    # 첫 번째 문서와 두 번째 문서의 TF-IDF 벡터 추출
    vector_a = tfidf_matrix[0]
    vector_b = tfidf_matrix[1]

    # 유사도 계산
    similarity = np.dot(vector_a, vector_b.T).toarray()[0, 0]

    # 유사도 보정
    similarity *= 3.5

    if similarity > 1:
      similarity = 0.99

    return similarity


def calculate_similarity(project_overview, resumes):
    # 업무 한 줄 소개로부터 키워드 추출
    project_keywords = extract_keywords(project_overview)

    # 이력서별로 유사도 계산
    similarity_scores = []
    for resume in resumes:
        # 이력서로부터 키워드 추출
        text = resume.keyword + resume.introduction
        # performance name + detail 
        # project name + detail
        resume_keywords = extract_keywords(text)
        # 업무 한 줄 소개와 이력서 사이의 유사도 계산
        similarity = calculate_cosine(project_keywords, resume_keywords)
        similarity_scores.append(similarity)

    return similarity_scores


def get_skills_score(required, user):
  if len(required) == 0: # 조건 없음
        return 0
  else:
        common = [required & user]
        return round(len(common) / len(required), 2), common


def get_pay_score(required, user):
  if required == -1:     # 조건 없음
        return 0
  elif user <= required: # 조건 만족
        return 1
  else:                  # 조건 불만족
        return 1 - (user - required) / 1000


def get_career_score(required, user):
  if required == -1:
        return 0
  elif required < user:
        return 1
  else:
        return 1 - (required - user) / 50


def get_final_score(ratio, scores):
  total, divide = 0, 0
  for i in range(5):
        if scores[i]:
          total += scores[i] * ratio[i]
          divide += ratio[i]
  return round((total / divide) * 100)


# 업무 한 줄 소개와 ncs 결과 추출 
def search(project_overview, job_group, job_role, required_skills, required_pay, required_career, commute_type):
    RATIO = (60, 20, 45, 25, 10) # 검색어, ncs, 스킬, 급여, 경력 반영비

    # 직무 -> 직군 -> 전체 순으로 검색
    try:
        if Resume.objects.filter(is_submitted=True, commute_type=commute_type, job_role=job_role).exists():
            resumes = Resume.objects.filter(is_submitted=True, commute_type=commute_type, job_role=job_role)
    except KeyError: 
        try:
            if Resume.objects.filter(is_submitted=True, commute_type=commute_type, job_group=job_group).exists():
                resumes = Resume.objects.filter(is_submitted=True, commute_type=commute_type, job_group=job_group)
        except KeyError:
            resumes = Resume.objects.filter(is_submitted=True, commute_type=commute_type)
    resumes = Resume.objects.all()
    
    final_scores = [0] * len(resumes)

    # 모든 이력서에 대해 검색어 & ncs 점수 한 번에 계산
    search_result = calculate_similarity(project_overview, resumes)
    ncs_result = 1

    # 이력서마다 스킬, 급여, 경력 점수 계산
    for i in range(len(resumes)):
        scores = [0] * 5        # 점수
        recommend_comments = [] # 코멘트

        scores[0] = search_result[i]
        scores[1] = ncs_result

        # 스킬
        required_skills = set(required_skills) # [ , , , ,] -> set ()
        user_skills = set(resumes[i].skills.strip('[]').split(', ')) 
        scores[2], common_skills = get_skills_score(required_skills, user_skills)
        if scores[2] > 0:
            recommend_comments.append({"commentType": 2, "comments": [str(skill) for skill in common_skills[:3]]})

        # 급여
        user_pay = resumes[i].min_month_pay
        scores[3] = get_pay_score(required_pay, user_pay)
        if scores[3] == 1:
            recommend_comments.append({"commentType": 3, "comments": []})

        # 경력
        user_career = resumes[i].career_year
        scores[4] = get_career_score(required_career, user_career)
        if scores[4] == 1:
            recommend_comments.append({"commentType": 4, "comments": [str(user_career)]})

        # 반영비를 고려해 최종 점수 산출
        final_score = get_final_score(RATIO, scores)
        final_scores[i] = (final_score, resumes[i].id, recommend_comments)

    # 점수가 높은 순으로 정렬
    final_resumes = sorted(final_scores, reverse=True) # (점수, 이력서 번호, 코멘트)

    # 결과 반환
    return final_resumes