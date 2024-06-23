# Generated by Django 5.0.6 on 2024-06-22 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('employee', 'Employee'), ('client', 'Client'), ('admin', 'Admin')], default='user', max_length=20),
        ),
    ]
