from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Hannanum
from elasticsearch import Elasticsearch
from resume.models import *
from users.models import *
import numpy as np
import pickle
import re, json

es = Elasticsearch(
        hosts=['http://es:9200'],
        http_auth=("elastic", "changeme")
    )

def create_index():
    es.indices.create(
        index='resumes', 
        body={ 
    "settings": {
        "analysis": { 
            "analyzer": {
                "my_analyzer": {
                "type": "custom",
                "tokenizer": "nori_tokenizer",
                "filter": ["nori_filter", "stop_filter"],
                "char_filter": ["html_strip"]
                }
            },
            "filter": {
            "nori_filter": {
                "type": "nori_part_of_speech",
                "stoptags": [
                    "E", "IC", "J", "MAG", "MAJ",
                    "MM", "SP", "SSC", "SSO", "SC",
                    "SE", "XPN", "XSA", "XSN", "XSV",
                    "UNA", "NA", "VSV"
                ]
            },
            "stop_filter": {
                "type": "stop",
                "stopwords": ['경험', '능력', '경력', '기술', '업무', '작업', '능숙', '풍부', '향상', '다양', '다양한', '완료', '관련', '특화', '역량', '보유', '담당',
                            '성공', '성공적', '프로젝트', '분야', '활용', '스킬', '목표', '도전', '기록', '노력', '수행', '참여', '참가', '달성', '적용', '적응', '배움',
                            '기여', '협력', '활동', '향상', '성장', '발전']  
                }
            }
        }},
        "mappings": {
                "properties": {
                        "id": {
                            "type": "long"
                        },
                        "content": {
                            "type": "text",
                            "analyzer": "my_analyzer"
                        }
                    }
            }
    })
    
    
def delete_index():
    es.indices.delete(index='resumes') 


def index_datas(resumes):
    body = ""
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
        
        body += json.dumps({"index": {"_index": "resumes"}}) + '\n'
        body += json.dumps({
            "id": resume.id,
            "content": text
        }, ensure_ascii=False) + '\n' 

    es.bulk(body) 
    es.indices.refresh(index='resumes')  # 인덱스 리프레시


def delete_datas():
    es.delete_by_query(
    index='resumes',
    body={
        "query": {
                "match_all": {}
            }
        }
    )
    es.indices.refresh(index='resumes')  # 인덱스 리프레시


def get_final_score(score): 
    k = 0.5
    score = score / ( k + score ) 
    final_score = round(score * 100) 
    return final_score if final_score > 0 else 0 


def search(project_overview, resumes, comment_types, user_id): 
    if user_id != -1:
        user = User.objects.get(id=user_id)
        if user.is_senior:
            member = SeniorUser.objects.get(user_id=user_id)
        else:
            member = EnterpriseUser.objects.get(user_id=user_id)

    # 이력서 생성
    if not es.indices.exists(index='resumes'): 
        create_index()
    
    # 이력서 데이터 인덱싱
    delete_datas()
    if not es.count(index='resumes')['count']:
        index_datas(resumes)
          
    # 검색
    docs = es.search(index='resumes',
        body={
            "query": {
                "match": {
                    "content": project_overview
                }
            }
        }
    )
    
    # (점수, 이력서 번호, 코멘트)
    results = dict()
    
    # 이력서 ID 리스트
    id_list = []
    print(docs)
    for hit in docs['hits']["hits"]:
        resume_id = hit["_source"]["id"]
        id_list.append(resume_id)
        similarity_score = hit["_score"]  
        results[resume_id] = similarity_score
    
    resumes_cnt = docs['hits']['total']['value']
    print(resumes_cnt, len(id_list))
    
    final_scores = [0] * len(id_list)
    
    # 이력서마다 코멘트 추가
    for i in range(len(id_list)):
        score = results[id_list[i]] # 점수 
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
            resume = Resume.objects.get(id=id_list[i]) 
            comments.append({"commentType": 4, "comments": [str(resume.career_year)]})

        # 최종 점수 산출
        final_scores[i] = [final_score, id_list[i], comments]

    # 점수가 높은 순으로 정렬
    print(final_scores)
    final_resumes = sorted(final_scores, reverse=True) # (점수, 이력서 번호, 코멘트)

    # 결과 반환
    return final_resumes
