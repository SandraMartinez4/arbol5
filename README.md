Proyecto Django 'arbol5'
-----------------------
- Formulario que acepta dos variables (X, Y) y permite escribir expresiones seguras
  usando X y Y (por ejemplo: X**2, 2*Y, X*Y + 3).
- Incluye configuración mínima para desplegar en Render (Procfile, build.sh, render.yaml).

Instrucciones locales:
1. crear virtualenv: python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py runserver
5. Abrir http://127.0.0.1:8000/

En Render: conecta el repo, configura variables de entorno DJANGO_SECRET_KEY y DJANGO_DEBUG (False).
