# Generated by Django 4.0.8 on 2024-01-06 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_auto_20231222_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='company_email',
            field=models.EmailField(blank=True, default='yourmail@gmail.com', max_length=254, null=True),
        ),
    ]
