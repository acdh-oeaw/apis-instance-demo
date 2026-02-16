import os
from pathlib import Path

from apis_acdhch_default_settings.settings import *

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
APIS_BASE_URI = "https://apis-demo.acdh-dev.oeaw.ac.at/"
ROOT_URLCONF = "apis_ontology.urls"
ADDITIONAL_APPS = [
    "apis_core.documentation",
    "django.contrib.staticfiles",
    "django_cosmograph",
]
CSP_DEFAULT_SRC = CSP_DEFAULT_SRC + (
    "'unsafe-eval'",  # needed for cosmograph 1.4.2
    "xovkkfhojasbjinfslpx.supabase.co",  # cosmograph telemetry
)

for app in ADDITIONAL_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)


APIS_BIBSONOMY = [
    {
        "type": "zotero",
        "url": "https://api.zotero.org",
        "user": os.environ.get("APIS_BIBSONOMY_USER"),
        "API key": os.environ.get("APIS_BIBSONOMY_PASSWORD"),
        "group": "297412",
    }
]
