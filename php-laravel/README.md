## PHP Laravel running on FC with custom-container runtime
There are two functions to be built and deployed in this demo, one of them is an `Event function` and the other is a `HTTP function`. Please see the source code and comments for more details.

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/php-laravel
```

### Option 1: Build and push using Docker only

```bash
# Create a laravel/laravel project locally under php-laravel/
composer create-project laravel/laravel laravelproject

# Move Dockerfile into project root
mv Dockerfile laravelproject/ && cd laravelproject

# Set FC_DEMO_IMAGE to your ACR image, e.g. registry.cn-shanghai.aliyuncs.com/{your-namespace}/php-laravel:v1
export FC_DEMO_IMAGE={your_image}
docker build -t $FC_DEMO_IMAGE .

# Local test
docker run -p 9000:9000 $FC_DEMO_IMAGE
# Event trigger
curl -X POST 0.0.0.0:9000/invoke
# HTTP trigger
curl http://0.0.0.0:9000/2016-08-15/proxy/CustomContainerDemo/php-laravel-http

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

# Push the image
docker push $FC_DEMO_IMAGE

# Deploy the image with Alibaba Cloud FC console or Funcraft command line tool
```

### Option 2 (Recommended): build and deploy using Funcraft

```bash
# Set FC_DEMO_IMAGE to your existent ACR image, could be the one from Option 1. For example, registry-vpc.cn-shanghai.aliyuncs.com/{your-namespace}/php-laravel:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Configure funcraft, make sure the container registry and fun are in the same region, skip this step if fun is already configured.
fun config

# Build the Docker image
fun build --use-docker

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# After a successful deploy, fun should return a HTTP proxy URL to invoke the function
curl https://{your-account-id}.{region}.fc.aliyuncs.com/2016-08-15/proxy/CustomContainerDemo/php-laravel-http/

```