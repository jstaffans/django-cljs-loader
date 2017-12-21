.PHONY: clean build deploy install check-env publish help

# Project settings
PROJECT = cljs-loader

REPOSITORY ?= test-pypi

requirements = -r requirements.txt

all: help

clean:  ## Clean
	@echo "Cleaning..."
	@find cljs_loader/ -name '*.pyc' -delete
	@rm -rf ./build ./*egg* ./dist

test: install  ## Run tests
	@cd tests && python manage.py test

build: install clean  ## Build for PyPi upload
	@echo "Building..."
	@python setup.py sdist bdist_wheel --universal

check-env:
ifndef VIRTUAL_ENV
	$(error VIRTUAL_ENV is undefined)
endif

install: check-env  ## Install build dependencies (prerequisite for build)
	@echo "Installing build dependencies"
	@pip install $(requirements)

generate-rst:  ## Use pandoc to generate .rst file
	@pandoc --from=markdown --to=rst --output=README.rst README.md

publish: generate-rst build  ##
	@echo "Publishing to pypi..."
	@twine upload -r $(REPOSITORY) dist/*

register: ##
	@echo "Registering package on pypi..."
	@twine register -r $(REPOSITORY)

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'
