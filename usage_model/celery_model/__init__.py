from celery import Celery

from usage_model import celeryconfig

app = Celery("tasks")
app.config_from_object(celeryconfig)
