SHELL := /bin/bash

PYTHON := python3.8
PYLINT_VERSION := 2.15.5
MYPY_VERSION := 0.982
PYINSTALLER_VERSION := 5.5


minesweeper: minesweeper.py src/*
	@echo "Creating virtual environment..." \
		&& $(PYTHON) -m venv venv
	@echo "Installing dependencies..." \
		&& source venv/bin/activate \
		&& $(PYTHON) -m pip install pylint==$(PYLINT_VERSION) \
		&& $(PYTHON) -m pip install mypy==$(MYPY_VERSION) \
		&& $(PYTHON) -m pip install pyinstaller==$(PYINSTALLER_VERSION) \
		&& deactivate
	@echo "Linting with pylint..." \
		&& source venv/bin/activate \
		&& $(PYTHON) -m pylint --exit-zero $< src/\
		&& deactivate
	@echo "Type checking with mypy..." \
		&& source venv/bin/activate \
		&& $(PYTHON) -m mypy $< src/ \
		&& deactivate
	@echo "Building with pyinstaller..." \
		&& source venv/bin/activate \
		&& pyinstaller --onefile --distpath . --specpath ./build $< \
		&& deactivate

clean:
	rm -rf build/ venv/ minesweeper

.PHONY: clean
