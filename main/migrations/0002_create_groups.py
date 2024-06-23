from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    client_group, created = Group.objects.get_or_create(name="client")
    employee_group, created = Group.objects.get_or_create(name="employee")

    # Add permissions if needed
    # Permission = apps.get_model("auth", "Permission")
    # permission = Permission.objects.get(codename='your_permission_codename')
    # client_group.permissions.add(permission)
    # employee_group.permissions.add(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
