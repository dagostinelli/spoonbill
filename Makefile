.PHONY: clean build lint install

default: test

clean:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf src/*.egg-info
	@rm -rf venv/
	@rm -rf .eggs/
	@rm -rf .pytest_cache/
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete

lint:
	@flake8

test:
	@python3 setup.py test

build:
	@python3 setup.py sdist
	@python3 setup.py bdist
	@python3 setup.py bdist_wheel

install-pipsi: build
	@pip uninstall spoonbill --yes
	@pip install spoonbill --user

dev-run:
	@echo Do this
	@echo python3 -m venv venv
	@echo source venv/bin/activate
	@echo python3 setup.py install
	@echo python3 -m src.spoonbill
	@echo deactivate
