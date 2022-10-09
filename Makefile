.PHONY: help
help: default

.PHONY: default
default:
	@echo "Usage: make RULE"
	@echo ""
	@echo "Developer rules:"
	@echo "  init  - Install for development"
	@echo "  lint  - Run linters"
	@echo ""
	@echo "Maintainer rules:"
	@echo "  init-maint  - Install for development and maintainance"
	@echo "  build-reqs  - Re-generate requirements/*.txt"

PIP ?= python -m pip

.PHONY: init
init:
	${PIP} install --upgrade pip wheel
	${PIP} install --upgrade -r requirements/main.txt -r requirements/dev.txt
	${PIP} install --upgrade -e .
	${PIP} check

.PHONY: lint
lint:
	black .
	flake8 .
	mypy .

.PHONY: init-maint
init-maint:
	${PIP} install --upgrade pip wheel
	${PIP} install --upgrade -r requirements/main.txt -r requirements/dev.txt -r requirements/maint.txt
	${PIP} install --upgrade -e .
	${PIP} check

PIPTOOLS ?= python -m piptools
PIPTOOLS_COMPILE_OPTS ?= --quiet --generate-hashes
PIPTOOLS_COMPILE ?= CUSTOM_COMPILE_COMMAND="make build-reqs" ${PIPTOOLS} compile ${PIPTOOLS_COMPILE_OPTS}

.PHONY: build-reqs
build-reqs:
	${PIPTOOLS_COMPILE} -o requirements/main.txt pyproject.toml
	${PIPTOOLS_COMPILE} --extra dev -o requirements/dev.txt pyproject.toml
	${PIPTOOLS_COMPILE} --extra maint -o requirements/maint.txt pyproject.toml
