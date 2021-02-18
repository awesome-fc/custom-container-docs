## Tensorflow serving running on FC with custom-container runtime
This example is based on the official [tensorflow/serving](https://www.tensorflow.org/tfx/serving/docker) image with provided Funcraft template to deploy the image to FC. After a deployment is successful, one can make prediction with HTTP requests.

## Build and deploy using Funcraft

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/tensorflow-serving

# Set FC_DEMO_IMAGE to your ACR image, e.g. registry-vpc.cn-beijing.aliyuncs.com/{your-namespace}/tensorflow-serving:v1
export FC_DEMO_IMAGE={your_image}

# Substitute {FC_DEMO_IMAGE} in template.yml
./setup.sh

# Configure funcraft, make sure the container registry and fun are in the same region, skip this step if fun is already configured.
fun config

# Build the Docker image
fun build --use-docker

# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# After a successful deploy, make a prediction, note the header "x-fc-invocation-target: 2016-08-15/proxy/CustomContainerDemo/tensorflow-serving-http" should match the service/function name
curl -X POST -H "x-fc-invocation-target: 2016-08-15/proxy/CustomContainerDemo/tensorflow-serving-http" htps://$ACCOUNT_ID.$REGION.fc.aliyuncs.com/v1/models/half_plus_two:predict  -d '{"instances": [1.0, 2.0, 5.0]}'
```

## Local testing
This demo can also be ran and invoked locally with docker.

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set
docker run -t --rm -e MODEL_NAME=half_plus_two -p 8501:8501 $FC_DEMO_IMAGE

# Make a prediction, expecting the following output
curl -X POST http://localhost:8501/v1/models/half_plus_two:predict -d '{"instances": [1.0, 2.0, 5.0]}'

# {
#    "predictions": [2.5, 3.0, 4.5
#    ]
# }
```