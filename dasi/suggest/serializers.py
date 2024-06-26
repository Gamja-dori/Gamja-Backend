from rest_framework import serializers
from .models import *
from users.models import SeniorUser, EnterpriseUser
from resume.models import Resume

class SuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggest
        fields = ['senior', 'enterprise', 'resume', 'commute_type', 'start_year_month', 'end_year_month', 'pay', 'job_description']

    def create(self, validated_data):
        senior = SeniorUser.objects.get(user_id=validated_data['senior_id'])
        enterprise = EnterpriseUser.objects.get(user_id=validated_data['enterprise_id'])
        resume = Resume.objects.get(id=validated_data['resume_id'], user=senior)

        suggest = Suggest.objects.create(
            senior=senior,
            enterprise=enterprise,
            resume=resume,
            commute_type=validated_data['commute_type'],
            start_year_month=validated_data['start_year_month'],
            end_year_month=validated_data['end_year_month'],
            pay=validated_data['pay'],
            duration=validated_data['duration'],
            job_description=validated_data['job_description'],
        )
        return suggest  
    
    
class CreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['suggest_id', 'item_name', 'total_amount']
        
    def create(self, validated_data):
        suggest = Suggest.objects.get(id=validated_data['suggest_id'])
        
        payment = Payment.objects.create(
            suggest=suggest,
            item_name=validated_data['item_name'],
            total_amount=validated_data['total_amount']
        )
        return payment
    
    
class PaymentSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Payment
        fields = '__all__'

    def update_tid(self, tid, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.tid = tid
            payment.save()
            return payment
        except Payment.DoesNotExist:
            return None
    
    def update(self, data, payment_id):
        allowed_fields = {'aid', 'payment_method_type', 'card_info', 'amount_info', 'created_at', 'approved_at'}
        
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return None
        
        # 허용된 필드 업데이트
        for attr, value in data.items(): 
            if attr in allowed_fields:
                setattr(payment, attr, value)
        
        payment.save()
        return payment