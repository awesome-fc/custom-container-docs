# Running custom containers on Function Compute
Clone the repo to local workspace

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/php-topthink
```

## Create a ThinkPHP project
```bash
# Create a topthink/think project locally under php-topthink/
composer create-project topthink/think thinkproject
````

## Option 1: Build and push using Docker only

```bash
export FC_DEMO_IMAGE="your ACR image name"  # e.g. registry.cn-shanghai.aliyuncs.com/namespace/thinkphp:tag
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

docker push $FC_DEMO_IMAGE

# Configure FC using console or command line tool
```

## Option 2 (Recommended): Build and deploy using Funcraft

```bash
# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shanghai.aliyuncs.com/{your-namespace}/thinkphp:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Build the Docker image
fun build --use-docker

# Docker login before pushing, replace {your-ACR-registry} with, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# After a successful deploy, fun should return a HTTP proxy URL to invoke the function
curl https://{your-account-id}.{region}.fc.aliyuncs.com -H "x-fc-invocation-target: 2016-08-15/proxy/ThinkPHPCustomContainer/thinkphp-http"
curl -X POST  https://1573869909382650.cn-shanghai.fc.aliyuncs.com/header/host -H "x-fc-invocation-target: 2016-08-15/proxy/ThinkPHPCustomContainer/thinkphp-http"
```

## Developing with source code or adding dependencies
* Check and modify server.go

## Local development and debugging
This demo can run locally using docker to test both HTTP and Event functions.

### Event functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shanghai.aliyuncs.com/namespace/thinkphp:tag
docker run -p 9000:9000 $FC_DEMO_IMAGE

# Invoke handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/invoke

# Initializer handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/initialize
```

### HTTP functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shanghai.aliyuncs.com/namespace/thinkphp:tag
docker run -p 9000:9000 $FC_DEMO_IMAGE

curl localhost:9000/
curl -X POST localhost:9000/
```
