from django.shortcuts import render, redirect
import environ, os, requests, json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

class MainView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, '../templates/index.html')
    
    @swagger_auto_schema(tags=['카카오페이 결제 요청을 전송합니다.'])
    def post(self, request):
        URL = 'https://open-api.kakaopay.com/online/v1/payment/ready'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }
        params = {
            "cid": "TC0ONETIME",            # 테스트용 코드
            "partner_order_id": "1001",     # 주문번호
            "partner_user_id": "german",    # 유저 아이디
            "item_name": "연어초밥",         # 상품명
            "quantity": "1",                # 상품 수량
            "total_amount": "12000",        # 상품 총액
            "tax_free_amount": "0",         # 상품 비과세 금액
            "approval_url": "http://localhost:8000/payments/approve/", # 결제 성공 시 이동할 url
            "fail_url": "http://localhost:8000/payments/fail/",        # 결제 실패 시 이동할 url            
            "cancel_url": "http://localhost:8000/payments/cancel/"     # 결제 취소 시 이동할 url
        } 
        
        # 카카오페이 서버에 결제 요청 전송
        response = requests.post(URL, headers=headers, json=params) 
        try:       
            # 결제 승인 시 사용할 tid를 세션에 저장
            if 'tid' in request.session:
                del request.session['tid']
            request.session['tid'] = response.json()['tid']  
            
            # 결제 페이지 url로 redirect
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
        URL = 'https://open-api.kakaopay.com/online/v1/payment/approve'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }
        params = {
            "cid": "TC0ONETIME",            
            "tid": request.session['tid'],
            "partner_order_id": "1001",
            "partner_user_id": "german",
            "pg_token": request.GET.get("pg_token")
        }         
        
        response = requests.post(URL, headers=headers, json=params)
        response = json.loads(response.text)
        return Response(response)
    

class FailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)
    
    
class CancelView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response(status=200)