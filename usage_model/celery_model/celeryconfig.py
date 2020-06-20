broker_url = 'redis://localhost:6379/1'

# Using the database to store task state and results.
result_backend = 'redis://localhost:6379/1'

enable_utc = True
CELERY_TIMEZONE = 'Asia/Shanghai'
timezone = 'Asia/Shanghai'
