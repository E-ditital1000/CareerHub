from django import forms
from .models import *


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['Email'].widget.attrs['placeholder'] = 'Enter a valid E-mail'

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'Email',
            'subject',
            'message'
        ]

class JobListingForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter job description here'}),
        label='Job Description'
    )

    responsibilities = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter responsibilities here'}),
        label='Job Responsibilities'
    )

    experience = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter required experience here'}),
        label='Experience'
    )

    def __init__(self, *args, **kwargs):
        super(JobListingForm, self).__init__(*args, **kwargs)
        self.fields['job_location'].widget.attrs['placeholder'] = 'Monrovia, Liberia'
        self.fields['Salary'].widget.attrs['placeholder'] = '60k-80k LRD, 4k-5k USD, Negotiable'
        self.fields['title'].widget.attrs['placeholder'] = 'Software Engineer, Web Designer'
        self.fields['application_deadline'].widget.attrs['placeholder'] = '2022-12-27'

        # Hide the 'status' field for regular users
        if not kwargs.get('instance') or not kwargs['instance'].user.is_superuser:
            self.fields['status'].widget = forms.HiddenInput()
        else:
            # Set the default value to 'draft' for regular users
            self.fields['status'].initial = 'draft'

    class Meta:
        model = JobListing
        exclude = ('user',)
        labels = {
            "job_location": "Job Location",
            "published_on": "Publish Date",
            "status": "Job Status",  # Include the label for 'status' field
        }





class JobApplyForm(forms.ModelForm):
    class Meta:
        model = ApplyJob
        fields = ['job_listing', 'name', 'email', 'file', 'resume', 'linkedin', 'skills', 'previous_jobs', 'portfolio']
        labels = {
            'file': 'CV (pdf format)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'file': forms.FileInput(attrs={'placeholder': 'Upload Your CV (pdf format)'}),
            'resume': forms.Textarea(attrs={'placeholder': 'Your Resume'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'Your LinkedIn URL'}),
            'skills': forms.TextInput(attrs={'placeholder': 'Your Skills'}),
            'previous_jobs': forms.TextInput(attrs={'placeholder': 'Your Previous Jobs'}),
            'portfolio': forms.URLInput(attrs={'placeholder': 'Your Portfolio URL'}),
        }
        # Set required fields
        required_fields = ['name', 'email', 'file', 'resume']
        
    def __init__(self, *args, **kwargs):
        super(JobApplyForm, self).__init__(*args, **kwargs)
        for field in self.Meta.required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super(JobApplyForm, self).clean()
        # Exclude URL fields from being required
        for field in self.Meta.required_fields:
            if field in cleaned_data and field in ['linkedin', 'portfolio']:
                self.fields[field].required = False
        return cleaned_data