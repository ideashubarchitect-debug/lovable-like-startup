# Gunicorn config for KloudBean Django app
# Use sync workers to avoid gthread "Invalid file descriptor: -1" in murder_keepalived
# See: https://github.com/benoitc/gunicorn/issues/3029

worker_class = "sync"
workers = 4
bind = "0.0.0.0:8000"
timeout = 120
