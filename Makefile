PYTHON		= python3
VERSION_TXT	= VERSION
VERSION		= $(shell cat $(VERSION_TXT))

versionis:
	@echo "Version is" $(VERSION)

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name __pycache__ -delete

build:
	$(PYTHON) setup.py bdist_wheel
