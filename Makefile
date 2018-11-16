.PHONY: test install install-dev install-all coverage

python = /usr/bin/env python 
pip = /usr/bin/env pip 
test_params = -m unittest discover test "*_test.py"

install: 
	$(pip) install .

install-dev: 
	$(pip) install -e .[dev]

install-all: install install-dev

test: 
	$(python) $(test_params)

coverage:
	coverage run $(test_params) && coverage html
