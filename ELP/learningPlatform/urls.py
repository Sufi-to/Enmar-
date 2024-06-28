from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Assuming this is the home page of your platform
    # path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_pk>/lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('courses/<int:course_pk>/lessons/', views.LessonListView.as_view(), name='lesson_list'),
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail'),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(template_name='learningPlatform/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path("logout/", views.logout_view, name="logout"),
    path('courses/', views.course_list, name='course_list'),
    path('login/', views.custom_login, name='login'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/course/<int:course_id>/students/', views.course_students, name='course_students'),
    path('instructor/add_course/', views.add_course, name='add_course'),
    path('add_lesson/', views.add_lesson, name='add_lesson'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/next/', views.next_lesson, name='next_lesson'),
]




