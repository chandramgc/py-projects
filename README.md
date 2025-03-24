# My Project

## 📌 Overview

This project is a Python-based configuration server that fetches configurations from a Git repository dynamically based
on profiles.

## 📂 Project Structure

```
my_project/
│── src/                     # Source code
│   ├── modules/             # Business logic modules
│   ├── utils/               # Utility functions/helpers
│   ├── services/            # External services and API handlers
│   ├── models/              # Data models or database ORM models
│   ├── controllers/         # Controllers/Views for handling requests
│   ├── config/              # Configuration settings
│   ├── main.py              # Entry point of the application
│
│── tests/                   # Unit and integration tests
│   ├── test_modules/             # Business logic modules
│   ├── test_utils/               # Utility functions/helpers
│   ├── test_services/            # External services and API handlers
│   ├── test_models/              # Data models or database ORM models
│   ├── test_controllers/         # Controllers/Views for handling requests
│── data/                    # Data files (if applicable)
│   ├── raw/                 # Raw data
│   ├── processed/           # Processed data
│── scripts/                 # Standalone scripts and automation tools
│── docs/                    # Documentation
│── logs/                    # Log files
│── venv/                    # Virtual environment (should be ignored in .gitignore)
│── requirements.txt         # Python dependencies
│── setup.py                 # Setup script for packaging (if applicable)
│── README.md                # Project documentation
│── .gitignore               # Files to ignore in version control
```

## 🛠️ Installation

### Prerequisites

- Python 3.x
- Git
- Virtual Environment (optional but recommended)

### Steps to Install

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/my_project.git
   cd my_project
   ```
2. **Create a virtual environment** (optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the main script:

```bash
export PYTHONPATH=.
python -m src.main
```

## 🧪 Running Tests

To run tests, execute:

```bash
python -m unittest discover -s tests -v
```

## ✅ Code Coverage

We use [coverage.py](https://coverage.readthedocs.io/) to measure how much of our code is exercised by the tests. This
helps ensure that our tests cover critical parts of the application.

### 1. Install Coverage

Install the coverage package via pip:

```bash
pip install coverage
```

### 2. Run Tests with Coverage

Run your tests and collect coverage data using the following command from your project's root directory:

```bash
coverage run -m unittest discover -s tests
```

### 3. Generate a Coverage Report

To display a text-based report in your terminal, run:

```bash
coverage report
```

To generate an HTML report that provides detailed coverage information, run:

```bash
coverage html
```

You can then open the generated htmlcov/index.html file in your browser to view the detailed report.

## 📚 Documentation

Our project documentation is generated using [Sphinx](https://www.sphinx-doc.org/), which supports automatic extraction
of docstrings from our source code. This helps keep our API documentation up-to-date and provides detailed information
on each module.

### Getting Started with Documentation

1. **Install Sphinx and Extensions**

   Install Sphinx along with the recommended extension for type hints:
   ```bash
   pip install sphinx sphinx-autodoc-typehints
   ```
2. **Initialize Sphinx (If Not Already Done)**

   If you haven't already configured Sphinx, navigate to the docs/ directory and run:
   ```bash
   cd docs
   sphinx-quickstart
   ```
   Answer the prompts to set up your documentation.

3. **Configure Sphinx**

   In the docs/conf.py file, add your source directory to the sys.path and enable the autodoc and napoleon extensions.
   For example:

   ```python
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../src'))

   extensions = [
      'sphinx.ext.autodoc',          # Automatically document API from docstrings
      'sphinx.ext.napoleon',         # Support for Google style and NumPy style docstrings
      'sphinx_autodoc_typehints',    # Better type hint support
   ]

   html_theme = 'alabaster'
   ```
4. **Generate the HTML Documentation**

   Build the documentation by running:

   ```bash
   make.bat html
   ```
   This will create an HTML version of your docs in the docs/_build/html/ directory.

5. **View the Documentation**

   Open docs/_build/html/index.html in your browser to review your documentation.

## ⚙️ Setup and Installation

Our project is packaged using setuptools via `setup.py`. Follow the steps below to package, install, and run the
application.

### 1. Packaging the Project

From the root directory of your project (where `setup.py` is located), run:

```bash
python setup.py sdist bdist_wheel
```

This command generates a source distribution (.tar.gz) and a wheel (.whl) file in the dist/ directory.

### 2. Installing the Package

To install the package locally, run:

```bash
pip install .
```

For an editable installation (which allows you to make changes to the code without reinstalling), run:

```bash
pip install -e .
```

### 3. Running the Application

If you have defined an entry point in setup.py, you can run your application directly from the command line. For
example, if your entry point is configured as:

```python
entry_points = {
    "console_scripts": [
        "config-server=main:main",
    ]
},
```

After installing the package, simply run:

```bash
config-server
```

This command will invoke the main() function defined in your src/main.py.

### 4. Uninstalling the Package

If you need to uninstall your package, you can do so by running:

```bash
pip uninstall config-server
```

By following these steps, you can easily distribute and run your project using the provided setup.py configuration.

## 📜 License

This project is open-source.
