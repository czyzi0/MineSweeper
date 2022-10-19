SHELL := /bin/bash

BIN_NAME := minesweeper

PYTHON := python3.8
PYINSTALLER_VERSION := 5.5


$(BIN_NAME): minesweeper.py
	$(PYTHON) -m venv .venv
	source .venv/bin/activate && $(PYTHON) -m pip install pyinstaller==$(PYINSTALLER_VERSION) && deactivate
	source .venv/bin/activate && pyinstaller --onefile --distpath . --specpath ./build $^ && deactivate
	rm -rf .venv

clean:
	rm -rf build/ .venv/ $(BIN_NAME)

.PHONY: clean
