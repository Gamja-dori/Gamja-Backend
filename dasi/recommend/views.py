from .models import *
from .serializers import *
from resume.models import Resume
from resume.serializers import ResumeSerializer
from users.models import User, SeniorUser
from .recommendation import search
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
import json
from django.core.exceptions import ObjectDoesNotExist
from users.models import Review

def calcReviewAvg(senior):
    reviews = Review.objects.filter(senior=senior)
    if len(reviews) == 0:
        return 0
    avg = round(sum([r.score for r in reviews]) / len(reviews), 1)
    return avg

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
            review_avg = calcReviewAvg(senior_user)
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
                "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
                "review_avg": review_avg,
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )

    
class SearchView(APIView):
    permission_classes = [AllowAny] 
    
    DEFAULT_CAREER_YEAR = 50
    DEFAULT_DURATION = 12
    DEFAULT_PAY = 1000
    
    def get_filtered_resumes(self, data):
        job_group = data.get("job_group")
        job_role = data.get("job_role")
        min_career_year = data.get("min_career_year")
        max_career_year = data.get("max_career_year")
        skills = data.get("skills")
        duration_start = data.get("duration_start")
        duration_end = data.get("duration_end")
        max_month_pay = data.get("max_month_pay")
        min_month_pay = data.get("min_month_pay")
        commute_type = data.get("commute_type")
        
        comment_types = dict()
        filters = {'is_submitted': True}
        if job_group:
            filters['job_group'] = job_group
        if job_role:
            filters['job_role'] = job_role
        if min_career_year != 0:
            comment_types[4] = True
            filters['career_year__gte'] = min_career_year
        if max_career_year != self.DEFAULT_CAREER_YEAR:
            comment_types[4] = True
            filters['career_year__lte'] = max_career_year
        if duration_start != 0: 
            filters['duration_end__gte'] = duration_start
        if duration_end != self.DEFAULT_DURATION: 
            filters['duration_start__lte'] = duration_end
        if min_month_pay != 0:
            comment_types[3] = True
        if max_month_pay != self.DEFAULT_PAY:
            comment_types[3] = True
            filters['min_month_pay__lte'] = max_month_pay

        if commute_type and commute_type != '상주 근무 및 원격 근무':
            filters['commute_type__contains'] = commute_type
            
        resumes = Resume.objects.filter(**filters)
        if skills and skills != '[]': 
            comment_types[2] = json.loads(skills)
            for skill in skills:
                resumes = resumes.filter(skills__icontains=skill)
                
        return resumes, comment_types
        
        
    def create_search_result(self, data):
        user_id = int(data.get("user_id"))
        query = data.get("query")
        
        # 이력서 조건별 필터링
        resumes, comment_types = self.get_filtered_resumes(data=data)
        
        # 유사도 점수 계산
        search_result = search(query, resumes, comment_types, user_id)

        response_data = {
            "resumes": []
        }
        
        for score, resume_id, comments in search_result:
            resume = Resume.objects.get(id=resume_id)
            user = User.objects.get(id=resume.user_id)
            senior_user = SeniorUser.objects.filter(user=user).first()
            review_avg = calcReviewAvg(senior_user)
            response_data["resumes"].append({
                "score": score,
                "resume_id": resume.id,
                "is_verified": resume.is_verified,
                "keyword": resume.keyword,
                "job_group": resume.job_group,
                "job_role": resume.job_role,
                "career_year": resume.career_year,
                "skills": resume.skills, 
                "commute_type": resume.commute_type,
                "comments": comments,
                "name": senior_user.name,
                "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
                "review_avg": review_avg,
            })
        
        return Response(
            data = response_data,
            status=status.HTTP_200_OK,
        )
        
        
    @swagger_auto_schema(tags=['인재 추천 검색 및 필터링 결과를 생성합니다.'], request_body=SearchSerializer)
    def post(self, request):
        response = self.create_search_result(data=request.data)
        return response  
        

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
                review_avg = calcReviewAvg(senior_user)
                res = Response(
                    {
                        "user_id": user.id,
                        "view": resume.view, 
                        "resume_id": resume_id,
                        "is_verified": resume.is_verified,
                        "name": senior_user.name,
                        "profile_image": "https://api.dasi-expert.com" + user.profile_image.url,
                        "review_avg": review_avg,
                        "resume": serializer.data,
                        "message": "이력서를 성공적으로 조회했습니다.",
                    },
                    status=status.HTTP_200_OK,
                )
                return res
        except ObjectDoesNotExist:
            return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)