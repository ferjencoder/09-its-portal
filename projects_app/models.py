# projects_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Función para generar la ruta de subida de archivos
def get_upload_path(instance, filename):
    return f"projects_files/{instance.deliverable.project.code}/documents/{filename}"


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

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    description = models.TextField(verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PENDING, verbose_name=_("Status")
    )
    assigned_to_employees = models.ManyToManyField(
        User,
        blank=True,
        related_name="assigned_employee_projects",
        verbose_name=_("Assigned Employees"),
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
        choices=[("pending", "Pendiente"), ("completed", "Completada")],
        default="pending",
        verbose_name="Estado",
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Asignado a"
    )

    def __str__(self):
        return self.name


# Model de Documento
class Document(models.Model):
    deliverable = models.ForeignKey(
        "Deliverable", on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to="get_upload_path", verbose_name=_("File"))
    status = models.CharField(
        max_length=10,
        choices=[("pending", _("Pending")), ("uploaded", _("Uploaded"))],
        default="pending",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name=_("Assigned To"),
    )
    comments = models.TextField(null=True, blank=True, verbose_name=_("Comments"))

    def __str__(self):
        return self.file.name


# Model de Actualización
class Update(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="updates",
        verbose_name="Proyecto",
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
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    document = models.FileField(upload_to="deliverables/", null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("uploaded", "Uploaded"),
            ("approved", "Approved"),
            ("commented", "Commented"),
            ("rejected", "Rejected"),
            ("annulled", "Annulled"),
        ],
        default="pending",
    )
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
