
all: build run

build:
	docker build . -t my-whylogs-contianer

run:
	docker run -it --net=host --env-file local.env my-whylogs-contianer


pyspy: ## Run profiler on the dev server
	sudo env "PATH=$(PATH)" py-spy record -o profile2.svg --pid $(PID)
