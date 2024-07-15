# Generated by Django 5.0.6 on 2024-07-15 00:53

import django.db.models.deletion
import projects_app.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Código')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('start_date', models.DateField(verbose_name='Fecha de Inicio')),
                ('end_date', models.DateField(verbose_name='Fecha de Finalización')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='pending', max_length=10, verbose_name='Estado')),
                ('assigned_to_client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_projects', to=settings.AUTH_USER_MODEL, verbose_name='Cliente Asignado')),
                ('assigned_to_employees', models.ManyToManyField(blank=True, related_name='assigned_employee_projects', to=settings.AUTH_USER_MODEL, verbose_name='Empleados Asignados')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('file', models.FileField(upload_to=projects_app.models.document_upload_path, verbose_name='File')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('uploaded', 'Uploaded')], default='pending', max_length=10, verbose_name='Status')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
                ('original_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='revisions', to='projects_app.document', verbose_name='Original Document')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='projects_app.project', verbose_name='Project')),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('due_date', models.DateField()),
                ('document', models.FileField(blank=True, null=True, upload_to='deliverables/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('uploaded', 'Uploaded'), ('approved', 'Approved'), ('commented', 'Commented'), ('rejected', 'Rejected'), ('annulled', 'Annulled')], default='pending', max_length=10)),
                ('comments', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliverables', to='projects_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_project_clients', to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_project_employees', to=settings.AUTH_USER_MODEL, verbose_name='Empleado')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='projects_app.project', verbose_name='Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('due_date', models.DateField(verbose_name='Fecha de vencimiento')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('completed', 'Completed')], default='pending', max_length=10, verbose_name='Estado')),
                ('is_personal', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Asignado a')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='projects_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('content', models.TextField(verbose_name='Contenido')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('status', models.CharField(choices=[('critical', 'Critical'), ('informative', 'Informative'), ('warning', 'Warning'), ('resolved', 'Resolved'), ('announcement', 'Announcement')], default='informative', max_length=15, verbose_name='Estado')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='projects_app.project', verbose_name='Proyecto')),
            ],
        ),
    ]
