.PHONY: test build

test:
	poetry run coverage run -m pytest

build:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	docker build -t pg_pfmon:latest .