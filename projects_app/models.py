# projects_app/models.py

import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Función para generar la ruta de subida de archivos
def get_upload_path(instance, filename):
    return f"project_files/{instance.deliverable.project.code}/documents/{filename}"


# Model de Proyecto
class Project(models.Model):
    PENDING = "pending"
    ONGOING = "ongoing"
    COMPLETED = "completed"

    STATUS_CHOICES = [
        (PENDING, _("Pending")),
        (ONGOING, _("Ongoing")),
        (COMPLETED, _("Completed")),
    ]

    name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Código"))
    description = models.TextField(verbose_name=_("Descripción"))
    start_date = models.DateField(verbose_name=_("Fecha de Inicio"))
    end_date = models.DateField(verbose_name=_("Fecha de Finalización"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PENDING, verbose_name=_("Estado")
    )
    assigned_to_client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_projects",
        verbose_name=_("Cliente Asignado"),
    )
    assigned_to_employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="assigned_employee_projects",
        verbose_name=_("Empleados Asignados"),
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


# Señal para generar códigos únicos de proyecto
@receiver(pre_save, sender=Project)
def generate_project_code(sender, instance, **kwargs):
    if not instance.code:
        latest_project = Project.objects.all().order_by("id").last()
        if latest_project:
            last_code = latest_project.code
            prefix = last_code[:2]
            number = int(last_code[2:]) + 1
            if number > 99:
                prefix = chr(ord(prefix[0]) + 1) + "A"
                number = 1
            instance.code = f"{prefix}{number:02}"
        else:
            instance.code = "AA01"


# Model de Asignación de Proyecto
class ProjectAssignment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Proyecto",
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_project_clients",
        verbose_name="Cliente",
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="assigned_project_employees",
        verbose_name="Empleado",
    )

    def __str__(self):
        return (
            f"{self.project.name} - {self.client.username} - {self.employee.username}"
        )


# Model de Tarea
class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    due_date = models.DateField(verbose_name="Fecha de vencimiento")
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("ongoing", "Ongoing"),
            ("completed", "Completed"),
        ],
        default="pending",
        verbose_name="Estado",
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Asignado a"
    )
    project = models.ForeignKey(
        "projects_app.Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks",
    )
    is_personal = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )

    def __str__(self):
        return self.name


def document_upload_path(instance, filename):
    # Obtener el código del proyecto desde la instancia
    project_code = instance.project.code
    # Verificar el grupo del usuario asignado
    if instance.assigned_to.groups.filter(name="employee").exists():
        folder = "entregados"
    elif instance.assigned_to.groups.filter(name="client").exists():
        folder = "recibidos"
    else:
        folder = "otros"

    # Incluir el número de versión en el nombre del archivo
    version = instance.version if instance.version else 1
    filename_base, filename_ext = os.path.splitext(filename)
    new_filename = f"{filename_base}_v{version}{filename_ext}"

    # Definir la estructura de carpetas
    return os.path.join(
        "project_files", project_code, "documents", folder, new_filename
    )


# Model de Documento
class Document(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Project"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    file = models.FileField(upload_to=document_upload_path, verbose_name=_("File"))
    status = models.CharField(
        max_length=10,
        choices=[("pending", _("Pending")), ("uploaded", _("Uploaded"))],
        default="pending",
        verbose_name=_("Status"),
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Assigned To"),
    )
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))
    version = models.IntegerField(default=1, verbose_name=_("Version"))
    original_document = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="revisions",
        verbose_name=_("Original Document"),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Si es un documento nuevo, incrementar el número de versión
            if self.original_document:
                self.version = self.original_document.version + 1
            else:
                self.version = 1
        super(Document, self).save(*args, **kwargs)


# Model de Actualización
class Update(models.Model):
    CRITICAL = "critical"
    INFORMATIVE = "informative"
    WARNING = "warning"
    RESOLVED = "resolved"
    ANNOUNCEMENT = "announcement"

    STATUS_CHOICES = [
        (CRITICAL, _("Critical")),
        (INFORMATIVE, _("Informative")),
        (WARNING, _("Warning")),
        (RESOLVED, _("Resolved")),
        (ANNOUNCEMENT, _("Announcement")),
    ]

    title = models.CharField(max_length=100, verbose_name=_("Título"))
    content = models.TextField(verbose_name=_("Contenido"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha"))
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=INFORMATIVE,
        verbose_name=_("Estado"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="updates",
        verbose_name=_("Proyecto"),
    )

    def __str__(self):
        return self.title


# Model de entregables por proyecto
class Deliverable(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="deliverables"
    )
    name = models.CharField(max_length=100)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    document = models.FileField(upload_to="deliverables/", null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", _("Pending")),
            ("uploaded", _("Uploaded")),
            ("approved", _("Approved")),
            ("commented", _("Commented")),
            ("rejected", _("Rejected")),
            ("annulled", _("Annulled")),
        ],
        default="pending",
    )
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
