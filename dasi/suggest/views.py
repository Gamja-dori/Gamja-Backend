from django.shortcuts import render, redirect
import environ, os, requests, json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from .models import *
from users.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

class SuggestCreateView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['기업 사용자가 채용 제안을 전송합니다.'])
    def post(self, request):
        serializer = SuggestSerializer(data=request.data)
            
        if serializer.is_valid():
            suggest = serializer.create(validated_data=request.data)
            res = Response(
                {
                    "suggest_id": str(suggest.id),
                    "message": "채용 제안이 성공적으로 생성되었습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
            return res        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetListViewBase(APIView):
    permission_classes = [AllowAny]
    model = None
    filter_field = None

    def get_suggests_list(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return None 
        
        if not (self.model == SeniorUser and user.is_senior) and not (self.model == EnterpriseUser and user.is_enterprise):
            return None        
        
        member = self.model.objects.filter(user=user).first()
        if not member:
            return None
        
        suggests = Suggest.objects.filter(**{self.filter_field: member})
        
        return suggests
       

class GetEnterpriseListView(GetListViewBase):
    model = SeniorUser
    filter_field = 'senior'
    
    @swagger_auto_schema(tags=['시니어 사용자가 받은 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        suggests = self.get_suggests_list(user_id)
        if suggests is None:
            return Response({"error": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "suggests": [
                {
                    "suggest_id": suggest.id,
                    "company": suggest.enterprise.company,
                    "is_cancelled": suggest.is_cancelled,
                    "profile_image": "https://api.dasi-expert.com" + suggest.enterprise.user.profile_image.url,
                }
                for suggest in suggests
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class GetSeniorListView(GetListViewBase):
    model = EnterpriseUser
    filter_field = 'enterprise'
    
    @swagger_auto_schema(tags=['기업 사용자가 보낸 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        suggests = self.get_suggests_list(user_id)
        
        if suggests is None:
            return Response({"error": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "suggests": [
                {
                    "suggest_id": suggest.id,
                    "name": suggest.senior.name,
                    "is_accepted": suggest.is_accepted,
                    "profile_image": "https://api.dasi-expert.com" + suggest.senior.user.profile_image.url,
                }
                for suggest in suggests
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)


class GetSuggestDetailView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['채용 제안의 상세 내용을 조회합니다.'])
    def get(self, request, suggest_id):
        try:
            suggest = Suggest.objects.get(id=suggest_id)
        except ObjectDoesNotExist:
            return Response({"error": "Suggest Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "suggest_id": suggest.id,
            "start_year_month": suggest.start_year_month,
            "end_year_month": suggest.end_year_month,
            "suggest_id": suggest.id,
            "pay": suggest.pay,
            "duration": suggest.duration,
            "job_description": suggest.job_description,
            "is_cancelled": suggest.is_cancelled,
            "is_accepted": suggest.is_accepted,
            "is_paid": suggest.is_paid,
            "is_expired": suggest.is_expired,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    
class PaymentRequestView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['카카오페이 결제 요청을 전송합니다.'])
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        payment = serializer.create(validated_data=request.data)
        device = request.data.get("device")
        
        URL = 'https://open-api.kakaopay.com/online/v1/payment/ready'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }
        params = {
            "cid": "TC0ONETIME",                           # 테스트용 코드
            "partner_order_id": str(payment.id),           # 주문번호
            "partner_user_id": str(payment.user.user_id),  # 유저 아이디
            "item_name": str(payment.item_name),           # 상품명
            "quantity": "1",                               # 상품 수량
            "total_amount": str(payment.total_amount),     # 상품 총액
            "tax_free_amount": "0",                        # 상품 비과세 금액
            "approval_url": "http://localhost:8000/pay/approve/", # 결제 성공 시 이동할 url
            "fail_url": "http://localhost:8000/pay/fail/",        # 결제 실패 시 이동할 url            
            "cancel_url": "http://localhost:8000/pay/cancel/"     # 결제 취소 시 이동할 url
        } 
        
        # 카카오페이 서버에 결제 요청 전송
        response = requests.post(URL, headers=headers, json=params) 
        try:       
            # 결제 승인 시 사용할 tid를 세션에 저장
            if 'tid' in request.session:
                del request.session['tid']
            tid = response.json()['tid']  
            request.session['tid'] = tid
            serializer.update_tid(tid, payment.id)
            
            # 결제 페이지 url로 redirect
            if device == "mobile":
                next_url = response.json()['next_redirect_mobile_url'] 
            else:
                next_url = response.json()['next_redirect_pc_url'] 
            return redirect(next_url)
        except:
            data = {
                "message": '결제 요청에 실패했습니다.',
                "error_code": str(response.json()['error_code']),
                "error_message": response.json()['error_message']
            }
            return Response(status=500, data=data)
                

class PaymentApproveView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        payment = Payment.objects.get(tid=request.session['tid'])
        
        URL = 'https://open-api.kakaopay.com/online/v1/payment/approve'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }        
        params = {
            "cid": "TC0ONETIME",            
            "tid": request.session['tid'],
            "partner_order_id": str(payment.id),
            "partner_user_id": str(payment.user.user_id),
            "pg_token": request.GET.get("pg_token")
        }         
        
        response = requests.post(URL, headers=headers, json=params)
        response = json.loads(response.text)
        if "cid" in response:
            PaymentSerializer.update(request.data, payment.id)      
        
        return Response(response)
    

class PaymentFailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)
    
    
class PaymentCancelView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)