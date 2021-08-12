## Python Flask running on FC with custom-container runtime

There are two functions to be built and deployed in this demo, one of them is an `Event function` and the other is a `HTTP function`. Please see the source code and comments for more details.

```bash
git clone https://github.com/awesome-fc/custom-container-docs.git
cd custom-container-docs/python-flask
```

### Recommended: build and deploy using Funcraft

# change template.yml Image

直接手动手改 template.yml, image 改成自己 acr 的镜像, 比如我先在 acr 仓库里面创建一个这样的仓库

![](https://img.alicdn.com/imgextra/i3/O1CN01Fw6TyH1a87NclFCIK_!!6000000003284-2-tps-970-543.png)

```bash
# 已经配置过， 不需要执行
# Configure funcraft, make sure the container registry and fun are in the same region, skip this step if fun is already configured.
fun config

# Build the Docker image
fun build --use-docker

# 第一次可能需要 docker login 下, 比如:
# docker login --username=fc-demo registry.cn-hangzhou.aliyuncs.com
# Deploy the function, push the image via the internet registry host (the function config uses the VPC registry for faster image pulling)
fun deploy --push-registry acr-internet

# Invoke function
fun invoke -e '{"key":"val"}'
```

## Developing with source code or adding dependencies

- Check and modify app.py
- Add dependencies in requirements.txt
- Re-run above image build and deploy steps after making changes.

## Local development and debugging

This demo can also be ran locally with docker for both HTTP and Event functions.

### Event functions

```bash
# Run the image, make sure FC_DEMO_IMAGE is already set, e.g. registry.cn-shenzhen.aliyuncs.com/fc-demo/python-flask:v0.1
docker run -p 9000:9000 $FC_DEMO_IMAGE

# Invoke handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/invoke -d '{"hello":"FC"}'

# Initializer handler
curl -X POST -H "x-fc-request-id: test-request-1" localhost:9000/initialize
```

### 修改代码， 更新函数

修改 app.py 相关的代码， 然后修改 template.yml Image, 比如从 v1 改成 v2, 然后 `fun deploy --push-registry acr-internet` 即可
