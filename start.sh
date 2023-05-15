#!/bin/bash
cd /home/akim_malyschik/event-scheduler-backend
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 wsgi:app
