.PHONY: docker-build deploy

docker-build:
	docker build -t registry.us-west-1.aliyuncs.com/fc-demo-1-3/forrest-ai-demo-model-deploy-prod:v1 .

deploy: docker-build
	fun deploy -y --push-registry acr-internet