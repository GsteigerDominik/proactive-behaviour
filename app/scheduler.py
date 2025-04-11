from apscheduler.schedulers.background import BackgroundScheduler

from app import app


def acting():
    app.acting()


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(acting, 'interval', minutes=5)
    scheduler.start()

    # Keep alive
    import time

    while True:
        time.sleep(60)
