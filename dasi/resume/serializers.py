from rest_framework import serializers
from .models import *
from users.models import SeniorUser

class CreateResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user']
        
    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        user = SeniorUser.objects.filter(user_id=user_id)[0]
        resume = Resume.objects.create(user=user)
        resume_num = len(Resume.objects.filter(user=user))
        resume.title = "이력서 " + str(resume_num)
        if len(Resume.objects.filter(user=user)) == 1:
            resume.is_default = True
        resume.save()
        return resume
        
class ChangeResumeTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'id', 'title']

class FindResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['user', 'id']

# 이력서 전체 관련 Serializer
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id', 'start_year_month', 'end_year_month', 'performance_name', 'performance_detail']

class CareerSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(many=True)
    class Meta:
        model = Career
        fields = ['id', 'start_year_month', 'end_year_month', 'company_name', 'job_name', 'performances']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'start_year_month', 'end_year_month', 'education_name', 'education_info']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'start_year_month', 'end_year_month', 'project_name', 'project_detail']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'portfolio_name'] #'portfolio_file'
    
class ResumeSerializer(serializers.ModelSerializer):
    careers = CareerSerializer(many=True)
    educations = EducationSerializer(many=True)
    projects = ProjectSerializer(many=True)
    portfolios = PortfolioSerializer(many=True)
    class Meta:
        model = Resume
        fields = ['is_submitted', 'keyword', 'introduction', 'job_group', 'job_role', 'career_year', 'skills', 'careers', 'educations', 'projects', 'portfolios', 'duration_start', 'duration_end', 'min_month_pay', 'max_month_pay', 'commute_type']

    def update(self, resume, validated_data):
        resume.keyword = validated_data.pop('keyword')
        resume.introduction = validated_data.pop('introduction')
        resume.job_group = validated_data.pop('job_group')
        resume.job_role = validated_data.pop('job_role')
        resume.career_year = validated_data.pop('career_year')
        resume.skills = validated_data.pop('skills')
        resume.duration_start = validated_data.pop('duration_start')
        resume.duration_end = validated_data.pop('duration_end')
        resume.min_month_pay = validated_data.pop('min_month_pay')
        resume.max_month_pay = validated_data.pop('max_month_pay')
        resume.commute_type = validated_data.pop('commute_type')

        careers = validated_data.pop('careers')
        educations = validated_data.get('educations')
        projects = validated_data.pop('projects')
        portfolios = validated_data.pop('portfolios')

        for career in careers:
            Career.objects.update_or_create(id=career['id'], defaults={
                'start_year_month': career['start_year_month'], 
                'end_year_month': career['end_year_month'], 
                'company_name': career['company_name'],
                'job_name': career['job_name'],
                'resume': resume
            })
            performances = career['performances']
            _career = Career.objects.get(id=career['id'])
            for performance in performances:
               Performance.objects.update_or_create(id=performance['id'], defaults={
               'start_year_month': performance['start_year_month'], 
                'end_year_month': performance['end_year_month'], 
                'performance_name': performance['performance_name'],
                'performance_detail': performance['performance_detail'],
                'career': _career
           })
        
        for education in educations:
            Education.objects.update_or_create(id=education['id'], defaults={
                'start_year_month': education['start_year_month'], 
                'end_year_month': education['end_year_month'], 
                'education_name': education['education_name'],
                'education_info': education['education_info'],
                'resume': resume
            })

        for project in projects:
            Project.objects.update_or_create(id=project['id'], defaults={
                'start_year_month': project['start_year_month'], 
                'end_year_month': project['end_year_month'], 
                'project_name': project['project_name'],
                'project_detail': project['project_detail'],
                'resume': resume
            })

        for portfolio in portfolios:
            Portfolio.objects.update_or_create(id=portfolio['id'], defaults={
                'portfolio_name': portfolio['portfolio_name'],
                #'portfolio_file': portfolio['portfolio_file'],
                'resume': resume
            })
        
        return resume