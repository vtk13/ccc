#!/usr/bin/env bash
CURRENT_DIR=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)

git pull

cd ${CURRENT_DIR}/cc
python3 ./manage.py migrate
python3 manage.py collectstatic --noinput

cd ${CURRENT_DIR}
bower --allow-root install
rm -rf cc/goods/static/assets
mkdir cc/goods/static/assets

cp bower_components/jquery/dist/jquery.min.js cc/goods/static/assets/jquery.js
cp bower_components/requirejs/require.js cc/goods/static/assets/require.js
mkdir cc/goods/static/assets/selectize
cp bower_components/selectize/dist/js/standalone/selectize.min.js cc/goods/static/assets/selectize/selectize.js
cp bower_components/selectize/dist/css/* cc/goods/static/assets/selectize/
mkdir cc/goods/static/assets/bootstrap
cp -r bower_components/bootstrap/dist/* cc/goods/static/assets/bootstrap

chmod 777 media/good_images

/etc/init.d/apache2 restart
