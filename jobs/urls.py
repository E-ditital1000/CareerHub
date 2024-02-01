from django.urls import path
from .views import *

app_name = 'jobs'

urlpatterns = [
    path('contact/', contact, name='contact'),
    path('about/', about_us, name='about'),
    path('service/', service, name='service'),
    path('job-post/', job_post, name='job-post'),
    path('job-listing/', job_listing, name='job-listing'),
    path('job-single/<int:id>/', job_single, name='job-single'),
    path('search/', SearchView.as_view(), name='search'),
    path('apply/<int:job_listing_id>/', job_apply, name='apply'),
    path('dashboard/', dashboard, name='dashboard'),
    path('thank-you/', thank_you_page, name='thank_you'),
    path('drafted_jobs/', drafted_jobs, name='drafted_jobs'),
    path('job-draft/<int:id>/', job_draft, name='job-draft'),  # New URL pattern for job draft
]

handler404 = 'jobs.views.error_404_view'
handler500 = 'jobs.views.error_500_view'
