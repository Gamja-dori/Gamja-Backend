from django.urls import path
from .views import CreateResumeAPIView, DeleteResumeAPIView

urlpatterns = [
    path('new/', CreateResumeAPIView.as_view()),
    path('delete/<int:user_id>/<int:resume_id>/', DeleteResumeAPIView.as_view()),
]

"""
    path('edit/<int:user_id>/<int:resume_id>/'),
    path('delete/<int:user_id>/<int:resume_id>/'),
    path('list/<int:user_id>/'),
    path('<int:user_id>/<int:resume_id>/'),
    path('prior-resume/<int:user_id>/<int:resume_id>/')
"""

