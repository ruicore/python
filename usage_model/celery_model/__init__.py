from usage_model.celery_model import celeryconfig
from celery import Celery

app = Celery("tasks")
app.config_from_object(celeryconfig)

if __name__ == "__main__":
    app.start()
