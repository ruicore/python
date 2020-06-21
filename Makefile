
req:
	pip freeze > requirements.txt
in-pre:
	pre-commit install
pre:
	pre-commit run --all-files
up-pre:
	pre-commit autoupdate
