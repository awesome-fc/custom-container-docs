# A ThinkPHP (top-think) web application running on FC with custom-container runtime

## Setup

```bash
# Clone this repo to local workspace
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/php-topthink

# Create a topthink/think project locally
composer create-project topthink/think thinkproject

# Set FC_DEMO_IMAGE to your desired ACR image name,
# e.g., registry.cn-shanghai.aliyuncs.com/{your-namespace}/php-topthink:v1
export FC_DEMO_IMAGE={your_image_name}

# Set FC_ACCOUNT to your Alibaba Cloud Account ID
export FC_ACCOUNT={your_account_id}

# Set region to the same as of your image, e.g., cn-shanghai
export region={region}

# Build image
docker build -t $FC_DEMO_IMAGE .

# Substitute {FC_DEMO_IMAGE} and {FC_ACCOUNT} in s.yaml
./setup.sh

# Before deploying, Docker login to your ACR registry, e.g., registry.cn-shanghai.aliyuncs.com
docker login registry.${region}.aliyuncs.com
```

## Deploy
### Option 1 (Recommended): Build and deploy only using Serverless Devs

```bash
# Deploying FC function automatically pushes image to your ACR repository
s deploy
```

### Option 2: Push image to ACR before deploying

```bash
# Push to your ACR repository
docker push $FC_DEMO_IMAGE

# Deploy FC function
s deploy --skip-push

```

## Before testing, wait until acceleration image is ready (Usually less than 1 min)

```bash
s cli fc-api getFunction --serviceName PHPTopthinkCustomContainer --functionName php-topthink --region ${region}
```

### Expected response
```yaml
...
CustomContainerConfig:
    ...
    # Make sure accelerationInfo.status is Ready
    accelerationInfo:
        status: Ready
        ...
```


## Test HTTP Trigger

```bash
curl https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com -H "x-fc-invocation-target: 2016-08-15/proxy/PHPTopthinkCustomContainer/php-topthink"

curl -X POST  https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com/header/host -H "x-fc-invocation-target: 2016-08-15/proxy/PHPTopthinkCustomContainer/php-topthink"
```

## Test Event Function

``` bash
curl -X POST https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com/initialize -H "x-fc-invocation-target: 2016-08-15/proxy/PHPTopthinkCustomContainer/php-topthink"

curl -X POST https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com/invoke -H "x-fc-invocation-target: 2016-08-15/proxy/PHPTopthinkCustomContainer/php-topthink"
```