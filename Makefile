# These can be overidden with env vars.
REGISTRY ?= us.icr.io
NAMESPACE ?= nyu-devops
IMAGE_NAME ?= wishlists-summer23
IMAGE_TAG ?= 1.0
IMAGE ?= $(REGISTRY)/$(NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)
PLATFORM ?= "linux/amd64"
CLUSTER ?= nyu-devops
SPACE ?= dev

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-\\.]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: all
all: help

##@ Development

.PHONY: clean
clean:	## Removes all dangling docker images
	$(info Removing all dangling docker images..)
	docker image prune -f

.PHONY: venv
venv: ## Create a Python virtual environment
	$(info Creating Python 3 virtual environment...)
	python3 -m venv .venv

.PHONY: install
install: ## Install dependencies
	$(info Installing dependencies...)
	sudo python3 -m pip install --upgrade pip wheel
	sudo pip install -r requirements.txt

.PHONY: lint
lint: ## Run the linter
	$(info Running linting...)
	flake8 service tests --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 service tests --count --max-complexity=10 --max-line-length=127 --statistics
	pylint service tests --max-line-length=127

.PHONY: tests
test: ## Run the unit tests
	$(info Running tests...)
	green -vvv --processes=1 --run-coverage --termcolor --minimum-coverage=95

.PHONY: run
run: ## Run the service
	$(info Starting service...)
	honcho start

.PHONY: namespace
namespace: ## Create the namespace assigned to the SPACE env variable
	$(info Creatng the $(SPACE) namespace...)
	kubectl create namespace $(SPACE) 
	kubectl get secret all-icr-io -n default -o yaml | sed 's/default/$(SPACE)/g' | kubectl create -n $(SPACE) -f -
	kubectl config set-context --current --namespace $(SPACE)

############################################################
# COMMANDS FOR DEPLOYING THE IMAGE
############################################################

##@ Deployment

.PHONY: login
login: ## Login to IBM Cloud using yur api key
	$(info Logging into IBM Cloud cluster $(CLUSTER)...)
	ibmcloud login -a cloud.ibm.com -g Default -r us-south --apikey @~/.bluemix/apikey.json
	ibmcloud cr login
	ibmcloud ks cluster config --cluster $(CLUSTER)
	ibmcloud ks workers --cluster $(CLUSTER)
	kubectl cluster-info

.PHONY: push
image-push: ## Push to a Docker image registry
	$(info Logging into IBM Cloud cluster $(CLUSTER)...)
	ibmcloud cr login
	docker push $(IMAGE)

.PHONY: deploy
depoy: ## Deploy the service on local Kubernetes
	$(info Deploying service locally...)
	kubectl apply -f deploy/

############################################################
# COMMANDS FOR BUILDING THE IMAGE
############################################################

##@ Docker Build

.PHONY: init
init: export DOCKER_BUILDKIT=1
init:	## Creates the buildx instance
	$(info Initializing Builder...)
	docker buildx create --use --name=qemu
	docker buildx inspect --bootstrap

.PHONY: build
build:	## Build all of the project Docker images
	$(info Building $(IMAGE) for $(PLATFORM)...)
	docker buildx build --file Dockerfile  --pull --platform=$(PLATFORM) --tag $(IMAGE) --load .

.PHONY: remove
remove:	## Stop and remove the buildx builder
	$(info Stopping and removing the builder image...)
	docker buildx stop
	docker buildx rm
