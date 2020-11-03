## Java Spring Boot running on FC with custom-container runtime
This demo is based on the [official document](https://spring.io/guides/gs/spring-boot-docker/) with required changes to containerize a Spring Boot web application.

## Build and deploy custom-container functions
There are two functions to be built and deployed in this demo, one of them is an `Event function` and the other is a `HTTP function`. Please see the source code and comments for more details.

### Option 1: Build and push using Docker only

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd java-springboot

export FC_DEMO_IMAGE={your_image}
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shenzhen.aliyuncs.com
docker login {your-ACR-registry}

# Push the image
docker push $FC_DEMO_IMAGE

# Local test
docker run -p 8080:8080 registry.cn-shenzhen.aliyuncs.com/fc-demo/java-spring-boot:v0.1
curl localhost:8080/2016-08-15/proxy/CustomContainerDemo/java-springboot-http/

# Deploy the image with Alibaba Cloud FC console or Funcraft command line tool
fun deploy
```

### Option 2 (Recommended): build and deploy using Funcraft

```bash
# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shenzhen.aliyuncs.com/{your-namespace}/fc-demo-java-spring-boot:v1
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
curl https://{your-account-id}.cn-shenzhen.fc.aliyuncs.com/2016-08-15/proxy/CustomContainerDemo/java-springboot-http/

```

## Developing with source code or adding dependencies
* Souce code is located at `src` dir, demo source code file is at `src/main/java/hello/Application.java`.
* Dependencies can be add in pom.xml.
* Re-run above image build and deploy steps after making changes.

## Local development and debugging
This demo can also be ran locally with docker for both HTTP and Event functions.

### Event functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/java-spring-boot:v0.1
docker run --user 10003 -p 8080:8080 $FC_DEMO_IMAGE

# Invoke handler
curl -X POST -H "Content-Type:application/json" localhost:8080/invoke -d '{"hello":"FC"}'

# Initializer handler
curl -X POST -H "Content-Type:application/json" localhost:8080/initialize -d '{"hello":"FC"}'
```

### HTTP functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/java-spring-boot:v0.1
docker run --user 10003 -p 8080:8080 $FC_DEMO_IMAGE

curl localhost:8080/2016-08-15/proxy/CustomContainerDemo/java-springboot-http/
```
