#!/bin/bash

cd $APP_DIR
ADMIN_PASS=${ADMIN_PASS:-}
python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
#python manage.py buildwatson

if [ ! -z "$ADMIN_PASS" ] ; then
  python manage.py update_admin_user --username=admin --password=$ADMIN_PASS
else
  python manage.py update_admin_user --username=admin --password=password
fi

chown -R www-data:www-data $APP_DIR
chmod go+x $APP_DIR
mkdir -p /var/log/gunicorn
touch /var/log/gunicorn/gunicorn-error.log
touch /var/log/gunicorn/gunicorn-access.log
tail -n 0 -f /var/log/gunicorn/gunicorn*.log &
export PYTHONPATH=$PYTHONPATH:$APP_DIR
export DJANGO_SETTINGS_MODULE='sal.settings'
#export SECRET_KEY='no-so-secret' # Fix for your own site!
# chdir /var/www/django/sd_sample_project/sd_sample_project
if [ "$DOCKER_SAL_DEBUG" = "true" ] || [ "$DOCKER_SAL_DEBUG" = "True" ] || [ "$DOCKER_SAL_DEBUG" = "TRUE" ] ; then
    service nginx stop
    echo "RUNNING IN DEBUG MODE"
    python manage.py runserver 0.0.0.0:8000
else
    supervisord --nodaemon -c $APP_DIR/supervisord.conf
fi