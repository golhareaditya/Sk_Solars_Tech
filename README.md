# sk_solar

Render deployment ke liye admin login enable karne ke liye ye environment variables set karein:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

Deploy ke time `python manage.py ensure_admin_user` automatically admin account create ya update karega.

## PostgreSQL setup

Ye project Postgres ke saath chal sakta hai agar aap `DATABASE_URL` environment variable set karte hain.
Production deploy mein SQLite use na karein. SQLite single-file database hai, isliye 5000 visitors/concurrent traffic ke liye PostgreSQL required hai.

Local se Postgres par migrate karne ke liye, naya management command use karein:

1. `DATABASE_URL` set karein (example):
   ```bash
   export DATABASE_URL="postgres://user:password@localhost:5432/dbname"
   ```
2. Migration command chalayein:
   ```bash
   python manage.py migrate_sqlite_to_postgres
   ```

Agar aap specific database URL dena chahte hain:

```bash
python manage.py migrate_sqlite_to_postgres --database-url "postgres://user:password@localhost:5432/dbname"
```

Ye command current default database se data dump karega, target PostgreSQL database par migrations apply karega, aur data load karega.

Render deployment already `render.yaml` mein `DATABASE_URL` use karta hai aur `psycopg[binary]` dependency installed hai.

## Production capacity for 5000 people

`render.yaml` Gunicorn ko multiple workers aur threads ke saath start karta hai:

```bash
gunicorn sk_solar.wsgi:application --workers ${WEB_CONCURRENCY:-3} --threads ${GUNICORN_THREADS:-2}
```

Important production settings:

- `DEBUG=false`
- `DATABASE_URL=postgres://...`
- `DATABASE_CONN_MAX_AGE=600`
- `DATABASE_SSL_REQUIRE=true`
- `WEB_CONCURRENCY=3`
- `GUNICORN_THREADS=2`

5000 users handle karne ke liye free app/database plan enough nahi hota. Render par app service aur PostgreSQL database ko paid/scaled plan par rakhein, monitoring enable karein, aur traffic badhne par `WEB_CONCURRENCY`, `GUNICORN_THREADS`, app instances, aur database size ko metrics ke hisaab se increase karein.

Media uploads (`MEDIA_ROOT`) local disk par hain. Production mein gallery/user uploaded images ke liye S3, Cloudinary, ya kisi persistent object storage ka use karein, warna deploy/restart ke baad files lose ho sakti hain.
