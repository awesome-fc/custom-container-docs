# Running custom containers on Function Compute
## - A weather forecast service
## Setup
Clone the repo to local workspace

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/asp-dotnet
```

## Deploy Service
### Option 1: Build and push using Docker

```bash
export FC_DEMO_IMAGE="your ACR image name"  # e.g. registry.cn-shanghai.aliyuncs.com/namespace/dotnet:v1
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

docker push $FC_DEMO_IMAGE

# Deploy the function without pushing the image to ACR
fun deploy
```

### Option 2 (Recommended): Build and deploy only using Funcraft

```bash
# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-shanghai.aliyuncs.com/{your-namespace}/dotnet:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Build the Docker image
fun build --use-docker

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-shanghai.aliyuncs.com
docker login {your-ACR-registry}

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# After a successful deploy, fun should return a HTTP proxy URL to invoke WeatherForecast function
curl https://{your-account-id}.{region}.fc.aliyuncs.com/WeatherForecast -H "x-fc-invocation-target: 2016-08-15/proxy/DotNetCustomContainer/weather-forecast"
```