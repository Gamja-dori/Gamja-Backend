from django.urls import path
from .views import CreateResumeAPIView, DeleteResumeAPIView, ChangeResumeTitleAPIView, SetDefaultResumeAPIView, SubmitResumeAPIView, EditResumeAPIView, GetResumeAPIView, GetResumeListAPIView

urlpatterns = [
    path('create/', CreateResumeAPIView.as_view()),
    path('delete/<int:user_id>/<int:resume_id>/', DeleteResumeAPIView.as_view()),
    path('new-title/', ChangeResumeTitleAPIView.as_view()),
    path('submit/', SubmitResumeAPIView.as_view()),
    path('set-default/', SetDefaultResumeAPIView.as_view()),
    path('edit/<int:user_id>/<int:resume_id>/', EditResumeAPIView.as_view()),
    path('detail/<int:user_id>/<int:resume_id>/', GetResumeAPIView.as_view()),
    path('list/<int:user_id>/', GetResumeListAPIView.as_view()),
]

"""
    path('prior-resume/<int:user_id>/<int:resume_id>/')
"""

