#!/bin/bash

NAME="hoitymoppet"                                   # Name of the application
DJANGODIR=/home/arkess1/public_html/live/Ecommerce_Website               # Django project directory
SOCKFILE=/home/arkess1/public_html/live/hoity_live_env/bin/gunicorn.sock  # we will communicte using this unix socket
USER=arkess1                                         # the user to run as
GROUP=arkess1                                        # the group to run as
NUM_WORKERS=3                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=Ecommerce_Website.settings      # which settings file should Django use
DJANGO_WSGI_MODULE=Ecommerce_Website.wsgi              # WSGI module name
echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
source /home/arkess1/public_html/live/hoity_live_env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-

