from django.db import models

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.EnterpriseUser', on_delete=models.CASCADE, default=-1)
    item_name = models.CharField(max_length=100)                # 상품명
    total_amount = models.IntegerField()                        # 금액
    
    # 응답에서 받아올 값
    aid = models.CharField(max_length=20, default='')           # 요청 고유 번호
    tid = models.CharField(max_length=20, unique=True, default='')           # 결제 고유 번호
    payment_method_type = models.CharField(max_length=10, default='') # 결제 수단
    card_info = models.CharField(max_length=300, default = "")  # 결제 상세 정보
    amount_info = models.CharField(max_length=300, default='')  # 금액 상세 
    created_at = models.CharField(max_length=20, default='')    # 결제 준비 요청 시각
    approved_at = models.CharField(max_length=20, default='')   # 결제 승인 시각

    class Meta: 
        db_table = 'payments'