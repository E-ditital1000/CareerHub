from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone

# Create your models here.


def validate_bio_word_count(value):
    max_word_count = 200  # Set your desired word limit
    words = value.split()
    if len(words) > max_word_count:
        raise ValidationError(f'The bio should not exceed {max_word_count} words.')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    bio = models.TextField(blank=True, validators=[validate_bio_word_count])
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return self.user.username



class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.first_name

class JobType(models.Model):
    JOB_TYPES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Freelancer', 'Freelancer'),
        # Add more job types as needed
    ]

    type = models.CharField(max_length=50, choices=JOB_TYPES)

    def __str__(self):
        return self.type


class Category(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField(default=False)  # Adding a description field
    is_active = models.BooleanField(default=True)  # Adding a field to mark category as active or inactive
    # Add other fields as needed

    def __str__(self):
        return self.category


class Gender(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        # Add more genders as needed
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.gender



class JobListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             null=True, editable=False, blank=True)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    employment_status = models.ForeignKey(JobType, on_delete=models.CASCADE)
    vacancy = models.CharField(max_length=10, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company_details = models.TextField(blank=True, null=True)
    company_email = models.EmailField(null=True, blank=True, default='yourmail@gmail.com')
    description = models.TextField()
    responsibilities = models.TextField()
    experience = models.CharField(max_length=1000)
    job_location = models.CharField(max_length=120)
    Salary = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='media', null=True)
    application_deadline = models.DateTimeField()
    published_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("jobs:job-single", args=[self.id])

    
class ApplyJob(models.Model):
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    file = models.FileField(upload_to='documents/', null=True)
    resume = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    skills = models.TextField(blank=True)
    previous_jobs = models.TextField(blank=True)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return self.name
