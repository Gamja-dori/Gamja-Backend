from .models import *
from .serializers import *
from resume.models import Resume
from resume.views import checkResumeExistence
from resume.serializers import ResumeSerializer
from users.models import User, SeniorUser
from .recommendation import search
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
import base64
from django.core.exceptions import ObjectDoesNotExist

def encode_base64(image_file):
    with open(image_file.path, "rb") as f: # 바이너리 읽기 모드로 열기
        image_data = f.read()
    return base64.b64encode(image_data)    


class MainView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['지금 떠오르는 인재 목록을 조회합니다.'])
    def get(self, request):
        response_data = {
            "resumes": []
        }
        
        resumes = Resume.objects.filter(is_submitted=True).order_by('view')
        LIMIT = 3
        cnt = 0
        
        for resume in resumes: 
            cnt += 1
            if cnt > LIMIT:
                break
            
            user = User.objects.filter(id=resume.user_id).first()
            senior_user = SeniorUser.objects.filter(user=user).first()
            response_data["resumes"].append({
                "resume_id": resume.id,
                "is_verified": resume.is_verified,
                "keyword": resume.keyword,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "career_year": resume.career_year,
                "skills": resume.skills, 
                "commute_type": resume.commute_type,
                "name": senior_user.name,
                "profile_image": user.profile_image.url,
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )
    
    
class SearchResultCreateView(APIView):
    permission_classes = [AllowAny] 
        
    def create_search_result(self, data):
        user_id = int(data.get("user_id"))
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
            "resumes": []
        }
        
        for score, resume_id, comments in search_result:
            resume = Resume.objects.get(id=resume_id)
            user = User.objects.get(id=resume.user_id)
            senior_user = SeniorUser.objects.filter(user=user).first()
            
            response_data["resumes"].append({
                "resume_id": resume.id,
                "is_verified": resume.is_verified,
                "keyword": resume.keyword,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "career_year": resume.career_year,
                "skills": resume.skills, 
                "commute_type": resume.commute_type,
                "score": score,
                "comments": comments,
                "name": senior_user.name,
                "profile_image": user.profile_image.url,
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )
        
    @swagger_auto_schema(tags=['인재 추천 검색 결과를 생성합니다.'], request_body=SearchSerializer)
    def post(self, request):
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
    
    @swagger_auto_schema(tags=['인재 필터링 결과를 반환합니다.'], request_body=FilterSerializer)
    def post(self, request):
        filtered_result = self.filter_resumes(request.data)
        
        response_data = {
            "resumes": []
        }
        
        resumes = Resume.objects.filter(id__in=filtered_result)
        users = User.objects.filter(id__in=resumes.values_list('user_id', flat=True))
        
        for resume, user in zip(resumes, users): 
            senior_user = SeniorUser.objects.filter(user=user).first()
            response_data["resumes"].append({
                "resume_id": resume.id,
                "is_verified": resume.is_verified,
                "keyword": resume.keyword,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "career_year": resume.career_year,
                "skills": resume.skills, 
                "commute_type": resume.commute_type,
                "name": senior_user.name,
                "profile_image": user.profile_image.url,
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )
        

class ResumeDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기업 사용자가 시니어 전문가의 이력서 상세 내용을 조회합니다.'])
    def get(self, request, resume_id):
        try:
            resume = Resume.objects.get(id=resume_id)
            if resume:
                serializer = ResumeSerializer(resume)
                resume.view += 1
                resume.save()
                user = User.objects.get(id=resume.user_id)
                senior_user = SeniorUser.objects.filter(user=user).first()
                res = Response(
                    {
                        "view": resume.view, 
                        "resume_id": resume_id,
                        "is_verified": resume.is_verified,
                        "name": senior_user.name,
                        "profile_image": encode_base64(user.profile_image),
                        "resume": serializer.data,
                        "message": "이력서를 성공적으로 조회했습니다.",
                    },
                    status=status.HTTP_200_OK,
                )
                return res
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)