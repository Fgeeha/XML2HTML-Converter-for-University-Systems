## Overview

The **XML2HTML-Converter-for-University-Systems** project parses XML files exported from a university
enrollment system and renders them into ready-to-publish HTML rating lists. It handles four types of
admission campaigns (`bak`, `mag`, `spo`, `asp`), computes applicant priorities and produces one HTML
report per campaign. The project includes logging and error handling, making it robust for managing
exceptions and tracking the processing status.

## Features

- Parses XML files efficiently, with XXE-hardened parsing (`defusedxml`)
- Computes the highest-priority flag for bachelor's and master's campaigns
- Renders reports from a Jinja2 template
- Archives processed input into a timestamped `dump/` folder
- Basic logging and error handling
- Modular codebase for easy extensibility
- Ships as a standalone Windows `.exe`, built automatically on every release tag

## Prerequisites

- Python >= 3.11, < 3.14
- Required Python libraries, as specified in `requirements.txt` or `pyproject.toml`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Fgeeha/XML2HTML-Converter-for-University-Systems.git
cd XML2HTML-Converter-for-University-Systems
```

2. Install dependencies:

mac or linux
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

OR use [poetry](https://python-poetry.org/docs)

```bash
poetry install
```

Poetry 2.x has no built-in `poetry shell`. Either prefix commands with `poetry run`, or activate the
environment explicitly:

```bash
poetry env activate
```

3. Set up environment variables by copying the template:

```bash
cp .env.template .env
```

Configure the environment variables as necessary.

## Usage

The main entry point of the application is located in `main.py`. To run the script:

```bash
python main.py
```

OR use poetry

```bash
poetry run python ./main.py
```

OR use the makefile

```bash
make app
```

### Input files

**Place the input archives in the repository root** — the application resolves them by name, using the
campaign IDs from `src/core/config.py`:

| File | Required for | Purpose |
|------|--------------|---------|
| `enr_rating_<pk_id>.xml.zip` | all campaigns | gzip-compressed XML with the rating list |
| `enr_recommended_enrollment_list_<pk_id>.zip` | `bak`, `mag` | zip archive with priority data |

The `<pk_id>` values are defined by `pk_id` in `src/core/config.py`. A campaign is skipped with a
warning if its `.xml.zip` is missing.

### Output

For every processed campaign the application writes `spiski_abitur_<pk_name>_<year>.html` into the
working directory, for example `spiski_abitur_bak_2026.html`.

### Configuration

Settings are read from `.env` with the `APP_CONFIG__` prefix and `__` as the nesting delimiter:

```bash
APP_CONFIG__APP__DEBUG=True
```

- `DEBUG=True` — input archives stay in the root, nothing is moved
- `DEBUG=False` — processed archives are moved into `dump/<DDMMYYYY HH-MM-SS>/`

`.env.template` is used as a fallback when no `.env` exists, so out of the box the application starts
in `DEBUG=True` mode.

## Project Structure

```
XML2HTML-Converter-for-University-Systems/
│
├── .github/workflows/build.yml    # Build in exe on github
├── img/volgau_gerb.ico            # Picture for the program
├── src/
│   ├── __init__.py
│   ├── initializing_creation.py   # Unpacking, orchestration, dump handling
│   ├── list_priority.py           # Forms priorities
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # MAIN information (file names)
│   └── template/
│       ├── __init__.py
│       ├── template.html          # Template
│       └── create_html.py         # Parse the xml and pass in template
├── .deepsource.toml               # Static analysis config
├── .env.template                  # Environment variables template
├── .flake8                        # Config flake8
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .gitattributes
├── .gitignore
├── makefile                       # app / freeze / build targets
├── requirements.txt               # Required Python libraries
├── poetry.lock                    # Required Python libraries
├── pyproject.toml                 # Required Python libraries
├── README.md                      # Project documentation
├── TODO.md                        # Project plans
└── main.py                        # Entry point script
```

## Development

### Makefile targets

```bash
make app      # run the application
make build    # build a standalone .exe with PyInstaller
make freeze   # regenerate requirements.txt from the active environment
```

### Code quality

The repository is checked by `pre-commit` (pyupgrade, add-trailing-comma, actionlint, autoflake,
black, isort, flake8) and by DeepSource. Line length is 120 characters everywhere.

```bash
poetry run pre-commit install      # enable the hooks for your clone
poetry run pre-commit run --all-files
```

## Contributing

Feel free to contribute to the project by submitting pull requests or opening issues. Ensure that your
code follows the repository's existing style and structure.

### Git push tag

Pushing a tag that matches `v*.*.*` triggers the **Build and Deploy EXE** workflow: it builds
`dist/main.exe` on `windows-latest` and publishes it as a GitHub Release. The workflow authenticates
with the `GH_PAT` repository secret.

#### Create a tag in the `v*.*.*` format
There are two types of tags in Git: lightweight and annotated. It is recommended to use annotated tags, as they contain additional information such as the author, date, and message.

Creating an annotated tag:
```bash
git tag -a v2.0.3 -m "Release version 2.0.3"
```
- `-a` — indicates that the tag is annotated.
- `v2.0.3` — the tag name corresponding to the  `v*.*.*` template.
- `-m "Release version 2.0.3"` — the message for the tag.

#### Push the tag to the remote repository
Push a **specific tag**:

To trigger only one **specific tag**:

```bash
git push origin v2.0.3
```
**Push all tags**:

If you want to push all the local tags that don't exist in the remote repository yet:
```bash
git push origin --tags
```

#### Deleting a tag: 
If you created the wrong tag by mistake, you can delete it locally and in a remote repository.:
```bash
# Delete a local tag
git tag -d v2.0.3

# Remove tag from remote repository
git push origin --delete v2.0.3
```


## License

This project is licensed under the MIT License.

---

For further information, please refer to the [repository](https://github.com/Fgeeha/XML2HTML-Converter-for-University-Systems).
