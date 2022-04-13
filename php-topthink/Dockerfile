FROM topthink/php:7.4

# Install dependencies
RUN apt-get update -y

# Create project directory
WORKDIR /usr/src/app
COPY ./thinkproject /usr/src/app

# Update routing
COPY ./app.php /usr/src/app/route/

# Start NGINX server and PHP-FPM
CMD php think run --host=0.0.0.0 --port=9000

# Open port used for request input
EXPOSE 9000
