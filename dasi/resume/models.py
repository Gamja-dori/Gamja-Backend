from django.db import models

class Resume(models.Model):
    user = models.ForeignKey('users.SeniorUser', on_delete=models.CASCADE, default=-1)
    title = models.CharField(max_length=100, default='')
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    keyword = models.TextField(null=True, blank=True, default='')
    introduction = models.TextField(null=True, blank=True, default='')
    job_group = models.CharField(max_length=100, default='직군')
    job_role = models.CharField(max_length=100, default='직무')
    career_year = models.IntegerField(default=1)
    skills = models.TextField(null=True, blank=True, default='[]')
    duration_start = models.IntegerField(default=0)
    duration_end = models.IntegerField(default=12)
    min_month_pay = models.IntegerField(default=0)
    max_month_pay = models.IntegerField(default=1000)
    commute_type = models.CharField(max_length=20, default='희망 근무 형태')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)

    class Meta:
        db_table = 'resumes'

class Career(models.Model):
    resume = models.ForeignKey(Resume, related_name='careers', on_delete=models.CASCADE)
    start_year_month = models.CharField(blank=True, max_length=7)
    end_year_month = models.CharField(blank=True, max_length=7)
    company_name = models.CharField(blank=True, max_length=100)
    job_name = models.CharField(blank=True, max_length=100)

    class Meta:
        db_table = 'careers'

class Performance(models.Model):
    career = models.ForeignKey(Career, related_name='performances', on_delete=models.CASCADE)
    start_year_month = models.CharField(blank=True, max_length=7)
    end_year_month = models.CharField(blank=True, max_length=7)
    performance_name = models.CharField(blank=True, max_length=100)
    performance_detail = models.TextField(blank=True)

    class Meta:
        db_table = 'performances'

class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='educations', on_delete=models.CASCADE)
    start_year_month = models.CharField(blank=True, max_length=7)
    end_year_month = models.CharField(blank=True, max_length=7)
    education_name = models.CharField(blank=True, max_length=100)
    education_info = models.CharField(blank=True, max_length=100)

    class Meta:
        db_table = 'educations'

class Project(models.Model):
    resume = models.ForeignKey(Resume, related_name='projects', on_delete=models.CASCADE)
    start_year_month = models.CharField(blank=True, max_length=7)
    end_year_month = models.CharField(blank=True, max_length=7)
    project_name = models.CharField(blank=True, max_length=100)
    project_detail = models.TextField(blank=True)

    class Meta:
        db_table = 'projects'

class PriorResume(models.Model):
    resume = models.ForeignKey(Resume, related_name='prior_resumes', on_delete=models.CASCADE)
    prior_resume_name = models.CharField(blank=True, max_length=100)
    prior_resume_file = models.FileField(upload_to='uploads/resume')

    class Meta:
        db_table = 'prior_resumes'

class Portfolio(models.Model):
    resume = models.ForeignKey(Resume, related_name='portfolios', on_delete=models.CASCADE)
    portfolio_name = models.CharField(blank=True, max_length=100)
    portfolio_file = models.FileField(upload_to='uploads/portfolio')
    
    class Meta:
        db_table = 'portfolios'