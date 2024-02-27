from django.db import models
from resume.models import Resume

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    
class SeniorUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='seniorUser')
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=40, null=True, blank=True)
    default_resume = models.ForeignKey(Resume, null=True, blank=True, on_delete=models.SET_NULL)
    profile_image = models.ImageField(upload_to='uploads/profile/senior', null=True, blank=True)

    class Meta: # 테이블 이름 지정
        db_table = 'senior_users'
        
    
class EnterpriseUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='enterpriseUser')
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=40, null=True, blank=True) # blank: 모델 폼에서 비워둘 수 있는지 여부
    business_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='uploads/profile/enterprise', null=True, blank=True)
    
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

# https://medium.com/geekculture/how-to-implement-multiple-user-types-in-django-b72df7a98dc3
