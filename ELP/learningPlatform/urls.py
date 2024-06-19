from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming this is the home page of your platform
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('courses/<int:course_pk>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('accounts/', include('django.contrib.auth.urls')),

]




