from django.db import models
from users.models import EnterpriseUser
from resume.models import Resume

class SearchResult(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=255)
    user = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'search_results'


class RecommendedResume(models.Model):
    recommend_result = models.ForeignKey(SearchResult, on_delete=models.CASCADE)
    resume_id = models.ForeignKey(Resume, on_delete=models.CASCADE, default=-1)
    percentage = models.IntegerField()
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'recommended_resumes'