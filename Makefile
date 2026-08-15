ifeq ($(OS),Windows_NT)
    # Windows
    PY_NAME := py
else
    # Linux, macOS
    PY_NAME := python3
endif

.DEFAULT_GOAL := help
.PHONY: help app freeze build

help: ## Показать список целей
	@grep -hE '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

app: ## Запустить приложение
	poetry run $(PY_NAME) main.py

freeze: ## Пересобрать requirements.txt из активного окружения
	pip freeze > requirements.txt

build: ## Собрать автономный .exe через PyInstaller
	poetry run pyinstaller --noconfirm --onefile --windowed --add-data "src/template/template.html;template" --icon="img/volgau_gerb.ico" main.py
