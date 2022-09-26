SHELL:=/bin/bash

.DEFAULT_GOAL := help
# ---
# Variables
# ---
PROJECT_PATH := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
GIT_REMOTE=$(shell basename $(shell git remote get-url origin))
PROJECT_NAME=$(shell echo $(GIT_REMOTE:.git=))

DOCKER_IMAGE_NAME=hsteinshiromoto/${PROJECT_NAME}

BUILD_DATE = $(shell date +%Y%m%d-%H:%M:%S)

BASE_IMAGE_TAG=$(shell git ls-files -s Dockerfile.base | awk '{print $$2}' | cut -c1-16)
DOCKER_TAG=$(shell git ls-files -s Dockerfile.app | awk '{print $$2}' | cut -c1-16)

# ---
# Targets
# ---

# Refences:
#	[1] https://www.cross-validated.com/Personal-website-with-Minimal-Mistakes-Jekyll-Theme-HOWTO-Part-I/

## Builds base and app Docker images
image: base_image app_image

## Build base Docker image
base_image:
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}.base:${BASE_IMAGE_TAG})

	@echo "Building docker image ${DOCKER_IMAGE_TAG}"
	docker build -f Dockerfile.base -t ${DOCKER_IMAGE_TAG} .
	@echo "Done"

	docker run --volume="$(PWD):/usr/src/app" -it ${DOCKER_IMAGE_TAG} bundle install

## Build application Docker image
app_image:
	$(eval DOCKER_PARENT_IMAGE=${DOCKER_IMAGE_NAME}.base:${BASE_IMAGE_TAG})
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}:${DOCKER_TAG})

	@echo "Building docker image ${DOCKER_IMAGE_TAG}"
	docker build -f Dockerfile.app -t ${DOCKER_IMAGE_TAG} .
	@echo "Done"

## Run container based on application image
run:
	$(eval DOCKER_PARENT_IMAGE=${DOCKER_IMAGE_NAME}.base:${BASE_IMAGE_TAG})
	$(eval DOCKER_IMAGE_TAG=${DOCKER_IMAGE_NAME}:${DOCKER_TAG})

	 docker run --volume="$(PWD):/usr/src/app" -p 4000:4000 -t ${DOCKER_IMAGE_TAG}

# ---
# Self Documenting Commands
# ---

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>

help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
