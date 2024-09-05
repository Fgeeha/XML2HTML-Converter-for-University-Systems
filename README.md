## Overview

The **parse_xml_file_volgau** project is designed to parse and process XML files, primarily aimed at automating workflows or processing structured data using Python. The project includes basic logging functionality and error handling, making it robust for managing exceptions and tracking the processing status.

## Features

- Parses XML files efficiently
- Basic logging and error handling
- Modular codebase for easy extensibility
- Well-structured for initializing and processing XML data

## Prerequisites

- Python 3.11 or above
- Required Python libraries, as specified in `requirements.txt` or `pyproject.toml`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Fgeeha/parse_xml_file_volgau.git
cd parse_xml_file_volgau
```

2. Install dependencies:

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

OR

```bash
poetry install
poetry shell
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

The application will initiate XML file parsing, and generates an html file with the entrants' rating at the output. Therefore, **you need to put xml files in the root.**

## Project Structure

```
parse_xml_file_volgau/
│
├── .github/workflows/build.yml    # Build in exe on github
├── .vscode/settings.json
├── img/volgau_gerb.ico            # Picture for the program
├── src/
|   |── __init__.py
│   ├── initializing_creation.py
│   ├── list_priority.py           # Forms priorities
│   ├── core/
│       ├── __init__.py
│       └── config.py              # MAIN information (file names)
│   └── template/
│       ├── __init__.py
│       ├── template.html          # Template
│       └── crete_html.py          # Parse the xml and pass in template
├── .env.template                  # Environment variables template
├── .flake8                        # Config flake8
├── .gitattributes
├── .gitignore
├── requirements.txt               # Required Python libraries
├── poetry.lock                    # Required Python libraries
├── pyproject.toml                 # Required Python libraries
├── README.md                      # Project documentation
├── TODO.md                      # Project plans
└── main.py                        # Entry point script
```

## Contributing

Feel free to contribute to the project by submitting pull requests or opening issues. Ensure that your code follows the repository's existing style and structure.

## License

This project is licensed under the MIT License.

---

For further information, please refer to the [repository](https://github.com/Fgeeha/parse_xml_file_volgau).
