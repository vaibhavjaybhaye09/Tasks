# Django Offline Deployment on Raspberry Pi

This guide explains how to deploy a Django application on a Raspberry Pi for stable, long-running offline use on a local network (LAN only).

## 1. Overview

This setup is intended for:

- Internal dashboards and business tools
- IoT/text-based monitoring systems
- Large local datasets and log-heavy applications
- Multi-user access inside a private network

Core goals:

- No internet dependency during runtime
- Reliable 24/7 service
- Good performance on constrained hardware

## 2. Architecture

Request flow:

`Laptop/Mobile (LAN) -> Nginx -> Gunicorn -> Django -> PostgreSQL -> SSD`

Component roles:

- `Nginx`: reverse proxy, static/media serving
- `Gunicorn`: production WSGI process manager
- `Django`: application logic
- `PostgreSQL`: primary data store
- `SSD`: durable and fast storage for database-heavy workloads

## 3. Hardware Recommendations

Minimum:

- Raspberry Pi 4 with 4 GB RAM

Recommended (production):

- Raspberry Pi 4 with 8 GB RAM
- External USB 3.0 SSD
- 32 GB+ SD card for OS only

Why use an SSD:

- Better read/write performance
- Lower risk of SD card wear/corruption
- Better fit for large and growing datasets

## 4. Operating System

Install:

- Raspberry Pi OS Lite (64-bit)

Update system packages:

```bash
sudo apt update
sudo apt upgrade -y
```

## 5. Install System Dependencies

```bash
sudo apt install python3.11 python3.11-venv python3-pip git nginx \
postgresql postgresql-contrib libpq-dev build-essential -y
```

## 6. Python Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required Python packages:

```bash
pip install django gunicorn psycopg2-binary djangorestframework pillow python-docx
```

## 7. Django Production Settings

In `settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ["*"]
CONN_MAX_AGE = 60

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Collect static files:

```bash
python manage.py collectstatic
```

Notes:

- Keep database host local: `HOST = "localhost"`
- Avoid runtime dependencies on cloud services or external APIs

## 8. PostgreSQL Setup

Open PostgreSQL shell:

```bash
sudo -u postgres psql
```

Create DB and user:

```sql
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
\q
```

Configure Django database:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "myuser",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Apply migrations:

```bash
python manage.py migrate
```

## 9. Large Data Optimization

Index frequently filtered/sorted fields:

```python
class Log(models.Model):
    created_at = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=50, db_index=True)
```

Avoid unbounded queries:

```python
# Avoid
Log.objects.all()

# Prefer
Log.objects.order_by("-created_at")[:100]
```

Use pagination for list views and archive/clean old rows on schedule.

## 10. Run Django with Gunicorn

Example:

```bash
gunicorn project.wsgi:application --workers 3 --bind 0.0.0.0:8000
```

Worker rule of thumb:

- `workers = (CPU cores * 2) + 1`

For a Raspberry Pi 4, start with `3` workers and tune using real load.

## 11. Nginx Configuration

Create:

- `/etc/nginx/sites-available/django`

Example config:

```nginx
server {
    listen 80;
    client_max_body_size 20M;
    keepalive_timeout 65;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /home/pi/project/staticfiles/;
    }

    location /media/ {
        alias /home/pi/project/media/;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

Find Pi IP:

```bash
hostname -I
```

Access app at:

- `http://<Pi-IP>`

## 12. Enable Services at Boot

```bash
sudo systemctl enable nginx
sudo systemctl enable postgresql
```

Create a `systemd` service for Gunicorn so the app also starts automatically.

## 13. Optional Offline Python Package Install

On a machine with internet:

```bash
pip freeze > requirements.txt
pip download -r requirements.txt -d packages/
```

On the Raspberry Pi (offline):

```bash
pip install --no-index --find-links=packages -r requirements.txt
```

## 14. Monitoring and Maintenance

Useful commands:

```bash
df -h
htop
```

Backup database:

```bash
pg_dump mydb > backup.sql
```

Operational recommendations:

- Store PostgreSQL data on SSD
- Clean old media/log files regularly
- Run weekly backups and test restore procedure

## 15. Network Stability

Assign a static IP by editing:

- `/etc/dhcpcd.conf`

This prevents LAN address changes that break client access.

## 16. Expected Capacity (Typical)

With Raspberry Pi 4 (8 GB) + SSD + PostgreSQL + Nginx/Gunicorn, typical targets are:

- Millions of records
- Around 50 to 100 LAN users
- Sub-100 ms responses for optimized endpoints
- Continuous 24/7 runtime

Actual results depend on query complexity, indexing quality, and request patterns.

## 17. Suggested Project Layout

```text
/home/pi/project/
|-- project/
|-- apps/
|-- staticfiles/
|-- media/
|-- venv/
|-- requirements.txt
`-- manage.py
```

## 18. Production Checklist

Before go-live, confirm:

- `DEBUG = False`
- `ALLOWED_HOSTS` is set correctly
- Static files collected
- PostgreSQL running locally
- Nginx serving traffic
- Gunicorn running via service
- Static IP configured
- Backup and restore tested
- Reboot test passed

## Final Recommendation

For reliable offline Django deployment on Raspberry Pi, use:

- Raspberry Pi 4 (8 GB)
- Local PostgreSQL
- External SSD
- Nginx + Gunicorn
- Indexed models + paginated views

This combination is practical for long-term internal production workloads.
