
req:
	pip freeze > requirements.txt
in-pre:
	pre-commit install
pre:
	pre-commit run --all-files
up-pre:
	pre-commit autoupdate
up-pack:
	pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U
up-pip:
	pip install --upgrade pip