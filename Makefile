


test:
	python setup.py test

autopep8:
	autopep8 . --recursive --in-place --pep8-passes 2000 --verbose
