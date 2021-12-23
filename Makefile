STAGE := dev
CDK_IMAGE_NAME := sample-cdk

.DEFAULT_GOAL := help
.PHONY: help

echo:
	echo $(SLS_IMAGE_NAME)

help:
	@echo "Makefile Options:"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	| column -t  -s ' '

.PHONY: prepare
prepare: ## : CDKコンテナのビルド
	docker build --rm -f docker/Dockerfile -t $(CDK_IMAGE_NAME) .
