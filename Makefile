lint:
	flake8 bandsintown tests

test:
	py.test --cov bandsintown -s -rxs ./tests/ --cov-fail-under 80

.PHONY: lint test
