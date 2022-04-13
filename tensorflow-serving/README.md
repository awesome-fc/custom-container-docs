
## Tensorflow server running on FC with custom-container runtime
This example is based on the official [tensorflow/serving](https://www.tensorflow.org/tfx/serving/docker) image with provided Serverless Devs template to deploy to FC.

## Setup

```bash
# Clone this repo to local workspace
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/tensorflow-serving

# Set FC_DEMO_IMAGE to your desired ACR image name,
# e.g., registry.cn-shanghai.aliyuncs.com/{your-namespace}/tensorflow:v1
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
s cli fc-api getFunction --serviceName TensorflowCustomContainer --functionName tensorflow --region ${region}
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


## Test

```bash
curl -X POST -H "x-fc-invocation-target: 2016-08-15/proxy/TensorflowCustomContainer/tensorflow" https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com/v1/models/half_plus_two:predict  -d '{"instances": [1.0, 2.0, 5.0]}'

# {
#    "predictions": [2.5, 3.0, 4.5
#    ]
# }
```