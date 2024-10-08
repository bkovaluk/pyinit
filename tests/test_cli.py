import os
import tempfile

from typer.testing import CliRunner

from pyinit.cli import app


def test_init():
    runner = CliRunner()
    project_name = 'test_project'

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chdir(tmpdirname)

        result = runner.invoke(app, [
            project_name,
            '--description', 'Test Project Description',
            '--author', 'Test Author',
            '--email', 'test@example.com',
            '--license', 'MIT',
            '--venv',
            '--git',
            '--ci'
        ])

        assert result.exit_code == 0
        assert f"Project '{project_name}' has been initialized!" in result.stdout
        assert os.path.exists(project_name)
        assert os.path.exists(os.path.join(project_name, 'README.md'))
        assert os.path.exists(os.path.join(project_name, '.gitignore'))
        assert os.path.exists(os.path.join(project_name, 'Makefile'))
        assert os.path.exists(os.path.join(project_name, 'LICENSE'))
        assert os.path.exists(os.path.join(project_name, 'pyproject.toml'))
        assert os.path.exists(os.path.join(project_name, 'requirements.txt'))
        assert os.path.exists(
            os.path.join(project_name, 'src', project_name, '__init__.py')
        )
        assert os.path.exists(
            os.path.join(project_name, 'tests', f'test_{project_name}.py')
        )
        assert os.path.exists(os.path.join(project_name, 'venv'))
        assert os.path.exists(
            os.path.join(project_name, '.github', 'workflows', 'ci.yml')
        )
        assert os.path.exists(os.path.join(project_name, '.github', 'dependabot.yml'))
