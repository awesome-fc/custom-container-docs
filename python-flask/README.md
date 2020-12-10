## Python Flask running on FC with custom-container runtime
There are two functions to be built and deployed in this demo, one of them is an `Event function` and the other is a `HTTP function`. Please see the source code and comments for more details.

### Option 1: Build and push using Docker only

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd python-flask

# Set FC_DEMO_IMAGE to your ACR image, e.g. registry.cn-shenzhen.aliyuncs.com/{your-namespace}/fc-demo-python-flask:v1
export FC_DEMO_IMAGE={your_image}
docker build -t $FC_DEMO_IMAGE .

# Local test
docker run -p 9000:9000 $FC_DEMO_IMAGE
curl -X POST -H "x-fc-request-id: test-request-1" 0.0.0.0:9000/invoke -d '{"hello": "FC"}'

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shenzhen.aliyuncs.com
docker login {your-ACR-registry}

# Push the image
docker push $FC_DEMO_IMAGE

# Deploy the image with Alibaba Cloud FC console or Funcraft command line tool
```

### Option 2 (Recommended): build and deploy using Funcraft

```bash
# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shenzhen.aliyuncs.com/{your-namespace}/fc-demo-python-flask:v1
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
curl https://{your-account-id}.{region}.fc.aliyuncs.com/2016-08-15/proxy/CustomContainerDemo/python-flask-http/

```

## Developing with source code or adding dependencies
* Check and modify app.py 
* Add dependencies in requirements.txt
* Re-run above image build and deploy steps after making changes.

## Local development and debugging
This demo can also be ran locally with docker for both HTTP and Event functions.

### Event functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/python-flask:v0.1
docker run -p 9000:9000 $FC_DEMO_IMAGE

# Invoke handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/invoke -d '{"hello":"FC"}'

# Initializer handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/initialize
```

### HTTP functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/python-flask:v0.1
docker run -p 9000:9000 $FC_DEMO_IMAGE

curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/2016-08-15/proxy/CustomContainerDemo/python-flask-http/ -d '{"hello":"FC"}'
```