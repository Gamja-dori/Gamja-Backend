from django.db import models
from users.models import EnterpriseUser
# from resume.models import Resume

class RecommendResult(models.Model):
    recommend_id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=255)
    user = models.ForeignKey(EnterpriseUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recommend_results'


class RecommendedResume(models.Model):
    recommended_resume_id = models.AutoField(primary_key=True)
    percentage = models.IntegerField()
    comment = models.CharField(max_length=255, null=True)
    recommend_result = models.ForeignKey(RecommendResult, on_delete=models.CASCADE)
    # resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'recommended_resumes'