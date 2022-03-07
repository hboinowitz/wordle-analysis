VENV_NAME?=.venv
PATH_TO_ACTIVATE = $(VENV_NAME)/bin/activate

create_venv:
	python3 -m venv $(VENV_NAME)

install: create_venv requirements.txt
	(. $(PATH_TO_ACTIVATE) && pip3 install -e .)

run-demo:
	(. $(PATH_TO_ACTIVATE) && cd demo && export FLASK_ENV=development && flask run)