#!/usr/bin/env bash

# Start PHP-FPM in background
php-fpm -D

# Make sure port for NGINX proxying requests to PHP-FPM is up
RETRY_INTERVAL=0.2 # in seconds
while ! netstat -an | grep 'LISTEN\>' | grep ':9000\>'; do
    sleep $RETRY_INTERVAL
done

# Start NGINX server in foreground
nginx -g 'daemon off;'
