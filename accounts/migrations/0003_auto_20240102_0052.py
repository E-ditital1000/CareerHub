# Generated by Django 3.1.14 on 2024-01-02 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_employee_is_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_employee',
            field=models.BooleanField(default=True),
        ),
    ]
