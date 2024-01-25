from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from .forms import *
from .models import *
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from .models import UserProfile
from accounts.models import Employee
import mimetypes
from email.message import EmailMessage
from django.core.mail import send_mail
from django.http import HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .forms import JobApplyForm
from .models import JobListing
from django.contrib import messages

from django.http import HttpResponseNotFound, HttpResponseServerError

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)


def job_apply(request, job_listing_id):
    job_listing = get_object_or_404(JobListing, id=job_listing_id)

    if request.method == 'POST':
        form = JobApplyForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.job_listing = job_listing # Link the application to the job listing
            instance.save()

            # Build the email message using EmailMessage
            subject = 'New Job Application'
            email_message = f'''A new job application has been submitted.
            
Applicant Name: {instance.name}
Applicant Email: {instance.email}
Applicant Skills: {instance.skills}
Applicant Previous Jobs: {instance.previous_jobs}
Applicant Portfolio URL: {instance.portfolio}
Resume: {instance.resume}
Linkedin: {instance.linkedin}
            '''

            try:
                # Send the email using send_mail
                send_mail(
                    subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [job_listing.company_email], # Send to the company's email
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error or handle it appropriately
                return HttpResponseServerError(f"Error sending email: {str(e)}")
            
            # Provide feedback to the user
            return render(request, 'thank_you.html')

    else:
        form = JobApplyForm()

    return render(request, 'jobs/job_apply.html', {'form': form})


def home(request):
    qs = JobListing.objects.all()
    jobs = JobListing.objects.all().count()
    user = User.objects.all().count()
    company_name = JobListing.objects.filter(company_name__startswith='P').count()
    paginator = Paginator(qs, 5)  # Show 5 jobs per page
    page = request.GET.get('page')
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        'query': qs,
        'job_qs': jobs,
        'company_name': company_name,
        'candidates': user
    }
    return render(request, "home.html", context)


def about_us(request):
    return render(request, "jobs/about_us.html", {})


def service(request):
    return render(request, "jobs/services.html", {})


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        instance.save()
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, "jobs/contact.html", context)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def job_listing(request):
    # Get all job listings ordered by published_on
    all_job_listings = JobListing.objects.all().order_by('-published_on')

    # Paginate the queryset
    paginator = Paginator(all_job_listings, 3)  # Show 3 jobs per page
    page = request.GET.get('page')

    try:
        job_listings = paginator.page(page)
    except PageNotAnInteger:
        job_listings = paginator.page(1)
    except EmptyPage:
        job_listings = paginator.page(paginator.num_pages)

    context = {
        'query': job_listings,  # Use the same variable name for the paginated queryset
        'job_count': paginator.count,  # Use paginator.count to get the total count
    }

    return render(request, "jobs/job_listing.html", context)

# views.py in your jobs app

#from mtn_payment_app.mtn_integration import MTNIntegration  # Import MTNIntegration from your payment app




# views.py
@login_required
def job_post(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST, request.FILES)

        # Check if an image is provided in the form
        if 'image' not in request.FILES:
            form.add_error('image', 'Please upload an image.')

        if form.is_valid():
            job_listing = form.save(commit=False)
            job_listing.user = request.user
            job_listing.save()
            return redirect('jobs:job-single', id=job_listing.id)

    else:
        form = JobListingForm()

    context = {'form': form}
    return render(request, "jobs/job_post.html", context)



@login_required
def job_single(request, id):
    job_query = get_object_or_404(JobListing, id=id)

    context = {'q': job_query}
    return render(request, "jobs/job_single.html", context)

@login_required
def apply_job(request, job_listing_id):
    job_listing = get_object_or_404(JobListing, id=job_listing_id)

    if request.method == 'POST':
        form = JobApplyForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the job listing reference in the form before saving it
            job_application = form.save(commit=False)
            job_application.job_listing = job_listing
            job_application.save()
            return redirect('thank_you_page')
    else:
        form = JobApplyForm()

    context = {'form': form, 'job_listing': job_listing}
    return render(request, "jobs/job_apply.html", context)


def thank_you_page(request):
    return render(request, 'thank_you.html')

from django.shortcuts import get_object_or_404

@login_required
def dashboard(request):

    # Count the number of jobs posted by the user
    user_jobs = JobListing.objects.filter(user=request.user).count()

    # Get the list of companies that posted jobs
    companies_with_jobs = JobListing.objects.values_list('company_name', flat=True).distinct()

    # Get the total number of user profiles
    total_users = UserProfile.objects.count()
    
    context = {
        
        'user_jobs': user_jobs,
        'total_users': total_users,
        'companies_with_jobs': companies_with_jobs,
        
    }
    return render(request, 'jobs/dashboard.html', context)

class SearchView(ListView):
    model = JobListing
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title', '')
        job_location = self.request.GET.get('job_location', '')
        employment_status = self.request.GET.get('employment_status', '')

        if title or job_location or employment_status:
            queryset = queryset.filter(
                title__icontains=title,
                job_location__icontains=job_location,
                employment_status__type__icontains=employment_status
            )
        return queryset

def get_counts(request):
    # Logic to fetch counts from the database
    job_count = JobListing.objects.count()
    candidate_count = ApplyJob.objects.count()  # Assuming ApplyJob is used for candidates
    company_count = UserProfile.objects.count()  # Assuming UserProfile is used for companies

    # Return counts as JSON
    return JsonResponse({
        'job_count': job_count,
        'candidate_count': candidate_count,
        'company_count': company_count,
    })

def dashboard(request):
    total_jobs = JobListing.objects.count()
    total_applied_jobs = ApplyJob.objects.count()
    total_users = User.objects.count()

    context = {
        'total_jobs': total_jobs,
        'total_applied_jobs': total_applied_jobs,
        'total_users': total_users,
    }

    return render(request, 'jobs/dashboard.html', context)

def dashboard(request):
    # Retrieve the list of employees from the Employee model
    employee_list = Employee.objects.all()

    # Add any additional context you want to pass to the template
    context = {
        'employee_list': employee_list,
        # Add more context variables as needed
    }

    return render(request, 'jobs/dashboard.html', context)


def company_info(request):
    # Fetching the first job listing for each company
    companies_with_jobs = JobListing.objects.values_list('company_name', flat=True).distinct()
    company_info_list = []

    for company in companies_with_jobs:
        job_listing = JobListing.objects.filter(company_name=company).first()

        if job_listing:
            company_info_list.append({
                'company_name': company,
                'image_url': job_listing.image.url,
            })
        else:
            company_info_list.append({
                'company_name': company,
                'image_url': None,
            })

    context = {
        'company_info_list': company_info_list,
    }

    return render(request, 'jobs/dashboard.html', context)


from django.shortcuts import render
from django.contrib.auth.models import User
from .models import JobListing
from django.db.models import Count
from django.utils import timezone


def dashboard(request):
    # Count total users
    total_users = User.objects.count()

    # Count total jobs
    total_jobs = JobListing.objects.count()
    
    today = timezone.now().date()
    total_jobs_published_today = JobListing.objects.filter(published_on__date=today).count()

     # Retrieve unique companies with jobs
    companies_with_jobs = JobListing.objects.values('company_name').distinct().count()

    # Retrieve employee information for the employee list
    employee_list = Employee.objects.all()  # Update this query based on your model

    user = request.user  # Assuming the logged-in user
    total_jobs_applied_by_user = ApplyJob.objects.filter(email=user.email).count()



    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'today_jobs':total_jobs_published_today,
        'companies_with_jobs': companies_with_jobs,
        'employee_list': employee_list,
        'applied_by_user' : total_jobs_applied_by_user,
    }

    return render(request, 'jobs/dashboard.html', context)

