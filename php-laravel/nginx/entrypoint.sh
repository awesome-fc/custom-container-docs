#!/usr/bin/env bash

startNginxWhenFpmUp() {
    # Make sure port for NGINX proxying requests to PHP-FPM is up
    RETRY_INTERVAL=0.2 # in seconds
    while ! netstat -an | grep 'LISTEN\>' | grep ':9000\>'; do
        sleep $RETRY_INTERVAL
    done

    # Start NGINX server background 
    nginx -g 'daemon on;'
}

# In background, repeatedly check if PHP-FPM is up
startNginxWhenFpmUp &

# Start PHP-FPM in foreground
php-fpm
