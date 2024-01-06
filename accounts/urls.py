# urls.py
from django.urls import path
from .views import *
app_name = 'accounts'
from .views import employee_dashboard, employer_dashboard

urlpatterns = [
    path('employee_registration/', employee_registration, name='employee_registration'),
    path('employer_registration/', employer_registration, name='employer_registration'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('employer_dashboard/', employer_dashboard, name='employer_dashboard'),
    path('user_login/', user_login, name='user_login'),  # Add this line
    path('logout/', logout_view, name='logout'),
    path('edit_employee/', edit_employee, name='edit_employee'),
    path('edit_employee_popup/', edit_employee_popup, name='edit_employee_popup'),
    path('accounts/employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    path('jobs/dashboard/', employer_dashboard, name='employer_dashboard'),
    # Add other paths for your views as needed
]
