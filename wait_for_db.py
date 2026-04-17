import time
import psycopg2
import sys

from conf.config import settings


TIMEOUT = 20  # секунд
start_time = time.time()

while True:
    try:
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
        )
        conn.close()
        print("✅ Postgres is ready!")
        break

    except psycopg2.OperationalError:
        elapsed = time.time() - start_time

        if elapsed > TIMEOUT:
            print("Timeout: Postgres is not ready after 20 seconds")
            sys.exit(1)

        print(f"Waiting for Postgres... ({int(elapsed)}s)")
        time.sleep(1)
