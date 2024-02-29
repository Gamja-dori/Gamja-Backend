from django.db import models
from resume.models import Resume
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, username, name, password, phone_number, email=None):
        if not username:
            raise ValueError('must have username')
        if not name:
            raise ValueError('must have user name')
        if not password:
            raise ValueError('must have password')
        if not phone_number:
            raise ValueError('must have phone number')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            name = name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, nickname, name, password=None):
        user = self.create_user(
            email,
            password = password,
            nickname = nickname,
            name = name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(null=True, blank=True)
    is_senior = models.BooleanField(default=False)
    is_enterprise = models.BooleanField(default=False)
    
    objects = UserManager()
    
    class Meta: # 테이블 이름 지정
        db_table = 'users'

    
class SeniorUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='senior_users')
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    default_resume = models.ForeignKey(Resume, null=True, blank=True, on_delete=models.SET_NULL)
    profile_image = models.ImageField(upload_to='uploads/profile/senior', null=True, blank=True)

    class Meta: # 테이블 이름 지정
        db_table = 'senior_users'
        
    
class EnterpriseUser(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='enterprise_users')
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    business_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='uploads/profile/enterprise', null=True, blank=True)
    is_certified = models.BooleanField(default=False) # 사업자번호 인증 여부
    
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


