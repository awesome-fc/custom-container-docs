# Running custom containers on Function Compute

## Option 1: Build and push using Docker only

```bash
export FC_DEMO_IMAGE="your ACR image name"  # e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/nodejs-express:v0.2
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shenzhen.aliyuncs.com
docker login {your-ACR-registry}

docker push $FC_DEMO_IMAGE

# Deploy the function without pushing the image to ACR
fun deploy
```

## Option 2 (Recommended): Build and deploy using Funcraft

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd nodejs-express

# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shenzhen.aliyuncs.com/{your-namespace}/fc-demo-java-spring-boot:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Build the Docker image
fun build --use-docker

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shenzhen.aliyuncs.com
docker login {your-ACR-registry}

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet
```


