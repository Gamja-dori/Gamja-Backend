from django.db import models

class Resume(models.Model):
    user_id = models.ForeignKey('users.SeniorUser', on_delete=models.CASCADE, default=-1)
    resume_name = models.CharField(max_length=20, default='')
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    introduction = models.TextField(null=True, blank=True, default='')
    job_group = models.CharField(max_length=20, default='')
    job_role = models.CharField(max_length=20, default='')
    career_length = models.IntegerField(default=0)
    skills = models.TextField(null=True, blank=True, default='[]')
    work_type = models.TextField(default='')
    min_hour_pay = models.IntegerField(default=0)
    max_hour_pay = models.IntegerField(default=50)
    min_month_pay = models.IntegerField(default=0)
    max_month_pay = models.IntegerField(default=1000)
    commute_type = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)

    class Meta:
        db_table = 'resumes'

class Career(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    company_name = models.CharField(max_length=40)
    job_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'careers'

class Performance(models.Model):
    career_id = models.ForeignKey(Career, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    performance_name = models.CharField(max_length=40)
    performance_detail = models.TextField()

    class Meta:
        db_table = 'performances'

class Education(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    education_name = models.CharField(max_length=40)
    education_info = models.CharField(max_length=40)

    class Meta:
        db_table = 'educations'

class Project(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    start_year_month = models.CharField(max_length=7)
    end_year_month = models.CharField(max_length=7)
    project_name = models.CharField(max_length=40)
    project_detail = models.TextField()

    class Meta:
        db_table = 'projects'

class PriorResume(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    prior_resume_name = models.CharField(max_length=40)
    prior_resume_file = models.FileField(upload_to='uploads/resume')

    class Meta:
        db_table = 'prior_resumes'

class Portfolio(models.Model):
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE)
    portfolio_name = models.CharField(max_length=40)
    portfolio_file = models.FileField(upload_to='uploads/portfolio')
    
    class Meta:
        db_table = 'portfolios'