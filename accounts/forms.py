from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter a valid e-mail'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter a username'

class EmployeeRegistrationForm(UserRegistrationForm):
    username = forms.CharField(max_length=10)

    class Meta(UserRegistrationForm.Meta):
        fields = UserRegistrationForm.Meta.fields + ['username']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employee = True  # Set the is_employee attribute
        if commit:
            user.save()
        return user

class EmployeeRegistrationForm(UserRegistrationForm):
    username = forms.CharField(max_length=10)

    class Meta(UserRegistrationForm.Meta):
        fields = UserRegistrationForm.Meta.fields + ['username']

class EmployerRegistrationForm(UserRegistrationForm):
    company_name = forms.CharField(max_length=100)

    class Meta(UserRegistrationForm.Meta):
        fields = UserRegistrationForm.Meta.fields + ['company_name']

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['skills', 'schedule', 'can_volunteer', 'contact_number', 'address', 'job_preferences', 'is_part_time', 'is_full_time', 'is_contract']
