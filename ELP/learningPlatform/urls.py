from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming this is the home page of your platform
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('courses/<int:course_pk>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='learningPlatform/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path("logout/", views.logout_view, name="logout"),

]




