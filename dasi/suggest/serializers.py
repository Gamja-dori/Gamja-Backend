from rest_framework import serializers
from .models import *
from users.models import EnterpriseUser

class PaymentSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Payment
        fields = '__all__'
        
    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        user = EnterpriseUser.objects.filter(user_id=user_id)[0]
        item_name = validated_data.get('item_name')
        total_amount = validated_data.get('total_amount')
            
        payment = Payment.objects.create(
            user=user,
            item_name=item_name,
            total_amount=total_amount
        )
        payment.save()
        return payment

    def update_tid(self, tid, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.tid = tid
            payment.save()
            return payment
        except Payment.DoesNotExist:
            return None
    
    def update(self, data, payment_id):
        aid = data.get('aid')
        payment_method_type = data.get('payment_method_type')
        card_info = data.get('card_info')
        amount_info = data.get('amount_info')
        created_at = data.get('created_at')
        approved_at = data.get('approved_at')
        
        try:
            payment = Payment.objects.get(id=payment_id)
            payment.aid = aid
            payment.payment_method_type = payment_method_type
            payment.card_info = card_info
            payment.amount_info = amount_info
            payment.created_at = created_at
            payment.approved_at = approved_at
            payment.save()
            return payment
        except Payment.DoesNotExist:
            return None