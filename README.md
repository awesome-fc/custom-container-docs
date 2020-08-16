# Running custom containers on Function Compute

## Option 1: Build and deploy using Funcraft
* Note: Replace `YOUR_ACR_IMAGE` in template.yml

```bash
# Build the Docker image
fun build --use-docker

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet
```

## Option 2: Build and push using Docker only

```bash
export IMAGE_NAME="your ACR image name"  # e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/nodejs-express:v0.2
docker build -t $IMAGE_NAME .
docker push $IMAGE_NAME

# Deploy the function without pushing the image to ACR
fun deploy
```
