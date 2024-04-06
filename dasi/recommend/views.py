from .models import *
from resume.models import Resume
from users.models import SeniorUser
from .recommendation import search
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

class SearchResultCreateView(APIView):
    permission_classes = [AllowAny] 
        
    def create_search_result(self, data):
        user_id = data.get("user_id")
        query = data.get("query")
        job_group = data.get("job_group")
        job_role = data.get("job_role")
        min_career_year = data.get("min_career_year")
        skills = data.get("skills")
        max_month_pay = data.get("max_month_pay")
        commute_type = data.get("commute_type")
        
        # 검색 결과 (점수, 이력서 번호, 코멘트)
        search_result = search(query, job_group, job_role, skills, max_month_pay, min_career_year, commute_type)
        
        response_data = {
            "query": query,
            "resumes": []
        }
        
        for score, resume_id, comments in search_result:
            resume = Resume.objects.get(id=resume_id)
            senior_user = SeniorUser.objects.get(id=resume.user_id)
            
            response_data["resumes"].append({
                "resume_id": resume_id,
                "is_verified": resume.is_verified,
                "career_year": resume.career_year,
                "commute_type": resume.commute_type,
                "profile_image": senior_user.profile_image,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "keyword": resume.keyword,
                "skills": resume.skills,    
                "score": score,
                "comments": comments
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200,
        )
    
    
    #@swagger_auto_schema(tags=['시니어 사용자 데이터를 생성합니다.'], request_body=SeniorSerializer)
    def post(self, request):
        # 검색 결과 객체 생성
        response = self.create_search_result(data=request.data)
        return response  
