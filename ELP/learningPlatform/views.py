from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Course, Lesson, Enrollment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    # Implement your home view logic here
    return render(request, 'learningPlatform/home.html')

class CourseListView(ListView):
    model = Course
    template_name = 'learningPlatform/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'learningPlatform/course_detail.html'
    context_object_name = 'course'


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'learningPlatform/lesson_detail.html'
    context_object_name = 'lesson'

@login_required
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user = request.user  # Assuming user is authenticated
    if Enrollment.objects.filter(learner=user, course=course).exists():
        # User is already enrolled
        return redirect('course_detail', pk=pk)
    else:
        Enrollment.objects.create(learner=user, course=course)
        return redirect('course_detail', pk=pk)


class LessonListView(LoginRequiredMixin, ListView):
    template_name = 'learningPlatform/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        self.course = get_object_or_404(Course, pk=self.kwargs['course_pk'])
        return Lesson.objects.filter(course=self.course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'learningPlatform/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        return Enrollment.objects.filter(learner=self.request.user)

class EnrollmentDetailView(LoginRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'learningPlatform/enrollment_detail.html'
    context_object_name = 'enrollment'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'learningPlatform/register.html', {'form': form})
