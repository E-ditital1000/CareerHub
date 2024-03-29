# Generated by Django 4.0.8 on 2024-02-01 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_remove_joblisting_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='joblisting',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='experience',
            field=models.CharField(max_length=100),
        ),
    ]
