# Build automation for Smart URL Shortener (Python equivalent of `mvn clean package`)
PYTHON ?= python3
IMAGE  ?= smart-url-shortener
TAG    ?= v1

.PHONY: install test clean build docker-build run

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -v

clean:
	rm -rf dist build *.egg-info

# Produces dist/smart_url_shortener-1.0.0-py3-none-any.whl
build: clean
	$(PYTHON) -m build --wheel

docker-build:
	docker build -t $(IMAGE):$(TAG) .

run:
	$(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000
