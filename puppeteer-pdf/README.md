# Nodejs Express and Puppeteer to print web pages as PDFs, running on FC with custom-container runtime
This example is based on [christopher-talke/node-express-puppeteer-pdf-example](https://github.com/christopher-talke/node-express-puppeteer-pdf-example) with minor tweaks.

## Setup

```bash
# Clone this repo to local workspace
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/puppeteer-pdf

# Set FC_DEMO_IMAGE to your desired ACR image name,
# e.g., registry.cn-shanghai.aliyuncs.com/{your-namespace}/puppeteer-pdf:v1
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

## Before testing, wait until acceleration image is ready (Usually less than 5 minutes)

```bash
s cli fc-api getFunction --serviceName PuppeteerPDFCustomContainer --functionName puppeteer-pdf --region ${region}
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


## Test with example.com

```bash
curl -X POST https://${FC_ACCOUNT}.${region}.fc.aliyuncs.com/invoke -H "x-fc-invocation-target: 2016-08-15/proxy/PuppeteerPDFCustomContainer/puppeteer-pdf"  -o /tmp/puppeteer-pdf-invoke.pdf

# Open generated PDF
open /tmp/puppeteer-pdf-invoke.pdf
```

## Test with official custom-container document

``` bash
curl 'https://'${FC_ACCOUNT}'.'${region}'.fc.aliyuncs.com/generate-pdf?url=https://help.aliyun.com/document_detail/179368.html' -H "x-fc-invocation-target: 2016-08-15/proxy/PuppeteerPDFCustomContainer/puppeteer-pdf"  -o /tmp/puppeteer-pdf-aliyun.pdf

# Open generated PDF
open /tmp/puppeteer-pdf-aliyun.pdf
```