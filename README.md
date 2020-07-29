# Running custom containers on Function Compute

## Option 1: Build and deploy using Funcraft
* Note: Replace `YOUR_ACR_IMAGE` in template.yml

```bash
fun deploy --use-docker
```

## Option 2: Build and push using Docker only

```bash
export IMAGE_NAMESPACE="your image namespace"

docker build -t registry.{region}.aliyuncs.com/$IMAGE_NAMESPACE/fc-custom-container-demo:v1beta1 .
docker push registry.{region}.aliyuncs.com/$IMAGE_NAMESPACE/fc-custom-container-demo:v1beta1
```