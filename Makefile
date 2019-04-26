PYTHON	= python3
MODULE	= otp
VERSION	= $(shell awk '{print $$3}' ${MODULE}/_version.py | tr -d "'")

.PHONY: clean bdist sdist install release publish

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name __pycache__ -delete

bdist:
	$(PYTHON) setup.py bdist

sdist:
	$(PYTHON) setup.py sdist

install:
	$(PYTHON) setup.py install

release:
	git tag -s $(VERSION) -m "$(VERSION)"
	$(PYTHON) setup.py check sdist
	git push origin master --tags

deploy:
	#twine upload dist/*
