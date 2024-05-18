from django.shortcuts import render, redirect
import environ, os, requests, json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import PaymentSerializer
from .models import Payment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

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
                

class ApproveView(APIView):
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
    

class FailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)
    
    
class CancelView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)