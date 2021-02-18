## Nodejs Express and Puppeteer to print web pages as PDFs, running on FC with custom-container runtime
This example is based on [christopher-talke/node-express-puppeteer-pdf-example](https://github.com/christopher-talke/node-express-puppeteer-pdf-example) along with minor tweaks and Alibaba Cloud FunctionCompute deployment templates. This demo illustrates the image acceleration feature. It deploys the same image as two functions, one with acceleration enabled (`AccelerationType: Default`) and another disabled (`AccelerationType: None`).

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/puppeteer-pdf
```

### Option 1: Build and push using Docker only

```bash
# Set FC_DEMO_IMAGE to your image in ACR, e.g. registry-vpc.cn-beijing.aliyuncs.com/{your-namespace}/fc-demo-puppeteer-pdf:v1
export FC_DEMO_IMAGE={your_image}

# Build the image
docker build -t $FC_DEMO_IMAGE .

# Docker login before pushing, replace {your-ACR-registry}, e.g. registry.cn-beijing.aliyuncs.com
docker login {your-ACR-registry}

# Push the image
docker push $FC_DEMO_IMAGE

# Local test
docker run --rm -p 3000:3000 $FC_DEMO_IMAGE
curl http://localhost:3000/generate-pdf?url=http://example.com -o /tmp/fc-demo-puppeteer-pdf.pdf

# Deploy the image with Alibaba Cloud FC console or Funcraft command line tool
fun deploy
```

### Option 2 (Recommended): build and deploy using Funcraft
```bash

# Set FC_DEMO_IMAGE to your image in ACR, e.g. registry-vpc.cn-beijing.aliyuncs.com/{your-namespace}/fc-demo-puppeteer-pdf:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Configure funcraft, make sure the container registry and fun are in the same region, skip this step if fun is already configured.
fun config

# Build the Docker image
fun build --use-docker

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet
```

## Testing the acceleration
After a successful deploy, make a http request to print a web page to a PDF

```bash
export ACCOUNT_ID={your-account-id}
export REGION={region} # e.g. cn-beijing

# Invoke WITHOUT image acceleration
time curl -H "x-fc-invocation-target: 2016-08-15/proxy/CustomContainerDemo/puppeteer-pdf-no-accl" https://$ACCOUNT_ID.$REGION.fc.aliyuncs.com/generate-pdf?url=http://example.com -o /tmp/fc-demo-puppeteer-pdf-no-accl.pdf

# Invoke WITH image acceleration
time curl -H "x-fc-invocation-target: 2016-08-15/proxy/CustomContainerDemo/puppeteer-pdf-accl" https://$ACCOUNT_ID.$REGION.fc.aliyuncs.com/generate-pdf?url=http://example.com -o /tmp/fc-demo-puppeteer-pdf-accl.pdf

# Acceleration disabled: 66.5s vs. Acceleration enabled: 15.2s, cold start performance improved by 77.1%.
```