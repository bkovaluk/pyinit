#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyInit CLI Tool: Initialize a new Python project.

This script creates a new Python project with the specified configurations.

Description:
- Creates a new project directory with the specified name.
- Renders template files (e.g., README.md, LICENSE) using Jinja2 templates.
- Optionally initializes a virtual environment and installs dependencies.
- Optionally initializes a Git repository and makes the initial commit.
- Optionally sets up CI/CD configurations using GitHub Actions and Dependabot.

Arguments:
- project_name: Name of the project directory to create.

Options:
- --description: Project description. Default is 'A new Python project.'.
- --author: Author name. Default is 'Your Name'.
- --email: Author email. Default is 'you@example.com'.
- --license: License type. Choices are 'MIT', 'Apache-2.0', 'GPL-3.0'. Default is 'MIT'.
- --venv: If provided, creates a virtual environment in the project directory.
- --git: If provided, initializes a Git repository in the project directory.
- --ci: If provided, sets up GitHub Actions workflow and Dependabot configuration.
- --interactive: If provided, runs 'poetry init' interactively.

Usage:
- Run the script with the required arguments and options.

Example:
python script.py my_project --author "John Doe" --email "john@example.com" --license MIT --venv --git --ci
"""

__author__ = "Bradley Kovaluk"
__email__ = "bkovaluk@gmail.com"
__description__ = "Initialize a new Python project with optional configurations."
__version__ = "0.1.0"
__date__ = "2024-10-08"
__license__ = "MIT"

import os
import subprocess
from datetime import datetime
from enum import Enum

from jinja2 import Environment, FileSystemLoader, select_autoescape
import typer

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_template(template_name, **context):
    """Render a template with the given context."""
    template = env.get_template(template_name)
    return template.render(**context)

class LicenseType(str, Enum):
    MIT = 'MIT'
    Apache = 'Apache-2.0'
    GPL = 'GPL-3.0'

app = typer.Typer()

@app.command()
def cli(
    project_name: str = typer.Argument(..., help='Name of the project'),
    description: str = typer.Option('A new Python project.', help='Project description.'),
    author: str = typer.Option('Your Name', help='Author name.'),
    email: str = typer.Option('you@example.com', help='Author email.'),
    license: LicenseType = typer.Option(LicenseType.MIT, help='License type.'),
    venv: bool = typer.Option(False, help='Create a virtual environment.'),
    git: bool = typer.Option(False, help='Initialize a Git repository.'),
    ci: bool = typer.Option(False, help='Set up GitHub Actions workflow and Dependabot.'),
    interactive: bool = typer.Option(False, help='Run poetry init interactively.')
):
    """PyInit CLI Tool: Initialize a new Python project."""
    
    # Define the project directory path
    project_dir = os.path.abspath(project_name)
    
    # Check if the project directory already exists
    if os.path.exists(project_dir):
        typer.echo(f"Error: Directory '{project_dir}' already exists.")
        raise typer.Exit(code=1)
    
    # Create the main project directory
    os.makedirs(project_dir)
    typer.echo(f"Created project directory: {project_dir}")
    
    # Context for templates
    context = {
        'project_name': project_name,
        'description': description,
        'author': author,
        'email': email,
        'license': license.value,
        'year': datetime.now().year
    }
    
    # List of templates to render
    templates = {
        'README.md.j2': 'README.md',
        '.gitignore.j2': '.gitignore',
        'Makefile.j2': 'Makefile',
        'LICENSE.j2': 'LICENSE',
        'requirements.txt.j2': 'requirements.txt',
        'test_project.py.j2': os.path.join('tests', f'test_{project_name}.py'),
        'src_init.py.j2': os.path.join('src', project_name, '__init__.py'),
        'ci.yml.j2': os.path.join('.github', 'workflows', 'ci.yml'),
        'dependabot.yml.j2': os.path.join('.github', 'dependabot.yml')
    }
    
    # Create subdirectories before rendering templates that depend on them
    subdirs = [
        os.path.join(project_dir, 'src', project_name),
        os.path.join(project_dir, 'tests'),
        os.path.join(project_dir, '.github', 'workflows')
    ]
    
    for subdir in subdirs:
        os.makedirs(subdir, exist_ok=True)
        typer.echo(f"Created directory: {subdir}")
    
    # Render and write template files
    for template_file, output_file in templates.items():
        rendered_content = render_template(template_file, **context)
        output_path = os.path.join(project_dir, output_file)
        
        # Ensure the directory exists for nested files
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(rendered_content)
        typer.echo(f"Created file: {output_path}")
    
    # Optionally run poetry init
    poetry_init_cmd = ['poetry', 'init']
    if not interactive:
        poetry_init_cmd.append('--no-interaction')
    
    typer.echo("Initializing Poetry...")
    try:
        subprocess.run(poetry_init_cmd, cwd=project_dir, check=True)
        typer.echo("Poetry initialization completed.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error during Poetry initialization: {e}")
        raise typer.Exit(code=1)
    
    # Optionally set up CI/CD configurations
    if ci:
        typer.echo("CI/CD configurations already set up via templates.")
        # No additional action needed since ci.yml and dependabot.yml are rendered above
    
    # Optionally create a virtual environment and install dependencies
    if venv:
        venv_path = os.path.join(project_dir, 'venv')
        typer.echo("Creating virtual environment...")
        subprocess.run([os.sys.executable, '-m', 'venv', venv_path], check=True)
        typer.echo(f"Created virtual environment at '{venv_path}'")
        
        # Define the path to the pip executable
        pip_executable = os.path.join(venv_path, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'pip.exe')
        
        # Upgrade pip and install dependencies
        subprocess.run([pip_executable, 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([pip_executable, 'install', '-r', os.path.join(project_dir, 'requirements.txt')], check=True)
        typer.echo("Installed project dependencies.")
    
    # Optionally initialize a Git repository
    if git:
        try:
            subprocess.run(['git', 'init'], cwd=project_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_dir, check=True)
            typer.echo("Initialized Git repository and made the initial commit.")
        except subprocess.CalledProcessError as e:
            typer.echo(f"Git initialization failed: {e}")
    
    typer.echo(f"\nProject '{project_name}' has been successfully initialized!")

if __name__ == '__main__':
    app()
