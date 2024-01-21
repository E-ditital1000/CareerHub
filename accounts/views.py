# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import EmployeeRegistrationForm, EmployerRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Employee
from .forms import EmployeeProfileForm
from jobs.models import JobListing  # Update this import statement
from jobs.models import UserProfile 
from jobs.models import ApplyJob
from jobs.models import User# Update this import statement
from django.shortcuts import render
from jobs.models import JobListing, ApplyJob
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import EmployeeRegistrationForm  # Import your EmployeeRegistrationForm


@login_required
def employee_dashboard(request):
    try:
        # Try to get the associated Employee object for the logged-in user
        employee = request.user.employee
    except Employee.DoesNotExist:
        # If the Employee object doesn't exist, redirect to the registration page
        return redirect('accounts:employee_registration')

    # Your existing employee_dashboard view logic goes here
    context = {'employee': employee}
    return render(request, 'accounts/employee_dashboard.html', context)

def employee_registration(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_employee = True  # This line can be omitted with the default value set in the model
            user.save()
            
            # Create an Employee object for the user
            Employee.objects.create(user=user)

            # Send confirmation email
            subject = 'Employee Registration Confirmation'
            message = (
                f'Thank you, {user.first_name} {user.last_name}, for registering as an employee on JOBNET360.\n\n'
                f'We appreciate your commitment to being part of our community. '
                f'Please find below some important information:\n\n'
                f'Login:jobnet360.com\n'
                f'Email: {user.email}\n\n'
                f'You can now log in to your account and explore our platform. If you have any '
                f'questions or need assistance, feel free to contact us at edigitalnetwork842@gmail.com.\n\n'
                f'We look forward to your contributions and success on JOBNET360!\n\n'
                f'Best regards,\n'
                f'The Abraham Bedell \n CEO @ JOBNET360'
            )
            from_email = 'joannabedella@gmail.com'  # Change to your email address
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            login(request, user)
            return redirect('accounts:employee_dashboard')  # Redirect to the employee dashboard
    else:
        form = EmployeeRegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/employee_registration.html', context)



def employer_registration(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send confirmation email with user's name
            subject = 'Welcome to Career Hub - Employer Registration Confirmation'
            message = (
    f'Thank you, {user.first_name} {user.last_name}, for registering as an employer on JOBNET360.\n\n'
    f'We appreciate your commitment to being part of our community. '
    f'Please find below some important information:\n\n'
    f'Login: jobnet360.com\n'
    f'Email: {user.email}\n\n'
    f'You can now log in to your account and explore our platform. If you have any '
    f'questions or need assistance, feel free to contact us at edigitalnetwork842@gmail.com.\n\n'
    f'We look forward to your contributions and success on JOBNET360!\n\n'
    f'Best regards,\n'
    f'The Abraham Bedell \n CEO @ JOBNET360'
)

            from_email = 'joannabedella@gmail.com'  # Change to your email address
            to_email = [user.email]
            send_mail(subject, message, from_email, to_email, fail_silently=False)

            login(request, user)
            return redirect('jobs:dashboard')  # Redirect to the employer dashboard
    else:
        form = EmployerRegistrationForm()

    context = {'form': form}
    return render(request, "accounts/employer_registration.html", context)

@login_required
def edit_employee(request):
    employee = request.user.employee  # Assuming user has a related employee instance

    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('accounts:employee_dashboard')  # Correct URL or view name
    else:
        form = EmployeeProfileForm(instance=employee)

    context = {'form': form}
    return render(request, 'accounts/employee_dashboard.html', context)

@login_required
def edit_employee_popup(request):
    # Add logic to fetch the employee instance
    employee = request.user.employee  # Assuming user has a related employee instance

    # Assuming you have a form for editing employee information
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('accounts:employee_dashboard')  # Correct URL or view name
    else:
        form = EmployeeProfileForm(instance=employee)

    context = {'form': form}
    return render(request, 'accounts/edit_employee_popup.html', context)


  
def employer_dashboard(request):
    return render(request, "accounts/employer_dashboard.html")

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                is_employee = getattr(user, 'is_employee', False)

                if is_employee:
                    # Handle employee login
                    login(request, user)
                    return redirect('accounts:employee_dashboard')
                else:
                    # Handle other user login (employer, superuser, etc.)
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials. Please try again.')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, "accounts/user_login.html", context)



def logout_view(request):
    logout(request)
    return redirect('accounts:user_login')

@login_required
def employer_dashboard(request):
    # Retrieve statistics and other data needed for the dashboard
    total_applied_jobs = ApplyJob.objects.count()
    total_users = User.objects.count()
    total_jobs = JobListing.objects.count()

    # Retrieve unique companies with jobs
    companies_with_jobs = JobListing.objects.values('company_name').distinct().count()

    # Retrieve employee information for the employee list
    employee_list = Employee.objects.all()  # Update this query based on your model

    context = {
        'total_applied_jobs': total_applied_jobs,
        'total_users': total_users,
        'total_jobs': total_jobs,
        'companies_with_jobs': companies_with_jobs,
        'employee_list': employee_list,
    }

    # Use the correct app name in the render function
    return render(request, 'jobs/dashboard.html', context)