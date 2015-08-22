#!/usr/bin/ python

setup:
	python setup.py install

devenv:
	rm -rf venv
	virtualenv venv
	venv/bin/pip install -r requirement.pip
	venv/bin/python setup.py install
	echo "please activate '. venv/bin/activate'"
