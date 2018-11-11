.PHONY: test install

python = /usr/bin/env python 
pip = /usr/bin/env pip 

install: 
	$(pip) install .

test: 
	$(python) -m unittest discover test "*_test.py"
