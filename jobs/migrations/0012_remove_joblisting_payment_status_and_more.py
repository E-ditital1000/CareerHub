# Generated by Django 4.0.8 on 2024-01-25 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_joblisting_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joblisting',
            name='payment_status',
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='experience',
            field=models.CharField(max_length=1000),
        ),
    ]
