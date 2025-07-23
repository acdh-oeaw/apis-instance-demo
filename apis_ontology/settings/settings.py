from apis_acdhch_default_settings.settings import *

from pathlib import Path

BASE_DIR = Path(__file__).resolve()
DEBUG = True
APIS_BASE_URI = "https://apis-demo.acdh-dev.oeaw.ac.at/"
ROOT_URLCONF = "apis_ontology.urls"
