from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Hannanum
from resume.models import *
from users.models import *
import numpy as np
import pickle
import nltk
import re

hannanum = Hannanum()

def extract_keywords(text):
    # 한글 키워드 추출
    keywords = hannanum.nouns(text)
    
    # 영문 키워드 추출
    eng_str = re.sub(r"[^a-zA-Z\s]", "", text) # 영문자 + 공백만 남기기
    eng_lower = eng_str.lower()
    eng_keywords = nltk.word_tokenize(eng_lower)
    return " ".join(keywords + eng_keywords)  # 단어 리스트를 다시 문자열로 변환하여 반환


def calculate(a, b):
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
    similarity *= 4

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
        text = resume.job_role + ' ' + resume.keyword + ' ' + resume.introduction
        
        careers = Career.objects.filter(resume_id=resume.id)
        for career in careers:
            if Performance.objects.filter(career_id=career.id).exists():
                performances = Performance.objects.filter(career_id=career.id)
                for p in performances:
                    text += ' ' + p.performance_name + ' ' + p.performance_detail

        if Education.objects.filter(resume_id=resume.id).exists():
            educations = Education.objects.filter(resume_id=resume.id)
            for e in educations:
                text += ' ' + e.education_name + ' ' + e.education_info

        if Project.objects.filter(resume_id=resume.id).exists():
            projects = Project.objects.filter(resume_id=resume.id)
            for p in projects:
                text += ' ' + p.project_name + ' ' + p.project_detail
        
        resume_keywords = extract_keywords(text)
        similarity = calculate(project_keywords, resume_keywords)
        similarity_scores.append(similarity)

    return similarity_scores


def get_final_score(score):
    final_score = round(score * 100)
    return final_score if final_score > 0 else 0


def search(project_overview, resumes, comment_types, user_id):
    final_scores = [0] * len(resumes)
    if user_id != -1:
        user = User.objects.get(id=user_id)
        if user.is_senior:
            member = SeniorUser.objects.get(user_id=user_id)
        else:
            member = EnterpriseUser.objects.get(user_id=user_id)

    # 모든 이력서에 대해 검색어 점수 한 번에 계산
    search_result = calculate_similarity(project_overview, resumes)

    # 이력서마다 코멘트 추가
    for i in range(len(resumes)):
        score = search_result[i] # 점수
        final_score = get_final_score(score)
        comments = []
        
        if score:
            if user_id != -1:
                comments.append({"commentType": 1, "comments": [member.name, final_score]}) # 코멘트 
            else:
                comments.append({"commentType": 1, "comments": ["-", final_score]})

        # 스킬
        if 2 in comment_types:
            required_skills = comment_types[2]
            comments.append({"commentType": 2, "comments": required_skills[:3]})

        # 급여
        if 3 in comment_types:
            comments.append({"commentType": 3, "comments": []})

        # 경력
        if 4 in comment_types:
            comments.append({"commentType": 4, "comments": [str(resumes[i].career_year)]})

        # 최종 점수 산출
        final_scores[i] = (final_score, resumes[i].id, comments)

    # 점수가 높은 순으로 정렬
    final_resumes = sorted(final_scores, reverse=True) # (점수, 이력서 번호, 코멘트)

    # 결과 반환
    return final_resumes