# Running custom containers on Function Compute
Clone the repo to local workspace

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/go-gin
```

## Option 1: Build and push using Docker only

```bash
export FC_DEMO_IMAGE="your ACR image name"  # e.g. registry.cn-shanghai.aliyuncs.com/fnf-fc-demo/go-gin:latest
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

docker push $FC_DEMO_IMAGE

# Deploy the function without pushing the image to ACR
fun deploy
```

## Option 2 (Recommended): Build and deploy using Funcraft

```bash
# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shanghai.aliyuncs.com/{your-namespace}/go-gin:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Build the Docker image
fun build --use-docker

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# After a successful deploy, fun should return a HTTP proxy URL to invoke the function
curl https://{your-account-id}.{region}.fc.aliyuncs.com -H "x-fc-invocation-target: 2016-08-15/proxy/GoGinCustomContainer/go-gin-http"
```

## Developing with source code or adding dependencies
* Check and modify server.go 
* Add dependencies in go.mod
* Re-run above image build and deploy steps after making changes.

## Local development and debugging
This demo can also be ran locally with docker for both HTTP and Event functions.

### Event functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shanghai.aliyuncs.com/fnf-fc-demo/go-gin:v1
docker run -p 9000:9000 $FC_DEMO_IMAGE

# Invoke handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/invoke

# Initializer handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/initialize
```

### HTTP functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shanghai.aliyuncs.com/fnf-fc-demo/go-gin:v1
docker run -p 9000:9000 $FC_DEMO_IMAGE

curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000
```
