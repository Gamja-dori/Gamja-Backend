from django.db import models
from resume.models import Resume
from django.contrib.auth.models import AbstractUser, BaseUserManager
    
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    is_senior = models.BooleanField(default=False)
    is_enterprise = models.BooleanField(default=False)
    
    class Meta: # 테이블 이름 지정
        db_table = 'users'

    
class SeniorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='senior_users')
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    default_resume = models.ForeignKey(Resume, null=True, blank=True, on_delete=models.SET_NULL)
    profile_image = models.ImageField(upload_to='uploads/profile/senior', null=True, blank=True)

    class Meta: # 테이블 이름 지정
        db_table = 'senior_users'
        
    
class EnterpriseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='enterprise_users')
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    business_number = models.CharField(max_length=20)
    is_certified = models.BooleanField(default=False) # 사업자번호 인증 여부
    profile_image = models.ImageField(upload_to='uploads/profile/enterprise', null=True, blank=True)

    class Meta: # 테이블 이름 지정
        db_table = 'enterprise_users'


class Review(models.Model):
    reviewer = models.ForeignKey(EnterpriseUser, on_delete=models.PROTECT)
    senior = models.ForeignKey(SeniorUser, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    class Meta:
        db_table = 'reviews'