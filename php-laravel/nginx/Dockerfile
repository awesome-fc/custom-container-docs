FROM php:7.4-fpm

# Install dependencies
RUN apt-get update -y && apt-get install -y nginx net-tools
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Update NGINX configuration
COPY ./nginx/nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
COPY ./nginx/entrypoint.sh /etc/entrypoint.sh
RUN chmod u+x /etc/entrypoint.sh

# Make sure PHP-FPM listens to the same port as which NGINX proxies requests.
COPY nginx/www.conf /etc/php/7.4/fpm/pool.d/

# Create project directory
WORKDIR /var/www/project
COPY ./laravelproject /var/www/project
RUN chown -R www-data:www-data /var/www

# Update routing
COPY ./web.php /var/www/project/routes/
COPY ./VerifyCsrfToken.php /var/www/project/app/Http/Middleware/

# Install project dependencies
COPY ./nginx/composer.json var/www/project/
RUN composer install

# Start NGINX server and PHP-FPM
COPY ./nginx/custom-php-fpm.conf /etc/php/7.4/fpm/pool.d/custom-php-fpm.conf/
ENTRYPOINT ["/etc/entrypoint.sh"]

# Open port used for request input
EXPOSE 8080
