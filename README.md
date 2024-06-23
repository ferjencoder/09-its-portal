# ITS Portal
---
ITS Portal es una aplicación web desarrollada como proyecto final para el curso de Python de Coderhouse.
Esta aplicación está diseñada para facilitar la gestión de proyectos, comunicaciones y foros para distintos tipos de usuarios: administradores, empleados y clientes.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal utilizado para la lógica del backend.
- **Django**: Framework web utilizado para el desarrollo del backend.
- **SQLite**: Base de datos utilizada para el almacenamiento de datos.
- **Bootstrap**: Framework de CSS utilizado para el diseño y la apariencia.
- **JavaScript**: Utilizado para funcionalidades interactivas en el frontend.
- **HTML/CSS**: Lenguajes utilizados para la estructura y el diseño de las páginas web.
- **FontAwesome**: Utilizado para iconos en la interfaz de usuario.

## Funcionalidades de la Aplicación

### Administrador

- **Dashboard de Administrador**: Vista principal donde el administrador puede acceder a todas las funcionalidades.
- **Gestión de Proyectos**: Crear, ver y gestionar proyectos.
- **Gestión de Asignaciones**: Crear, ver y gestionar asignaciones para los empleados.
- **Mensajes**: Visualizar y gestionar mensajes.
- **Foro**: Participar y gestionar foros de discusión.
- **Blog**: Crear y gestionar publicaciones en el blog.

### Empleado

- **Dashboard de Empleado**: Vista principal donde los empleados pueden acceder a sus funcionalidades específicas.
- **Gestión de Proyectos**: Ver proyectos asignados.
- **Mensajes**: Visualizar y gestionar mensajes.
- **Foro**: Participar en foros de discusión.

### Cliente

- **Dashboard de Cliente**: Vista principal donde los clientes pueden acceder a sus funcionalidades específicas.
- **Gestión de Proyectos**: Ver proyectos en los que están involucrados.
- **Mensajes**: Visualizar y gestionar mensajes.
- **Foro**: Participar en foros de discusión.

## Instalación

### Requisitos Previos

- Python 3.7+
- Django 3.2+
- pip (gestor de paquetes de Python)
- Virtualenv (opcional, pero recomendado)

### Pasos para la Instalación

1. **Clonar el Repositorio**

```bash
   git clone https://github.com/usuario/its-portal.git
   cd its-portal
```

2. **Crear un Entorno Virtual**

```bash
python -m venv env
source env/bin/activate   # En windows: env\Scripts\activate
```

3. **Instalar las Dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar la Base de Datos**

```bash
python manage.py migrate
```

5. **Crear un Superusuario**

```bash
python manage.py createsuperuser
```

6. **Correr el Servidor de Desarrollo**

```bash
python manage.py runserver
```

7. **Acceder a la Aplicación**

Abre tu navegador y ve a http://127.0.0.1:8000

## Estructura del Proyecto

```md
its-portal/
├── blog/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── client_portal/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── employee_portal/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── forum_app/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── its_admin/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── its_portal/
│   ├── static/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── main/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── __init__.py
├── messages_app/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── projects/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── __init__.py
├── .env
├── db.sqlite3
├── manage.py
└── Pipfile
```

## Contribuir
Si deseas contribuir a este proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del proyecto.
2. Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).
3. Realiza tus cambios y haz commits descriptivos (git commit -am 'Agrega nueva funcionalidad').
4. Haz un push a la rama (git push origin feature/nueva-funcionalidad).
5. Abre un Pull Request.

## Licencia
Este proyecto está bajo la Licencia MIT. Para más detalles, consulta el archivo LICENSE.

## Contacto
Si tienes alguna pregunta o comentario sobre el proyecto, no dudes en contactarme:

Nombre: Fernanda Jensen
Email: ferjen.coder@gmail.com

¡Gracias por visitar el proyecto y espero tus comentarios y contribuciones!
