all:
	autopep8 --in-place --recursive .
	flake8
	pytest