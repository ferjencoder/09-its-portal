# ITS Portal
---
ITS Portal es una aplicación web desarrollada como proyecto final para el curso de Python de Coderhouse.
Esta aplicación está diseñada para facilitar la gestión de proyectos, comunicaciones y foros para distintos tipos de usuarios: administradores, empleados y clientes.

---

## Índice
- [Pasos para cargar la bd y probar el site](#pasos-para-cargar-la-bd-y-probar-el-site)
- [Tests](#tests)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Funcionalidades de la Aplicación](#funcionalidades-de-la-aplicación)
  - [Administrador](#administrador)
  - [Empleado](#empleado)
  - [Cliente](#cliente)
- [Instalación](#instalación)
  - [Requisitos Previos](#requisitos-previos)
  - [Pasos para la Instalación](#pasos-para-la-instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)


## Pasos para popular la db y probar el site:

### Scripts para popular la db
1. python main/reset_migrations_and_db.py
2. python main/create_test_all_data.py (crea data para blog_app, forum_app, messages_app y projects_app)

### Scripts individuales para popular la db
1. python main/reset_migrations_and_db.py
2. python main/create_test_users.py
3. python blog_app/create_test_blog_data.py
4. python forum_app/create_test_forum_data.py 
5. python messages_app/create_test_messages_data.py
6. python messages_app/create_test_projects_data.py

## Tests:
1. python manage.py test blog_app
2. python manage.py test forum_app
3. python manage.py test main
4. python manage.py test messages_app
5. python manage.py test projects_app

## Tecnologías Utilizadas

- **Python**: Lenguaje principal utilizado para la lógica del backend.
- **Django**: Framework web utilizado para el desarrollo del backend.
- **SQLite**: Base de datos utilizada para el almacenamiento de datos.
- **JavaScript**: Utilizado para funcionalidades interactivas en el frontend.
- **CKeditor5**: Utilizado para agregar texto enriquecido en las publicaciones del blog y otros contenidos.
- **JSON**: Formato utilizado para el intercambio de datos.
- **AJAX**: Técnica utilizada para la actualización asíncrona de las páginas web.
- **Bootstrap**: Framework de CSS utilizado para el diseño y la apariencia.
- **FontAwesome**: Utilizado para iconos en la interfaz de usuario.

## Funcionalidades de la Aplicación

### Administrador

- **Dashboard de Administrador**: Vista principal donde el administrador puede acceder a todas las funcionalidades.
- **Gestión de Proyectos**: Crear, ver, editar y eliminar proyectos. Asignar empleados y clientes a los proyectos.
- **Gestión de Asignaciones**: Crear, ver y gestionar asignaciones para los empleados.
- **Gestión de Entregables**: Crear, ver, editar, subir documentos, aprobar y eliminar entregables.
- **Gestión de Tareas**: Ver y actualizar el estado de las tareas asignadas a los empleados.
- **Gestión de Actualizaciones**: Ver las actualizaciones relacionadas con los proyectos.
- **Mensajes**: Visualizar y gestionar mensajes entre usuarios.
- **Foro**: Participar y gestionar foros de discusión.
- **Blog**: Crear, editar y gestionar publicaciones en el blog.

### Empleado

- **Dashboard de Empleado**: Vista principal donde los empleados pueden acceder a sus funcionalidades específicas.
- **Gestión de Proyectos**: Ver proyectos asignados y sus detalles.
- **Gestión de Entregables**: Ver entregables asignados y su estado. Subir documentos y comentar sobre los entregables.
- **Gestión de Tareas**: Ver y actualizar el estado de las tareas asignadas.
- **Mensajes**: Visualizar y gestionar mensajes entre usuarios.
- **Foro**: Participar en foros de discusión y colaborar con otros empleados y administradores.
- **Blog**: Ver y comentar en publicaciones del blog.

### Cliente

- **Dashboard de Cliente**: Vista principal donde los clientes pueden acceder a sus funcionalidades específicas.
- **Gestión de Proyectos**: Ver proyectos en los que están involucrados, sus detalles y progreso.
- **Gestión de Entregables**: Ver entregables y su estado.
- **Mensajes**: Visualizar y gestionar mensajes entre usuarios.
- **Foro**: Participar en foros de discusión relacionados con sus proyectos.
- **Blog**: Ver y comentar en publicaciones del blog.

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

## Pendientes
- [ ] README.md: versión inglés también
- [ ] Video: versión esp e inglés
- [ ] Repensar: uso de jquery, es poco pero...
- [ ] Look and feel: el dark-mode para los group-items por ej.
- [ ] Funcionalidad para que el usuario pueda dockear los paneles a su gusto.
- [ ] Un settings para que el user pueda manejar notificaciones y seleccionar una paleta de colores por ej.
- [ ] Pensar en agregar react... websockets...

## Estructura del Proyecto
- main/: Contiene la configuración principal del proyecto.
- blog_app/: Aplicación para la gestión de blogs.
- forum_app/: Aplicación para la gestión de foros.
- messages_app/: Aplicación para la gestión de mensajes.
- projects_app/: Aplicación para la gestión de proyectos.
- static/: Archivos estáticos (CSS, JavaScript, imágenes).
- templates/: Plantillas HTML para la representación de las vistas.
- requirements.txt: Lista de dependencias del proyecto.

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
