# PEC College Examination Portal

Complete Flask website prototype for a college online examination portal.

## Stack
- HTML5
- CSS3
- Vanilla JavaScript
- Python Flask
- Jinja2 templates
- Gunicorn for cloud deployment

## Pages
- Home
- About
- Login
- Student Dashboard
- Online Examination
- Result
- Admin Dashboard
- 404 page

## Backend integration
Flask handles:
- Page routing
- Student/Admin sessions
- Login form
- Exam selection
- Question submission
- Automatic scoring
- Result generation
- Access control

No database is used in this prototype, as requested. Exam data is kept in `app.py`, and login/result information uses Flask sessions.

## Run in VS Code

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo login
Any username and password works.

Choose:
- Student → Student Dashboard
- Admin / Faculty → Admin Dashboard

## Deploy to Render

Build command:
```text
pip install -r requirements.txt
```

Start command:
```text
gunicorn app:app
```

`render.yaml` is already included.

## Important
This is a college project prototype. For a production examination system, add a real database, secure authentication, CSRF protection, HTTPS, persistent exam attempts and server-side security controls.
