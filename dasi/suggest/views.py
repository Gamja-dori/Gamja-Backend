from django.shortcuts import render, redirect
import environ, os, requests, json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from .serializers import *
from .models import *
from users.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env()

class CreateSuggestView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['기업 사용자가 채용 제안을 전송합니다.'], request_body=SuggestSerializer)
    def post(self, request):
        serializer = SuggestSerializer(data=request.data)
            
        if serializer.is_valid():
            # 시니어, 기업, 이력서의 존재 여부 검증
            try:
                senior = SeniorUser.objects.get(user_id=request.data['senior_id'])
                EnterpriseUser.objects.get(user_id=request.data['enterprise_id'])
                Resume.objects.get(id=request.data['resume_id'], user=senior)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            # 채용 제안 생성
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


class BaseListView(APIView):
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


class GetSeniorListView(BaseListView):
    model = EnterpriseUser
    filter_field = 'enterprise'
    is_paid = None
    
    def get(self, request, user_id):
        suggests = self.get_suggests_list(user_id)
        if suggests is None:
            return Response({"error": "Invalid user or no suggests found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        if self.is_paid is None:
            pass
        elif self.is_paid: 
            suggests = suggests.filter(progress='is_paid')
        else:
            suggests = Suggest.objects.exclude(progress='is_paid')
        
        response_data = {
            "suggests": [
                {
                    "suggest_id": suggest.id,
                    "is_verified": suggest.resume.is_verified,
                    "resume_id": suggest.resume.id,
                    "name": suggest.senior.name,
                    "career_year": suggest.resume.career_year,
                    "job_group": suggest.resume.job_group,
                    "job_name": suggest.resume.job_role,
                    "date": suggest.resume.created_at,
                    "commute_type": suggest.resume.commute_type, 
                    "profile_image": "https://api.dasi-expert.com" + suggest.senior.user.profile_image.url,
                    "progress": suggest.progress
                } 
                for suggest in suggests
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class GetPaidSeniorListView(GetSeniorListView):
    is_paid = True

    @swagger_auto_schema(tags=['기업 사용자의 결제 완료된 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        return super().get(request, user_id)


class GetUnpaidSeniorListView(GetSeniorListView):
    is_paid = False
    
    @swagger_auto_schema(tags=['기업 사용자의 결제되지 않은 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        return super().get(request, user_id)
    
    
class GetEnterpriseNotificationsView(BaseListView):
    model = EnterpriseUser
    filter_field = 'enterprise'
    
    @swagger_auto_schema(tags=['기업 사용자의 알림창에서 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        suggests = self.get_suggests_list(user_id)
        if suggests is None:
            return Response({"error": "Invalid user or no suggests found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "suggests": [
                {
                    "suggest_id": suggest.id,
                    "resume_id": suggest.resume.id,
                    "name": suggest.senior.name,
                    "progress": suggest.progress,
                    "is_read": suggest.is_enterprise_read,
                    "profile_image": "https://api.dasi-expert.com" + suggest.senior.user.profile_image.url,
                }
                for suggest in suggests
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class GetSeniorNotificationsView(BaseListView):
    model = SeniorUser
    filter_field = 'senior'
    
    @swagger_auto_schema(tags=['시니어 사용자의 알림창에서 채용 제안 목록을 조회합니다.'])
    def get(self, request, user_id):
        suggests = self.get_suggests_list(user_id)
        if suggests is None:
            return Response({"error": "Invalid user or no suggests found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "suggests": [
                {
                    "suggest_id": suggest.id,
                    "resume_id": suggest.resume.id,
                    "company": suggest.enterprise.company,
                    "progress": suggest.progress,
                    "is_read": suggest.is_senior_read,
                    "profile_image": "https://api.dasi-expert.com" + suggest.enterprise.user.profile_image.url,
                }
                for suggest in suggests
            ]
        }
        return Response(response_data, status=status.HTTP_200_OK)


class GetNotificationCountView(APIView):   
    permission_classes = [AllowAny]
     
    @swagger_auto_schema(tags=['새로운 알림 개수를 조회합니다.'])
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_senior:
                senior = SeniorUser.objects.get(user=user)
            else:
                enterprise = EnterpriseUser.objects.get(user=user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_senior:
            notifications_count = Suggest.objects.filter(senior=senior, is_senior_read=False).count() 
        else:
            notifications_count = Suggest.objects.filter(enterprise=enterprise, is_enterprise_read=False).count() 
        
        return Response({
            "notifications_count": notifications_count,
        }, status=status.HTTP_200_OK)
        
        
class PatchNotificationView(APIView):
    permission_classes = [AllowAny]
    
    def get_suggest_from_user(self, user, suggest_id):
        if user.is_senior:
            senior = SeniorUser.objects.get(user=user)
            suggest = Suggest.objects.get(id=suggest_id, senior=senior)
        else:
            enterprise = EnterpriseUser.objects.get(user=user)
            suggest = Suggest.objects.get(id=suggest_id, enterprise=enterprise)   
        return suggest 
    
    @swagger_auto_schema(tags=['채용 제안 열람 여부를 갱신합니다.'])
    def patch(self, request):
        user_id = request.data.get('user_id')
        suggest_id = request.data.get('suggest_id')
        is_read = request.data.get('is_read')
        
        if user_id is None or suggest_id is None or is_read is None:
            return Response({"error": "User ID, Suggest ID, is_read field are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            suggest = self.get_suggest_from_user(user, suggest_id) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # 열람 여부 갱신
        if user.is_senior:
            suggest.is_senior_read = is_read
            response_data = suggest.is_senior_read
        else:
            suggest.is_enterprise_read = is_read 
            response_data = suggest.is_enterprise_read
        suggest.save()

        return Response({
            "suggest_id": suggest.id,
            "is_read": response_data,
            "message": "채용 제안 열람 여부가 성공적으로 갱신되었습니다."
        }, status=status.HTTP_200_OK)
        

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
            "commute_type": suggest.commute_type,
            "start_year_month": suggest.start_year_month,
            "end_year_month": suggest.end_year_month,
            "pay": suggest.pay,
            "duration": suggest.duration,
            "job_description": suggest.job_description,
            "progress": suggest.progress,
            "is_expired": suggest.is_expired,
            "company": suggest.enterprise.company,
            "profile_image": "https://api.dasi-expert.com" + suggest.enterprise.user.profile_image.url
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

class GetProgressView(APIView):
    permission_classes = [AllowAny]   
    
    @swagger_auto_schema(tags=['채용 제안의 상태를 조회합니다.'])
    def get(self, request, suggest_id):
        try:
            suggest = Suggest.objects.get(id=suggest_id) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "suggest_id": suggest.id,
            "progress": suggest.progress,
            "is_senior_read": suggest.is_senior_read,
            "is_enterprise_read": suggest.is_enterprise_read,
            "message": "채용 제안의 상태를 성공적으로 조회했습니다."
        }, status=status.HTTP_200_OK)
        

class UpdateProgressView(APIView):
    permission_classes = [AllowAny]   
    
    @swagger_auto_schema(tags=['채용 제안의 상태를 변경합니다.'])
    def patch(self, request):
        try:
            suggest_id = request.data.get('suggest_id')
            suggest = Suggest.objects.get(id=suggest_id) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        progress = request.data.get('progress')
        if progress not in ['is_pending', 'is_declined', 'is_cancelled', 'is_paid', 'is_accepted', 'is_reviewed']:
            return Response({"error": "Progress is invalid. Possible choices are 'is_pending', 'is_declined', 'is_cancelled', 'is_paid', 'is_accepted'."}
                            , status=status.HTTP_400_BAD_REQUEST)
        
        # 상태 설정 및 사용자의 읽은 상태 변경    
        suggest.progress = progress
        if progress in ['is_accepted', 'is_declined', 'is_paid']:
            suggest.is_senior_read = True
            suggest.is_enterprise_read = False 
        elif progress == 'is_cancelled':
            suggest.is_senior_read = False  
            suggest.is_enterprise_read  = True 
        elif progress == 'is_reviewed':
            suggest.is_senior_read = True  
            suggest.is_enterprise_read  = True 
        suggest.save()

        return Response({
            "suggest_id": suggest.id,
            "progress": suggest.progress,
            "is_senior_read": suggest.is_senior_read,
            "is_enterprise_read": suggest.is_enterprise_read,
            "message": "채용 제안의 상태가 성공적으로 변경되었습니다."
        }, status=status.HTTP_200_OK)
  
    
class PaymentRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags=['카카오페이 결제 요청을 전송합니다.'])
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        payment = serializer.create(validated_data=request.data)
        
        URL = 'https://open-api.kakaopay.com/online/v1/payment/ready'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }
        params = {
            "cid": "TC0ONETIME",                           # 테스트용 코드
            "partner_order_id": str(payment.id),           # 주문번호
            "partner_user_id": str(payment.suggest.enterprise.user_id), # 유저 아이디
            "item_name": str(payment.item_name),           # 상품명
            "quantity": "1",                               # 상품 수량
            "total_amount": str(payment.total_amount),     # 상품 총액
            "tax_free_amount": "0",                        # 상품 비과세 금액
            "approval_url": f"https://dasi-expert.com/suggestion/payment/{payment.suggest.resume.id}/{payment.suggest.id}", # 결제 성공 시 이동할 url
            "fail_url": f"https://dasi-expert.com/suggestion/payment/{payment.suggest.resume.id}",  # 결제 실패 시 이동할 url            
            "cancel_url": f"https://dasi-expert.com/suggestion/payment/{payment.suggest.resume.id}/{payment.suggest.id}" # 결제 취소 시 이동할 url
        } 
        
        # 카카오페이 서버에 결제 요청 전송
        response = requests.post(URL, headers=headers, json=params) 
        try:       
            # 결제 승인 시 사용할 tid 저장
            tid = response.json()['tid']  
            serializer = PaymentSerializer(data=request.data)
            serializer.update_tid(tid, payment.id)
            
            response = json.loads(response.text)
            response["payment_id"] = payment.id
            return Response(response)
        except:
            data = {
                "message": '결제 요청에 실패했습니다.',
                "error_code": str(response.json()['error_code']),
                "error_message": response.json()['error_message']
            }
            return Response(status=500, data=data)
                

class PaymentApproveView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, payment_id, pg_token):
        payment = Payment.objects.get(id=payment_id)
        
        URL = 'https://open-api.kakaopay.com/online/v1/payment/approve'
        headers = {
            "Authorization": "SECRET_KEY " + env('KAKAO_SECRET_KEY'),  
            "Content-Type": "application/json"
        }        
        params = {
            "cid": "TC0ONETIME",            
            "tid": payment.tid,
            "partner_order_id": str(payment.id),
            "partner_user_id": str(payment.suggest.enterprise.user_id),
            "pg_token": pg_token
        }         
        
        response = requests.post(URL, headers=headers, json=params)
        response = json.loads(response.text)
        
        if "cid" in response:
            serializer = PaymentSerializer(data=response)
            serializer.update(response, payment.id)
            suggest = payment.suggest
            suggest.progress = "is_paid" 
            suggest.is_senior_read = True
            suggest.is_enterprise_read = False  
            suggest.save()    
        
        return Response(response)
    

class GetIsPaidView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(tags=['채용 제안의 결제 여부를 조회합니다.'])
    def get(self, request, suggest_id):
        try:
            suggest = Suggest.objects.get(id=suggest_id)
        except Suggest.DoesNotExist:
            return Response({"error": "Suggest not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if suggest.progress == 'is_paid':
            res = True
        else:
            res = False
            
        return Response({
            "is_paid": res
        }, status=status.HTTP_200_OK) 
        