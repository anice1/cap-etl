SHELL = /bin/bash

# Environment
.PHONY: setup
setup:
	python3 -m venv ~/cosmo-etl && \
	source ~/cosmo-etl/bin/activate && \
	pip3 install -r requirements.txt && \
	cp config.ini.example config.ini

# Cleaning
.PHONY: clean
clean: 
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".trash" | xargs rm -rf
	find . | grep -E ".vscode" | xargs rm -rf
	rm -f .coverage
	black .
	clear