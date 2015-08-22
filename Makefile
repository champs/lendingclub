# prep dev env
setup:
	python setup.py install

devenv:
	rm -rf venv
	virtualenv venv
	venv/bin/pip install -r requirement.pip
	python setup.py install

