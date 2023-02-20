
all: build run

build:
	docker build . -t my-whylogs-contianer

run:
	docker run -it --net=host --env-file local.env my-whylogs-contianer
