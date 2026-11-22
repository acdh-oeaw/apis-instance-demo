# Demo APIS Instance

This demo instance of APIS makes use of a fictional data model and sample data to demonstrate its features.


# Local Postres Database

Run these as a PostgreSQL superuser. `sudo -u postgres psql`.
```
CREATE ROLE apis_demo_admin WITH LOGIN PASSWORD 'apis_demo_admin_password' CREATEDB;
CREATE DATABASE apis_demo_db OWNER apis_demo_admin;
\c apis_demo_db
GRANT ALL ON SCHEMA public TO apis_demo_admin;
\du apis_demo_db
\l apis_demo_db
```

And add the following to the local settings:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "apis_demo_db",
        "USER": "apis_demo_admin",
        "PASSWORD": "apis_demo_admin_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

```

`
