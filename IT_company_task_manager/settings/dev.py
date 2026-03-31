from IT_company_task_manager.settings.base import *

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = False

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

