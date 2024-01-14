import typer
from gmx.logic.project import ProjectLogic
from gmx.logic.preference import PreferenceLogic

project_app = typer.Typer(help="Project related operations.")

@project_app.command(name="add", help="Creates a new project with the given name.")
def add_project(
        name: str = typer.Argument(
            ..., 
            help="The name of the project to create."
        )
    ):
    """
    Add a project.

    Args:
        name (str): The name of the project to create.
    """
    typer.echo(f"Adding project {name}.")
    pl = ProjectLogic()
    pl.add_project(name)
    typer.echo("Status : Done.")
    pl = PreferenceLogic()
    pl.set_preference('current_project', name)
    typer.echo(f"{name} set as the current project.")
    typer.echo("")
    typer.echo("Run a sample project using the below command:")
    typer.echo(f"gmx wf run sample")

@project_app.command(name="set", help="Set project as a current project.")
def set_current_project(
        name: str = typer.Argument(
            ..., 
            help="The name of the project to set as current."
        )
    ):
    """
    Set project as current project.

    Args:
        name (str): The name of the project to create.
    """
    pl = PreferenceLogic()
    pl.set_preference('current_project', name)
    typer.echo(f"Current project set to {name}.")
    typer.echo("Status : Done.")

@project_app.command(name="get", help="Get current project.")
def get_current_project():
    """
    Get current project.
    """
    pl = PreferenceLogic()
    current_proj = pl.get_preference('current_project')
    if current_proj is None:
        print(f'Current project is not set.\n')
        print(f'Set using:')
        print(f'gmx proj set <your-project-name>')
    else:
        print(f'Current project is {current_proj}.')

    