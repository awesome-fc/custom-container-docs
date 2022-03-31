FROM php:7.4-fpm

# Install dependencies
RUN apt-get update -y && apt-get install -y libmcrypt-dev openssl
RUN pecl install mcrypt-1.0.4 && docker-php-ext-enable mcrypt
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Create app directory
WORKDIR /usr/src/app
COPY ./laravelproject /usr/src/app

# Update routes
COPY ./web.php /usr/src/app/routes/
COPY ./VerifyCsrfToken.php /usr/src/app/app/Http/Middleware/

# Install project dependencies
RUN composer install

# Start server
CMD php artisan serve --host=0.0.0.0 --port=9000
EXPOSE 9000
