SHELL:=/bin/bash

image: base_image
	rm Gemfile.lock
	docker build -t ruby-environment .
	app_image

base_image:
	docker build -t ruby-environment .

app_image:
	docker build -f Dockerfile.app -t minimal-mistakes .

run:
	 docker run --volume="$(PWD):/usr/src/app" -P -t minimal-mistakes