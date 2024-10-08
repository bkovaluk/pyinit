# Potara ![Lint](https://github.com/bkovaluk/potara/actions/workflows/lint.yml/badge.svg) | ![Test](https://github.com/bkovaluk/potara/actions/workflows/test.yml/badge.svg)



Potara is a powerful command-line tool designed to streamline the creation of new Python projects with a standardized and customizable structure. By automating the setup process, Potara allows developers to focus on writing code rather than configuring their projects from scratch.

## Features

- **Standardized Project Structure:** Automatically creates essential directories and files.
- **Virtual Environment Setup:** Optionally creates a virtual environment for dependency management.
- **Git Integration:** Initializes a Git repository and makes the initial commit.
- **CI/CD Configuration:** Sets up GitHub Actions workflows and Dependabot configurations.
- **Template Rendering:** Utilizes Jinja2 templates for dynamic file generation.
- **Interactive and Non-Interactive Modes:** Choose between guided setup or default settings.
- **Poetry Integration:** Leverages Poetry for dependency management and packaging.

## Installation

To install **Potara**, follow these steps:

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.7+**: Download from [python.org](https://www.python.org/downloads/).
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads).
- **Poetry**: Install following the [official guide](https://python-poetry.org/docs/#installation).

### Steps

1. **Clone the Repository:**

    Navigate to your desired directory and clone the Potara repository.

    ~~~bash
    git clone https://github.com/yourusername/potara.git
    cd potara
    ~~~

2. **Install Dependencies:**

    Use Poetry to install the necessary dependencies.

    ~~~bash
    poetry install
    ~~~

3. **Activate the Poetry Shell:**

    Enter the Poetry-managed virtual environment.

    ~~~bash
    poetry shell
    ~~~

4. **(Optional) Install Potara Globally:**

    If you wish to use Potara as a global command-line tool, install it in editable mode.

    ~~~bash
    poetry install --editable
    ~~~

## Usage

Initialize a new Python project by running the `potara` command followed by your desired project name.

### Basic Usage

~~~bash
potara my_project
~~~

This command will create a new directory named `my_project` with a standardized Python project structure.

### Available Options

- `--description`: Project description. Default is "A new Python project."
- `--author`: Author name. Default is "Your Name."
- `--email`: Author email. Default is "you@example.com."
- `--license`: License type. Choices are "MIT", "Apache-2.0", "GPL-3.0". Default is "MIT."
- `--venv`: Flag to create a virtual environment.
- `--git`: Flag to initialize a Git repository.
- `--ci`: Flag to set up GitHub Actions workflows and Dependabot.
- `--interactive`: Flag to run `poetry init` interactively. By default, it runs non-interactively.

### Example with All Options

~~~bash
potara awesome_app --description "An awesome Python application." --author "Alice Smith" --email "alice.smith@example.com" --license MIT --venv --git --ci --interactive
~~~

This command will:

- Create a directory named `awesome_app`.
- Set up a virtual environment.
- Initialize a Git repository and make the initial commit.
- Set up GitHub Actions workflows and Dependabot configurations.
- Run `poetry init` interactively to create `pyproject.toml`.
- Generate all necessary project files based on templates.

## Project Structure

Upon initialization, Potara sets up the following project structure:

~~~plaintext
awesome_app/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci.yml
├── src/
│   └── awesome_app/
│       └── __init__.py
├── tests/
│   └── test_awesome_app.py
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── requirements.txt
└── pyproject.toml
~~~

## Testing

Potara includes test cases to ensure that the project initialization works as expected.

### Running Tests

To run the tests, navigate to the Potara project directory and execute:

~~~bash
pytest
~~~

Ensure that you're inside the Poetry shell or that the virtual environment is activated.

## Contribution

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository:**

    ~~~bash
    git clone https://github.com/yourusername/potara.git
    cd potara
    ~~~

2. **Create a New Branch:**

    ~~~bash
    git checkout -b feature/YourFeatureName
    ~~~

3. **Make Your Changes:**

    Implement your feature or bug fix.

4. **Commit Your Changes:**

    ~~~bash
    git commit -m "Add feature: YourFeatureName"
    ~~~

5. **Push to the Branch:**

    ~~~bash
    git push origin feature/YourFeatureName
    ~~~

6. **Create a Pull Request:**

    Submit a pull request detailing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Poetry](https://python-poetry.org/) for dependency management.
- [Click](https://click.palletsprojects.com/) for building the CLI.
- [Jinja2](https://jinja.palletsprojects.com/) for templating.
- [Pytest](https://pytest.org/) for testing.

