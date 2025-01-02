.PHONY: app freeze build

app:
	poetry run main.py

freeze:
	pip freeze > requirements.txt

build:
	poetry run pyinstaller --noconfirm --onefile --windowed --add-data "src/template/template.html;template" --icon="img/volgau_gerb.ico" main.py
