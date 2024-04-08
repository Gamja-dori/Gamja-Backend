from django.db import models
from users.models import EnterpriseUser
from resume.models import Resume

class SearchResult(models.Model):
    query = models.CharField(max_length=255)
    user = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)
    job_group = models.CharField(max_length=20, default='')
    job_role = models.CharField(max_length=20, default='')
    min_career_year = models.IntegerField(default=0)
    max_career_year = models.IntegerField(default=0)
    skills = models.TextField(null=True, blank=True, default='[]')
    min_month_pay = models.IntegerField(default=0)
    max_month_pay = models.IntegerField(default=1000)
    commute_type = models.CharField(max_length=20, default='')
   
    class Meta:
        db_table = 'search_results'


class RecommendedResume(models.Model):
    recommend_result = models.ForeignKey(SearchResult, on_delete=models.CASCADE)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE, default=-1)
    percentage = models.IntegerField()
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'recommended_resumes'