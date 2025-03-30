
ifeq ($(OS),Windows_NT)
    # Windows
    PY_NAME := py
else
    # Linux, macOS
    PY_NAME := python3
endif

.PHONY: app freeze build

app:
	poetry run $(PY_NAME) main.py

freeze:
	pip freeze > requirements.txt

build:
	poetry run pyinstaller --noconfirm --onefile --windowed --add-data "src/template/template.html;template" --icon="img/volgau_gerb.ico" main.py
