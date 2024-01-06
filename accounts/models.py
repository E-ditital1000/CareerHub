from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=True)
    skills = models.TextField(blank=True)
    schedule = models.CharField(max_length=255, blank=True)
    can_volunteer = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    job_preferences = models.CharField(max_length=255, blank=True)
    is_part_time = models.BooleanField(default=False)
    is_full_time = models.BooleanField(default=False)
    is_contract = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    def get_latest_information(self):
        # Return the latest information for the employee
        return {
            'skills': self.skills,
            'schedule': self.schedule,
            'can_volunteer': self.can_volunteer,
            'contact_number': self.contact_number,
            'address': self.address,
            'job_preferences': self.job_preferences,
            'is_part_time': self.is_part_time,
            'is_full_time': self.is_full_time,
            'is_contract': self.is_contract,
        }

class EmployeeUpdates(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now_add=True)
    update_fields = models.TextField()  # Store updated fields and values as JSON

class TimeClock(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    punch_in = models.DateTimeField(blank=True, null=True)
    punch_out = models.DateTimeField(blank=True, null=True)

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()

class RecentAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    recent_attendance_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

class LeaveHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    reason = models.TextField()
