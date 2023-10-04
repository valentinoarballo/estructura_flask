#!/bin/bash

# Run your first command (e.g., flask db init)
flask db init

# Run your second command (e.g., another command)
flask db migrate -m "initial migration"

# Run your third command (e.g., yet another command)
flask db upgrade

# Start your Flask application
gunicorn app:app --bind 0.0.0.0:5005 #module_name:application_variable_name

#0.0.0.0: This is the host IP address.
#Using 0.0.0.0 means Gunicorn will listen on all available network interfaces,
# making the application accessible from outside the container.