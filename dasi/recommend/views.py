from .models import *
from .serializers import *
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
        user_id = int(data.get("user"))
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
            senior_user = SeniorUser.objects.get(user_id=resume.user_id)
            
            response_data["resumes"].append({
                "resume_id": resume_id,
                "is_verified": resume.is_verified,
                "career_year": resume.career_year,
                "commute_type": resume.commute_type,
                # "profile_image": senior_user.profile_image,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "keyword": resume.keyword,
                "skills": resume.skills,    
                "score": score,
                "comments": comments
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )
        
    
    @swagger_auto_schema(tags=['인재 추천 검색 결과를 생성합니다.'], request_body=SearchSerializer)
    def post(self, request):
        # 검색 결과 객체 생성
        response = self.create_search_result(data=request.data)
        return response  


class FilterResultCreateView(APIView):
    permission_classes = [AllowAny] 
    
    def filter_resumes(self, data):
        job_group = data.get("job_group")
        job_role = data.get("job_role")
        min_career_year = data.get("min_career_year")
        max_career_year = data.get("max_career_year")
        skills = data.get("skills")
        skills = list(skills.strip('[]').split(', '))
        max_month_pay = data.get("max_month_pay")
        commute_type = data.get("commute_type")
        
        filters = {'is_submitted': True}
        
        if job_group:
            filters['job_group'] = job_group
        if job_role:
            filters['job_role'] = job_role
        if min_career_year:
            filters['career_year__gte'] = min_career_year
        if max_career_year:
            filters['career_year__lte'] = max_career_year
        if max_month_pay:
            filters['min_month_pay__lte'] = max_month_pay
        if commute_type and commute_type != '상주 근무 및 원격 근무':
            filters['commute_type__contains'] = commute_type
        
        resumes = Resume.objects.filter(**filters)
        if skills: 
            for skill in skills:
                resumes = resumes.filter(skills__icontains=skill)
        
        return resumes.values_list('id', flat=True)
    
    
    #@swagger_auto_schema(tags=['시니어 사용자 데이터를 생성합니다.'], request_body=SeniorSerializer)
    def post(self, request):
        filtered_result = self.filter_resumes(request.data)
        
        response_data = {
            "resumes": []
        }
        
        resumes = Resume.objects.filter(id__in=filtered_result)
        senior_users = SeniorUser.objects.filter(user_id__in=resumes.values_list('user_id', flat=True))
        
        for resume, senior_user in zip(resumes, senior_users):            
            response_data["resumes"].append({
                "resume_id": resume.id,
                "is_verified": resume.is_verified,
                "career_year": resume.career_year,
                "commute_type": resume.commute_type,
                "profile_image": senior_user.profile_image,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "keyword": resume.keyword,
                "skills": resume.skills,    
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )