from django.db import models
# from resume.models import Resume

class SeniorUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    id = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=40, null=True, blank=True)
    # default_resume = models.ForeignKey(Resume, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta: # 테이블 이름 지정
        db_table = 'senior_users'
        
    
class EnterpriseUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    id = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=40, null=True, blank=True) # blank: 모델 폼에서 비워둘 수 있는지 여부
    business_number = models.CharField(max_length=20)

    class Meta: # 테이블 이름 지정
        db_table = 'enterprise_users'


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    reviewer = models.ForeignKey(EnterpriseUser, on_delete=models.PROTECT)
    senior = models.ForeignKey(SeniorUser, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        db_table = 'reviews'