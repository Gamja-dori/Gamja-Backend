from django.db import models
from users.models import SeniorUser

class Resume(models.Model):
    resume_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(SeniorUser, on_delete=models.CASCADE)
    resume_name = models.CharField(max_length=20)
    is_default = models.BooleanField()
    introduction = models.TextField(null=True, blank=True)
    job_group = models.CharField(max_length=20)
    job_role = models.CharField(max_length=20)
    career = models.IntegerField()
    skills = models.TextField(null=True, blank=True)
    work_type = models.TextField()
    minimum_pay = models.IntegerField()
    maximum_pay = models.IntegerField()
    commute_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view = models.IntegerField()

    class Meta:
        db_table = 'resumes'

class Career(models.Model):
    career_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    company_name = models.CharField(max_length=40)
    job_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'careers'

class Performance(models.Model):
    performance_id = models.AutoField(primary_key=True)
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    performance_name = models.CharField(max_length=40)
    performance_detail = models.TextField()

    class Meta:
        db_table = 'performances'

class Education(models.Model):
    education_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    education_name = models.CharField(max_length=40)
    education_info = models.CharField(max_length=40)

    class Meta:
        db_table = 'educations'

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    project_name = models.CharField(max_length=40)
    project_detail = models.TextField()

    class Meta:
        db_table = 'projects'

class PriorResume(models.Model):
    prior_resume_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    prior_resume_name = models.CharField(max_length=40)
    prior_resume_file = models.FileField(upload_to='uploads/resume')

    class Meta:
        db_table = 'prior_resumes'

class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=40)
    portfolio_file = models.FileField(upload_to='uploads/portfolio')
    
    class Meta:
        db_table = 'portfolios'