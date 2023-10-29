
# Comandos
PYTHON = python3
PIP = pip

# Nome do ambiente virtual
VENV_NAME = venv

install:
	$(PYTHON) -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

clean:
	rm -rf $(VENV_NAME)

.PHONY: install run clean
