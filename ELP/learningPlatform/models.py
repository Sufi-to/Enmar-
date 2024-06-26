from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.core.exceptions import ValidationError


class User(AbstractUser):
    is_learner = models.BooleanField(default=False, verbose_name="Learner Status")
    is_instructor = models.BooleanField(default=False, verbose_name="Instructor Status")
    is_admin = models.BooleanField(default=False, verbose_name="Admin Status")
    bio = models.TextField(blank=True, null=True, verbose_name="Biography")

    def __str__(self):
        return self.username
    
 
 
  
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300 )
            img.thumbnail(output_size)
            img.save(self.image.path)



class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_courses', verbose_name="Instructor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Update Date")
    
    def __str__(self):
        return f'{self.title} by {self.instructor.username}'
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Course")
    title = models.CharField(max_length=200, verbose_name="Lesson Title")
    content = models.TextField(verbose_name="Lesson Content")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Update Date")
    
    def __str__(self):
        return f'{self.title} in {self.course.title}'
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

class Enrollment(models.Model):
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Learner")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Enrollment Date")
    
    class Meta:
        unique_together = ('learner', 'course')
        ordering = ['enrolled_at']
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        
    def __str__(self):
        return f'{self.learner.username} enrolled in {self.course.title}'
    

