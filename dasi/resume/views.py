from .models import *
from .serializers import CreateResumeSerializer, EditResumeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from users.models import SeniorUser

class CreateResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['새 이력서를 생성합니다.'], request_body=CreateResumeSerializer)
    def post(self, request):
        serializer = CreateResumeSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.create(validated_data=request.data)
            res = Response(
                {
                    "user_id": resume.user.user_id,
                    "resume_id": resume.id,
                    "title": resume.title,
                    "created_at": resume.created_at,
                    "message": "이력서가 생성되었습니다."
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteResumeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(tags=['이력서를 삭제합니다.'])
    def delete(self, request, user_id, resume_id):
        user = SeniorUser.objects.filter(user_id=user_id)[0]
        delete_resume = Resume.objects.get(id=resume_id, user=user)
        delete_resume.delete()
        res = Response(
            {
                "message": "이력서가 삭제되었습니다."
            },
            status=status.HTTP_200_OK,
        )
        return res