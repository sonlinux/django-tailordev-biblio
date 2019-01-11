
CELERYBEAT_SCHEDULE = {
    'import_reference_records': {
        'task': 'tasks.import_reference_record',
        'schedule': 3600.0,  # update every 60 minutes
    }
}

CELERY_TIMEZONE = 'UTC'
