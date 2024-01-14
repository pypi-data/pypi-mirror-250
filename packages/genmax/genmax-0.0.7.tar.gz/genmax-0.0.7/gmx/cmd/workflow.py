from typing import List
import typer
from gmx.logic.workflow import WorkFlowLogic
from gmx.logic.preference import PreferenceLogic

workflow_app = typer.Typer(help="Workflow related operations.")

@workflow_app.command(name="run", help="Run a workflow from a specific project.")
def run_workflow(
        workflows: List[str] = typer.Argument(
            ..., 
            help="List the workflows to run."
        )
    ):
    """
    Run a workflow.

    Args:
        name (str): The name of the project with the workflows.
        workflows (list): List of workflows to run.
    """
    typer.echo("Running workflow.")
    pl = PreferenceLogic()
    current_proj = pl.get_preference('current_project')
    if current_proj is None:
        typer.echo("Please set a project to run a workflow.")
        return
    WorkFlowLogic.run_workflows(current_proj, workflows)