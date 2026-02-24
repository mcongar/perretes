# 🐶 Perretes

Red social para amantes de los perros donde los usuarios pueden publicar mensajes cortos llamados **ladridos**.

Prueba técnica para el puesto de desarrollador Full-Stack en Ábaco.

---

## 🚀 Instalación y puesta en marcha

### Requisitos previos

- Python 3.10 o superior
- pip

### Pasos

1. **Clona el repositorio**

```bash
git clone https://github.com/mcongar/perretes.git
cd perretes
```

1. **Crea y activa el entorno virtual**

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

1. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

1. **Aplica las migraciones**

```bash
python manage.py migrate
```

1. **Arranca el servidor**

```bash
python manage.py runserver
```

1. Abre el navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Acceso al panel de administración (opcional)

```bash
python manage.py createsuperuser
```

Disponible en [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## ✨ Funcionalidades

- Registro de usuario con login automático al crear la cuenta
- Inicio de sesión y cierre de sesión
- Publicar ladridos de hasta 140 caracteres con contador en tiempo real
- Ver perfil público de cualquier usuario en `/usuarios/<username>/`
- Edición inline de ladridos propios sin cambiar de página
- Eliminación de ladridos con confirmación
- Página de error personalizada para perfiles inexistentes
- Panel de administración con búsqueda y filtros

---

## 🏗️ Decisiones técnicas

### Backend: Django

Django incluye de serie todo lo necesario para esta prueba: ORM, sistema de autenticación, panel de administración, sistema de templates y gestión de archivos estáticos. No fue necesario añadir ninguna dependencia adicional más allá del propio framework.

### Base de datos: SQLite

SQLite es la opción por defecto de Django y más que suficiente para una aplicación de este alcance. Facilita además la instalación al no requerir ningún servidor de base de datos externo.

### Frontend: Django Templates + CSS vanilla

Se optó por Django Templates para mantener el proyecto como una única unidad cohesionada sin necesidad de un servidor frontend separado, configuración de CORS ni proceso de build. Los estilos se escribieron en CSS puro con custom properties para mantener el proyecto sin dependencias de frontend y demostrar control sobre los estilos base.

### Estructura del proyecto

```
perretes/
  core/
    static/core/css/    → estilos
    templates/
      base.html         → template global
      core/             → templates de la app
      errors/           → páginas de error
    models.py
    views.py
    forms.py
    admin.py
  perretes/
    settings.py
    urls.py
```

---

## 🔮 Mejoras con más tiempo

- **Tests automatizados** — tests unitarios para modelos y vistas con `pytest-django`
- **Paginación** — los ladridos se cargan todos de golpe, con volumen alto convendría paginar
- **Feed global** — página de inicio con ladridos de todos los usuarios ordenados por fecha
- **Seguir usuarios** — modelo de follows para construir un feed personalizado
- **Dockerización** — `Dockerfile` y `docker-compose.yml` para facilitar el despliegue
- **Variables de entorno** — mover `SECRET_KEY` y `DEBUG` a un `.env` con `python-decouple`
- **Base de datos en producción** — migrar a PostgreSQL para un entorno real

