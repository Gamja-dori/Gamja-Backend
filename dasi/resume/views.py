from .models import *
from .serializers import CreateResumeSerializer, ChangeResumeTitleSerializer, FindResumeSerializer, ResumeSerializer, PriorResumeSerializer, CareerSerializer, EducationSerializer, ProjectSerializer, PortfolioSerializer, PerformanceSerializer, ResumeCardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import SeniorUser
from django.core.exceptions import ObjectDoesNotExist
from .create_senior_intro import create_intro;

def checkUserExistence(user_id):
    try:
        user = SeniorUser.objects.get(user_id=user_id)
    except ObjectDoesNotExist:
        return False
    return user

def checkResumeExistence(user_id, resume_id):
    user = checkUserExistence(user_id)
    if user:
        try:
            resume = Resume.objects.get(id=resume_id, user=user)
        except ObjectDoesNotExist:
            return False
        return resume
    return False

class CreateResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['새 이력서를 생성합니다.'], request_body=CreateResumeSerializer)
    def post(self, request):
        user_id = request.data.get('user_id')
        user = checkUserExistence(user_id)
        if user:
            serializer = CreateResumeSerializer(data=request.data)
            if serializer.is_valid():
                resume = serializer.create(validated_data=request.data)
                res = Response(
                    {
                        "user_id": user_id,
                        "resume_id": resume.id,
                        "title": resume.title,
                        "is_default": resume.is_default,
                        "created_at": resume.created_at,
                        "message": "이력서가 성공적으로 생성되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class DeleteResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 삭제합니다.'])
    def delete(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            resume.delete()
            res = Response(
                {
                    "message": "이력서가 성공적으로 삭제되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ChangeResumeTitleAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서 제목을 변경합니다.'], request_body=ChangeResumeTitleSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ChangeResumeTitleSerializer(resume, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                res = Response(
                    {
                        "resume_id": resume.id,
                        "title": resume.title,
                        "message": "이력서 제목이 성공적으로 변경되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class SetDefaultResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['해당 이력서를 기본 이력서로 설정합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = FindResumeSerializer(resume, data=request.data, partial=True)
            if serializer.is_valid():
                resumes = Resume.objects.filter(user_id=user_id)
                for r in resumes:
                    r.is_default = False
                    r.save()
                resume.is_default = True
                serializer.save()
                res = Response(
                    {
                        "resume_id": resume.id,
                        "is_default": resume.is_default,
                        "message": "기본 이력서가 성공적으로 변경되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class SubmitResumeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['이력서를 인재풀에 등록합니다.'], request_body=FindResumeSerializer)
    def patch(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = FindResumeSerializer(resume, data=request.data, partial=True)
            if serializer.is_valid():
                resume.is_submitted = True
                serializer.save()
                res = Response(
                    {
                        "resume_id": resume.id,
                        "is_submitted": resume.is_submitted,
                        "message": "이력서가 성공적으로 인재풀에 등록되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class EditResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 수정합니다.'], request_body=ResumeSerializer)
    def put(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ResumeSerializer(resume, data=request.data)
            if serializer.is_valid():
                resume = serializer.update(resume, validated_data=request.data)
                resume.save()
                res = Response(
                    {
                        "resume_id": resume_id,
                        "resume": serializer.data,
                        "message": "이력서가 성공적으로 수정되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
    
class GetResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['이력서 상세 내용을 조회합니다.'])
    def get(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ResumeSerializer(resume)
            res = Response(
                {
                    "user_id": user_id,
                    "resume_id": resume_id,
                    "is_submitted": resume.is_submitted,
                    "resume": serializer.data,
                    "message": "이력서를 성공적으로 조회했습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateResumeDetailAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서 상세 항목을 생성합니다.'])
    def post(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            detail_type = request.data.get('detail_type')
            if detail_type == "careers":
                detail = Career.objects.create(resume=resume)
                detail_serializer = CareerSerializer(detail)
            elif detail_type == "educations":
                detail = Education.objects.create(resume=resume)
                detail_serializer = EducationSerializer(detail)
            elif detail_type == "projects":
                detail = Project.objects.create(resume=resume)
                detail_serializer = ProjectSerializer(detail)
            elif detail_type == "portfolios":
                detail = Portfolio.objects.create(resume=resume)
                detail_serializer = PortfolioSerializer(detail)
            elif detail_type == "performances":
                try: 
                    career_id = request.data.get('career_id')    
                    career = Career.objects.get(id=career_id, resume=resume)
                except ObjectDoesNotExist:
                    return Response({"error": "Career not found"}, status=status.HTTP_404_NOT_FOUND)
                detail = Performance.objects.create(career=career)
                detail_serializer = PerformanceSerializer(detail)
            res = Response(
                {
                    "resume_id": resume_id,
                    "detail_type": detail_type,
                    "detail": detail_serializer.data,
                    "message": "상세 항목이 성공적으로 생성되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteResumeDetailAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서 상세 항목을 삭제합니다.'])
    def delete(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            detail_type = request.data.get('detail_type')
            detail_id = request.data.get('detail_id')
            try:
                if detail_type == "careers":
                    detail = Career.objects.get(id=detail_id, resume=resume)
                elif detail_type == "educations":
                    detail = Education.objects.get(id=detail_id, resume=resume)
                elif detail_type == "projects":
                    detail = Project.objects.get(id=detail_id, resume=resume)
                elif detail_type == "portfolios":
                    detail = Portfolio.objects.get(id=detail_id, resume=resume)
                elif detail_type == "performances":
                    career_id = request.data.get('career_id')
                    career = Career.objects.get(id=career_id, resume=resume)
                    detail = Performance.objects.get(id=detail_id, career=career)
            except ObjectDoesNotExist:
                return Response({"error": "Detail not found"}, status=status.HTTP_404_NOT_FOUND)
            detail.delete()
            res = Response(
                {
                    "resume_id": resume_id,
                    "detail_type": detail_type,
                    "detail_id": detail_id,
                    "message": "상세 항목이 성공적으로 삭제되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

class GetResumeListAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['사용자의 이력서 목록을 조회합니다.'])
    def get(self, request, user_id):
        user = checkUserExistence(user_id)
        if user:
            resumes = ResumeCardSerializer(Resume.objects.filter(user=user), many=True)
            res = Response(
                {
                    "user_id": user_id,
                    "resumes": resumes.data,
                    "message": "이력서 목록을 성공적으로 조회했습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ExtractPriorResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기존 이력서에서 정보를 추출합니다.'], request_body=PriorResumeSerializer)
    def post(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = PriorResumeSerializer(data=request.data)
            if serializer.is_valid():
                careers, educations = serializer.create(validated_data=request.data, resume=resume)
                career_serializer = CareerSerializer(careers, many=True)
                education_serializer = EducationSerializer(educations, many=True)
                res = Response(
                    {
                        "user_id": user_id,
                        "resume_id": resume.id,
                        "careers": career_serializer.data,
                        "educations": education_serializer.data,
                        "message": "이력서 정보가 성공적으로 추출되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)
            
class GetDefaultResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기본 이력서 정보를 조회합니다.'])
    def get(self, request, user_id):
        user = checkUserExistence(user_id)
        if user: 
            default_resume = Resume.objects.filter(user=user, is_default=True)
            if not default_resume:
                res = Response(
                    {
                        "user_id": user_id,
                        "resume": {},
                        "message": "등록된 기본 이력서가 없습니다."
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                serializer = ResumeCardSerializer(default_resume[0])
                res = Response(
                    {
                        "user_id": user_id,
                        "resume": serializer.data,
                        "message": "기본 이력서 정보가 성공적으로 조회되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
            return res
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
def copyDetails(objects, resume_id, isCareer=False):
    if isCareer:
        for o in objects:
            original_career = o.pk
            o.resume_id = resume_id
            o.pk = None
            o.save()
            new_career = Career.objects.last()
            performances = Performance.objects.filter(career_id=original_career)
            for p in performances:
                p.career_id = new_career.pk
                p.pk = None
                p.save()
    else:
        for o in objects:
            o.resume_id = resume_id
            o.pk = None
            o.save()

class CopyResumeAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['기존 이력서를 복제합니다.'], request_body=FindResumeSerializer)
    def post(self, request):
        user_id = request.data.get('user_id')
        resume_id = request.data.get('resume_id')
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            resume.pk = None
            resume.is_default = False
            resume.is_submitted = False
            resume.title = resume.title + "의 사본"
            resume.save()
            new_resume = Resume.objects.last()
            careers = Career.objects.filter(resume_id=resume_id)
            educations = Education.objects.filter(resume_id=resume_id)
            projects = Project.objects.filter(resume_id=resume_id)
            portfolios = Portfolio.objects.filter(resume_id=resume_id)
            copyDetails(careers, new_resume.pk, True)
            copyDetails(educations, new_resume.pk)          
            copyDetails(projects, new_resume.pk)
            copyDetails(portfolios, new_resume.pk)    
            serializer = ResumeCardSerializer(new_resume, data=request.data)
            if serializer.is_valid():
                res = Response(
                    {
                        "user_id": user_id,
                        "resume_id": resume.id,
                        "resume": serializer.data,
                        "message": "이력서가 성공적으로 복제되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CreateSeniorIntroAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['이력서를 바탕으로 전문가 소개를 생성합니다.'], request_body=ResumeSerializer)
    def post(self, request, user_id, resume_id):
        resume = checkResumeExistence(user_id, resume_id)
        if resume:
            serializer = ResumeSerializer(resume, data=request.data)
            if serializer.is_valid():
                createdIntro = create_intro(request.data)
                res = Response(
                    {
                        "resume_id": resume_id,
                        "introduction": createdIntro,
                        "message": "전문가 소개가 성공적으로 생성되었습니다."
                    },
                    status=status.HTTP_200_OK,
                )
                return res
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)