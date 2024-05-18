from django.db import models

class Suggest(models.Model):
    id = models.AutoField(primary_key=True)
    enterprise = models.ForeignKey('users.EnterpriseUser', on_delete=models.CASCADE, default=-1)
    senior = models.ForeignKey('users.SeniorUser', on_delete=models.CASCADE, default=-1)
    start_year_month = models.CharField(max_length=7)            
    end_year_month = models.CharField(max_length=7)                       
    pay = models.IntegerField()
    duration = models.IntegerField()
    job_description = models.TextField()
    is_cancelled = models.BooleanField(default=False) # 채용 취소 여부
    is_accepted = models.BooleanField(default=False)  # 제안 수락 여부
    is_paid = models.BooleanField(default=False)      # 결제 여부
    is_expired = models.BooleanField(default=False)   # 계약 만료 여부
    
    class Meta: 
        db_table = 'suggests'


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.EnterpriseUser', on_delete=models.CASCADE, default=-1)
    item_name = models.CharField(max_length=100)                       # 상품명
    total_amount = models.IntegerField()                               # 금액
    
    # 응답에서 받아올 값
    aid = models.CharField(max_length=20, default='')                  # 요청 고유 번호
    tid = models.CharField(max_length=20, unique=True, default='')     # 결제 고유 번호
    payment_method_type = models.CharField(max_length=10, default='')  # 결제 수단
    card_info = models.TextField(null=True, blank=True, default='')    # 결제 상세 정보
    amount_info = models.TextField(null=True, blank=True, default='')  # 금액 상세 
    created_at = models.CharField(max_length=20, default='')           # 결제 준비 요청 시각
    approved_at = models.CharField(max_length=20, default='')          # 결제 승인 시각

    class Meta: 
        db_table = 'payments'