from apis_acdhch_default_settings.settings import *

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True
APIS_BASE_URI = "https://apis-demo.acdh-dev.oeaw.ac.at/"
ROOT_URLCONF = "apis_ontology.urls"
ADDITIONAL_APPS = [
    "apis_core.documentation",
    "django.contrib.staticfiles",
    "django_cosmograph",
]

for app in ADDITIONAL_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)
