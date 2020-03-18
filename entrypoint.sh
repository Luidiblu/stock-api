python manage.py db upgrade

rm -rf /srv/logs
mkdir /srv/logs/
touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

python stock_api/api/helper/essential_helper.py &

echo Starting Gunicorn
# flask run
exec gunicorn stock_api.wsgi:app \
    --bind 0.0.0.0:5000 \
    --chdir /app/stock_api \
    --workers 3 \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log
