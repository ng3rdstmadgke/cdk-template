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

.PHONY: generate-classdiagram
generate-classdiagram: ## : クラス図の出力 (https://qiita.com/kenichi-hamaguchi/items/c0b947ed15725bfdfb5a)
	pyreverse -o png -d ./doc/image --colorized --max-color-depth=3 -p cdk .
