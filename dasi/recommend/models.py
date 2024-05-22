from django.db import models
from users.models import EnterpriseUser
from resume.models import Resume

class SearchHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)
    query = models.CharField(max_length=255, default='')
    job_group = models.CharField(max_length=20, blank=True, default='')
    job_role = models.CharField(max_length=20, blank=True, default='')
    min_career_year = models.IntegerField(default=0)
    max_career_year = models.IntegerField(default=0)
    skills = models.TextField(null=True, blank=True, default='[]')
    duration_start = models.IntegerField(default=0)
    duration_end = models.IntegerField(default=12)
    min_month_pay = models.IntegerField(default=0)
    max_month_pay = models.IntegerField(default=1000)
    commute_type = models.CharField(max_length=20, blank=True, default='')
        
    class Meta:
        db_table = 'search_historys'