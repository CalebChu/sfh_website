# Service for Humanity Website

A Django website for **Service for Humanity (SfH)**, a student-led organization at Austin High School connecting students with volunteer opportunities in the Greater Houston area.

The site brings public club information, member registration, volunteering, event attendance, and participation points into one place.

## Features

- **Public pages:** club mission, officer directory, photo gallery, and site credits.
- **Google sign-in:** account creation and authentication through Google Identity Services.
- **Member profiles:** membership registration, grade and contact information, and profile editing.
- **Volunteer opportunities:** officer-created listings with dates, locations, capacity limits, member sign-ups, and attendance tracking.
- **Club events:** event listings and time-limited attendance links displayed as QR codes.
- **Points and leaderboard:** attendance-related points, manual officer adjustments, transaction history, and member rankings.
- **Officer tools:** announcements, event and opportunity management, gallery uploads, and registration codes managed by superusers.

## Tech stack

| Component | Technology |
| --- | --- |
| Backend | Python and Django 5.0.6 |
| Frontend | Django templates, CSS, and JavaScript |
| Authentication | Google Identity Services and Django sessions |
| Database | MySQL in the checked-in settings; SQLite can be used for local development |
| Image handling | Pillow and Django image fields |
| Dependencies | Pinned in `requirements.txt` |

## Project structure

| Path | Purpose |
| --- | --- |
| `sfh_website/` | Project settings, root URLs, and WSGI/ASGI entry points |
| `default/` | Public pages, Google sign-in, gallery, and shared templates |
| `members/` | Member profiles and registration |
| `officers/` | Officer profiles and registration codes |
| `private/` | Dashboard, volunteering, events, attendance, announcements, and points |
| `static/` | CSS, JavaScript, images, fonts, and other frontend assets |
| `manage.py` | Django management commands |
| `requirements.txt` | Python dependencies |

## Local development

### 1. Clone and install

Use Python 3.12 as a starting point for the pinned dependencies. The repository does not declare a supported Python version.

```bash
git clone https://github.com/CalebChu/sfh_website.git
cd sfh_website
python -m venv .venv
```

Activate the virtual environment:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Then install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2. Configure a local database and hostnames

**Before running migrations, replace the database configuration in your local copy of `sfh_website/settings.py`.** The checked-in configuration points to a hosted MySQL database. Use a separate development database.

For a simple local setup, replace the entire `DATABASES` assignment with:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Also set local hostnames:

```python
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

Keep `DEBUG = True` only for local development. Use a separate development secret key.

If you use MySQL instead, configure your own database credentials and install a compatible driver such as `mysqlclient`; it is not included in `requirements.txt`.

Settings call `load_dotenv()`, but the database credentials and Django secret key are currently hardcoded. Adding a `.env` file alone does not override those values.

Keep local credentials, `.venv/`, and `db.sqlite3` out of commits. The current `.gitignore` does not cover all of these.

### 3. Initialize and run

After configuring the local database:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://localhost:8000/](http://localhost:8000/). Django administration is available at [http://localhost:8000/admin/](http://localhost:8000/admin/).

The superuser account provides access to Django administration. Member and officer access in the main site also requires the corresponding profile.

### 4. Configure Google sign-in

Google sign-in requires a Google OAuth web client configured for your development origin.

1. Configure a web client in Google Cloud for your local origin, such as `http://localhost:8000`.
2. Configure the login callback URL used by the site: `http://localhost:8000/auth-receiver`.
3. Update the client ID in **both** `default/templates/sign_in.html` (`data-client_id`) and `default/views.py` (the audience passed to `verify_oauth2_token`).
4. Visit `/sign-in` and sign in with Google.

Use the same hostname throughout the flow. The callback is built from the incoming request's origin. A new Google account is redirected to complete the membership form.

## Accounts and workflows

- **Members** sign in with Google, complete their membership profile, and use the dashboard to find volunteer opportunities, register, view events, and track points.
- **Officers** register at `/officers/form` using an active officer code. Their tools include creating listings, recording attendance, posting announcements, and adjusting points.
- **Superusers** can manage data through `/admin/` and generate officer registration codes at `/officers/codes`.

`SIGN_UPS_OPEN` in `sfh_website/settings.py` controls registration availability. Superuser status alone does not create an officer profile.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Public home page |
| `/gallery` | Photo gallery |
| `/officers_info` | Public officer directory |
| `/sign-in` | Google sign-in |
| `/p/dashboard` | Member/officer dashboard |
| `/p/volunteering` | Volunteer opportunities |
| `/p/events` | Club events |
| `/p/announcements` | Announcements |
| `/p/points` | Points and transaction management |
| `/p/leaderboard` | Member rankings |
| `/admin/` | Django administration |

Most application routes are defined without a trailing slash. Pages under `/p/` require a member or officer profile.

## Development checks

With the development database configured:

```bash
python manage.py check
python manage.py test
```

The app test files currently contain placeholders or commented-out tests, so the test command does not provide meaningful automated coverage yet. Manually verify sign-in, registration, role permissions, volunteer sign-ups, attendance, and points when changing these workflows.

## Deployment notes

The checked-in settings require changes before production use:

- Rotate exposed credentials and move secrets and database configuration out of source control.
- Disable `DEBUG`, configure the deployment's allowed hosts, and review HTTPS/session security settings.
- Configure the Google client and callback URL for the deployment domain.
- Configure persistent upload storage and media serving. `MEDIA_ROOT` and `MEDIA_URL` are currently empty.
- Collect static assets with `python manage.py collectstatic` and configure the host to serve `STATIC_ROOT`.
- Run migrations against the intended deployment database.

Django entry points are `sfh_website.wsgi:application` and `sfh_website.asgi:application`. Gunicorn is included in the dependencies.

## Credits

Created by **Caleb Chu, Austin High School Class of 2026**.

Icon attributions are listed in `default/templates/credit.html`. The bundled QRCode.js library includes its own license under `static/javascript/davidshimjs-qrcodejs-04f46c6/`.

No project-level license is currently included in this repository.
