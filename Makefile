VENV=$(CURDIR)/.venv

.PHONY: all pull_data setup_dependencies docker notebook

all: notebook

$(VENV):
	python3 -m venv $(VENV)

$(VENV)/bin/jupyter-notebook: $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $(VENV)/bin/jupyter-notebook

notebook: $(VENV)/bin/jupyter-notebook pull_data
	$(VENV)/bin/jupyter-notebook

docker:
	docker build -t ratt-ru/fundamentals_of_interferometry .
