import os
import click
import shutil
import subprocess
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_template(template_name, **context):
    """Render a template with the given context."""
    template = env.get_template(template_name)
    return template.render(**context)

@click.command()
@click.argument('project_name')
@click.option('--description', default='A new Python project.', help='Project description.')
@click.option('--author', default='Your Name', help='Author name.')
@click.option('--email', default='you@example.com', help='Author email.')
@click.option('--license', default='MIT', type=click.Choice(['MIT', 'Apache-2.0', 'GPL-3.0']), help='License type.')
@click.option('--venv', is_flag=True, help='Create a virtual environment.')
@click.option('--git', is_flag=True, help='Initialize a Git repository.')
@click.option('--ci', is_flag=True, help='Set up GitHub Actions workflow and Dependabot.')
@click.option('--interactive', is_flag=True, help='Run poetry init interactively.')
def cli(project_name, description, author, email, license, venv, git, ci, interactive):
    """PyInit CLI Tool: Initialize a new Python project."""
    
    # Define the project directory path
    project_dir = os.path.abspath(project_name)
    
    # Check if the project directory already exists
    if os.path.exists(project_dir):
        click.echo(f"Error: Directory '{project_dir}' already exists.")
        return
    
    # Create the main project directory
    os.makedirs(project_dir)
    click.echo(f"Created project directory: {project_dir}")
    
    # Context for templates
    context = {
        'project_name': project_name,
        'description': description,
        'author': author,
        'email': email,
        'license': license,
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
        click.echo(f"Created directory: {subdir}")
    
    # Render and write template files
    for template_file, output_file in templates.items():
        rendered_content = render_template(template_file, **context)
        output_path = os.path.join(project_dir, output_file)
        
        # Ensure the directory exists for nested files
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(rendered_content)
        click.echo(f"Created file: {output_path}")
    
    # Optionally run poetry init
    poetry_init_cmd = ['poetry', 'init']
    if not interactive:
        poetry_init_cmd.append('--no-interaction')
    
    click.echo("Initializing Poetry...")
    try:
        subprocess.run(poetry_init_cmd, cwd=project_dir, check=True)
        click.echo("Poetry initialization completed.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error during Poetry initialization: {e}")
        return
    
    # Optionally set up CI/CD configurations
    if ci:
        click.echo("CI/CD configurations already set up via templates.")
        # No additional action needed since ci.yml and dependabot.yml are rendered above
    
    # Optionally create a virtual environment and install dependencies
    if venv:
        venv_path = os.path.join(project_dir, 'venv')
        click.echo("Creating virtual environment...")
        subprocess.run([os.sys.executable, '-m', 'venv', venv_path], check=True)
        click.echo(f"Created virtual environment at '{venv_path}'")
        
        # Define the path to the pip executable
        pip_executable = os.path.join(venv_path, 'bin', 'pip') if os.name != 'nt' else os.path.join(venv_path, 'Scripts', 'pip.exe')
        
        # Upgrade pip and install dependencies
        subprocess.run([pip_executable, 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([pip_executable, 'install', '-r', os.path.join(project_dir, 'requirements.txt')], check=True)
        click.echo("Installed project dependencies.")
    
    # Optionally initialize a Git repository
    if git:
        try:
            subprocess.run(['git', 'init'], cwd=project_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=project_dir, check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=project_dir, check=True)
            click.echo("Initialized Git repository and made the initial commit.")
        except subprocess.CalledProcessError as e:
            click.echo(f"Git initialization failed: {e}")
    
    click.echo(f"\nProject '{project_name}' has been successfully initialized!")
    
if __name__ == '__main__':
    cli()
