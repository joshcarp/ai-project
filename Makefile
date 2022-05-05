all:
	python3.8 -m autopep8 --in-place --recursive .
	python3.8 -m flake8
	python3.8 -m pytest

pdf:
	md-to-pdf README.md
