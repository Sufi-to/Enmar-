from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Course, Lesson, Enrollment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login as auth_login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, CourseForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'learningPlatform/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'learningPlatform/logout.html', {'user': request.user})

# def custom_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             if user.is_instructor:
#                 return redirect('instructor_dashboard')
#             else:
#                 return redirect('course_list')
#     return render(request, 'learningPlatform/login.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')

                # Redirect based on user role
                if user.is_instructor:
                    return redirect('instructor_dashboard')
                elif user.is_learner:
                    return redirect('course_list')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'learningPlatform/login.html', {'form': form})


@login_required
def course_list(request):
    if request.user.is_learner:
        courses = Course.objects.all()
        enrollments = Enrollment.objects.filter(learner=request.user).values_list('course_id', flat=True)
        return render(request, 'learningPlatform/course_list.html', {'courses': courses, 'enrollments': enrollments})
    else:
        return redirect('home')
    

@login_required
def instructor_dashboard(request):
    if request.user.is_instructor:
        courses = Course.objects.filter(instructor=request.user)
        return render(request, 'learningPlatform/instructor_dashboard.html', {'courses': courses})
    else:
        return redirect('course_list')  # Redirect learners to course list


@login_required
def course_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id, instructor=request.user)
    enrollments = Enrollment.objects.filter(course=course)
    return render(request, 'learningPlatform/course_students.html', {'course': course, 'enrollments': enrollments})


# @login_required
# def add_course(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         Course.objects.create(title=title, description=description, instructor=request.user)
#         return redirect('instructor_dashboard')
#     return render(request, 'learningPlatform/add_course.html')


@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor_dashboard')
        else:
            print(form.errors)  # Print form errors to the console
            messages.error(request, 'Error creating course. Please check the form and try again.')
    else:
        form = CourseForm()
    return render(request, 'learningPlatform/add_course.html', {'form': form})

# def add_course(request):
#     instructor = request.user  # Assuming user is authenticated
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             # Process form data
#             form.save()
#             # Redirect or return a success response
#     else:
#         form = CourseForm()

#     context = {
#         'form': form,
#         'instructor': instructor,
#     }
#     return render(request, 'learningPlatform/add_course.html', context)


@login_required
def add_lesson(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        title = request.POST.get('title')
        video_url = request.POST.get('video_url')

        course = Course.objects.get(pk=course_id)
        Lesson.objects.create(course=course, title=title, video_url=video_url)
        messages.success(request, 'Lesson added successfully!')
        return redirect('instructor_dashboard')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'learningPlatform/add_lesson.html', {'courses': courses})