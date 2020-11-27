.PHONY: clean build lint install test

default: test

venv_directory = ./venv

clean:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info
	@rm -rf src/*.egg-info
	@rm -rf $(venv_directory)/
	@rm -rf .eggs/
	@rm -rf .pytest_cache/
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete

prep: $(venv_directory)

$(venv_directory):
	@python3 -m venv venv
	$(venv_directory)/bin/pip install --upgrade pip
	$(venv_directory)/bin/pip install flake8
	@$(venv_directory)/bin/python3 setup.py install

lint:
	@$(venv_directory)/bin/flake8

test: prep lint
	@python3 setup.py test
	@$(venv_directory)/bin/python3 -m src.spoonbill render --template-dir example-data/ --inline-config '{"description":"I am the description", "canonical_relative_path":"/fake/site/index.html","classifications":[{"name":"Fruit","sort_order":1,"tag":"fruit"},{"name":"Meats","sort_order":2,"tag":"meats"},{"name":"Dairy","sort_order":3,"tag":"dairy"},{"name":"Vegetables","sort_order":4,"tag":"vegetables"}],"categories":[{"name":"Canned","sort_order":1,"tag":"canned"},{"name":"Boxed","sort_order":2,"tag":"boxed"},{"name":"Bagged","sort_order":3,"tag":"bagged"},{"name":"Fresh","sort_order":4,"tag":"fresh"}]}' example-data/example1.md > /dev/null
	@$(venv_directory)/bin/python3 -m src.spoonbill render --template-dir example-data/ --inline-config '{"description":"I am the description", "canonical_relative_path":"/fake/site/index.html","classifications":[{"name":"Fruit","sort_order":1,"tag":"fruit"},{"name":"Meats","sort_order":2,"tag":"meats"},{"name":"Dairy","sort_order":3,"tag":"dairy"},{"name":"Vegetables","sort_order":4,"tag":"vegetables"}],"categories":[{"name":"Canned","sort_order":1,"tag":"canned"},{"name":"Boxed","sort_order":2,"tag":"boxed"},{"name":"Bagged","sort_order":3,"tag":"bagged"},{"name":"Fresh","sort_order":4,"tag":"fresh"}]}' example-data/example2.md > /dev/null
	@$(venv_directory)/bin/python3 -m src.spoonbill render --template-dir example-data/ --inline-config '{"description":"I am the description", "canonical_relative_path":"/fake/site/index.html","classifications":[{"name":"Fruit","sort_order":1,"tag":"fruit"},{"name":"Meats","sort_order":2,"tag":"meats"},{"name":"Dairy","sort_order":3,"tag":"dairy"},{"name":"Vegetables","sort_order":4,"tag":"vegetables"}],"categories":[{"name":"Canned","sort_order":1,"tag":"canned"},{"name":"Boxed","sort_order":2,"tag":"boxed"},{"name":"Bagged","sort_order":3,"tag":"bagged"},{"name":"Fresh","sort_order":4,"tag":"fresh"}]}' example-data/example3.md > /dev/null
	@$(venv_directory)/bin/python3 -m src.spoonbill render --template-dir example-data/ --inline-config '{"description":"I am the description", "canonical_relative_path":"/fake/site/index.html","classifications":[{"name":"Fruit","sort_order":1,"tag":"fruit"},{"name":"Meats","sort_order":2,"tag":"meats"},{"name":"Dairy","sort_order":3,"tag":"dairy"},{"name":"Vegetables","sort_order":4,"tag":"vegetables"}],"categories":[{"name":"Canned","sort_order":1,"tag":"canned"},{"name":"Boxed","sort_order":2,"tag":"boxed"},{"name":"Bagged","sort_order":3,"tag":"bagged"},{"name":"Fresh","sort_order":4,"tag":"fresh"}]}' example-data/example4.md > /dev/null

	@$(venv_directory)/bin/python3 -m src.spoonbill render --template-dir example-data/ --inline-config '{"description":"I am the description", canonical_relative_path":"/fake/site/index.html","classifications":[{"name":"Fruit","sort_order":1,"tag":"fruit"},{"name":"Meats","sort_order":2,"tag":"meats"},{"name":"Dairy","sort_order":3,"tag":"dairy"},{"name":"Vegetables","sort_order":4,"tag":"vegetables"}],"categories":[{"name":"Canned","sort_order":1,"tag":"canned"},{"name":"Boxed","sort_order":2,"tag":"boxed"},{"name":"Bagged","sort_order":3,"tag":"bagged"},{"name":"Fresh","sort_order":4,"tag":"fresh"}]}' example-data/example4.md | $(venv_directory)/bin/python3 -m src.spoonbill pack - > /dev/null

build: prep
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
