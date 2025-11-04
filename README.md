# Tkinter + Django Apps

This repo contains:
- A Tkinter Loan Calculator with validation, history, save/load, and CSV export.
- A Django real-time chat app with authentication, room CRUD, search/filter, and WebRTC video calling.

## Prerequisites
- Windows
- Python 3.10+
- (Optional) Virtualenv

## Tkinter App
Run:
1) `python d:\mscs\OOP\Django\LoanCalculator.py`

Features:
- Validate amount/rate/duration
- Correct amortization formula
- History display
- Save/Load JSON
- Export CSV
- Modal StudentID dialog

## Django App
Setup:
1) `python -m venv venv`
2) `venv\Scripts\activate`
3) `pip install "django>=5.0,<6.0" "channels>=4.0,<5.0" daphne`
4) `django-admin startproject config .` (already done if files exist)
5) `django-admin startapp chat` (already done if files exist)
6) `python manage.py makemigrations`
7) `python manage.py migrate`
8) `python manage.py createsuperuser`
9) `python manage.py runserver`

Open `http://127.0.0.1:8000/`

Features:
- Signup/Login/Logout
- Create and search rooms
- Real-time chat
- WebRTC video calls (open same room in two browsers)
- Simple dashboard stats on home page

## Notes
- For production/WebRTC reliability across networks, you’ll want TURN servers; the default STUN may be enough for local testing.
- Channels in-memory layer is used for dev. For multi-process or scaling, configure Redis.

## Deploy (Render)
This app supports WebSockets and HTTPS (required for camera/mic). Deploy using Render:

1) Push this repo to GitHub (see commands below).
2) In Render, “New +” → “Blueprint” → select this repo → it will read `render.yaml`.
3) Wait for build; Render runs `collectstatic` and `migrate` automatically.
4) Open the service URL, e.g. `https://django-chat.onrender.com/`.

If deploying manually (without blueprint):
- Build: `pip install -r requirements.txt`
- Start: `daphne -b 0.0.0.0 -p $PORT config.asgi:application`

## Deploy (Railway)
1) Push this repo to GitHub.
2) Railway → New Project → Deploy from GitHub → choose this repo.
3) Variables:
   - SECRET_KEY = any secure random string
   - DJANGO_SETTINGS_MODULE = config.settings
   - PYTHON_VERSION = 3.12
4) Railway detects the Procfile and runs:
   - collectstatic, migrate, then starts Daphne.
5) Open your live URL: https://<your-service>.up.railway.app/

## GUI App Download
The Tkinter GUI is packaged as a Windows executable.

Build locally:
- Install: `pip install pyinstaller`
- Build LoanCalculator: `pyinstaller --onefile --windowed --name LoanCalculator LoanCalculator.py`
- Build GUIControls: `pyinstaller --onefile --windowed --name GUIControls GUIControls.py`

Publish:
- Create a GitHub Release and upload `dist\LoanCalculator.exe` and `dist\GUIControls.exe`.
- Download URL: https://github.com/<your-username>/<repo>/releases/latest

## Features Added (Short Note)
Tkinter:
- Validation for amount/rate/duration
- Correct amortization and zero-interest handling
- Currency dropdown and styled UI
- History list + load selected
- Save/Load JSON, CSV export
- Light/Dark theme toggle
- Modal StudentID dialog

Django:
- Auth (signup/login/logout)
- Room create, search/filter
- Real-time chat (Channels/WebSockets)
- WebRTC video calling with robust signaling (glare rollback, ICE queuing)
- Responsive room UI with status badge
- Static serving + deployment config (WhiteNoise, Railway)