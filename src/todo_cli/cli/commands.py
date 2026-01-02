import sys
import json
from typing import Optional
import click
from ..services.task_service import TaskService


@click.group()
def cli():
    """A command-line todo application with in-memory storage."""
    pass


@cli.command()
@click.argument('content', type=str)
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
def add(content: str, json_output: bool):
    """Add a new task to the todo list."""
    try:
        service = TaskService()
        task = service.add_task(content)

        if json_output:
            result = {
                "success": True,
                "task": {
                    "id": task.id,
                    "content": task.content,
                    "completed": task.completed
                }
            }
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"Task added successfully with ID {task.id}")

        sys.exit(0)
    except Exception as e:
        if json_output:
            error_result = {
                "success": False,
                "error": str(e),
                "error_code": 1
            }
            click.echo(json.dumps(error_result, indent=2))
        else:
            click.echo(f"Error: {str(e)}")

        sys.exit(1)


@cli.command()
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
def list(json_output: bool):
    """List all tasks in the todo list."""
    try:
        service = TaskService()
        tasks = service.get_all_tasks()

        if json_output:
            result = {
                "tasks": [
                    {
                        "id": task.id,
                        "content": task.content,
                        "completed": task.completed
                    }
                    for task in tasks
                ]
            }
            click.echo(json.dumps(result, indent=2))
        else:
            if not tasks:
                click.echo("No tasks in the list.")
            else:
                for task in tasks:
                    status = "X" if task.completed else "O"
                    click.echo(f"[{status}] {task.id}: {task.content}")

        sys.exit(0)
    except Exception as e:
        if json_output:
            error_result = {
                "success": False,
                "error": str(e),
                "error_code": 1
            }
            click.echo(json.dumps(error_result, indent=2))
        else:
            click.echo(f"Error: {str(e)}")

        sys.exit(1)


@cli.command()
@click.argument('task_id', type=int)
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
def complete(task_id: int, json_output: bool):
    """Mark a task as complete."""
    try:
        service = TaskService()
        task = service.mark_complete(task_id)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "content": task.content,
                        "completed": task.completed
                    }
                }
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(f"Task {task_id} marked as complete")
            sys.exit(0)
        else:
            if json_output:
                error_result = {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                    "error_code": 2
                }
                click.echo(json.dumps(error_result, indent=2))
            else:
                click.echo(f"Error: Task with ID {task_id} not found")
            sys.exit(2)
    except Exception as e:
        if json_output:
            error_result = {
                "success": False,
                "error": str(e),
                "error_code": 1
            }
            click.echo(json.dumps(error_result, indent=2))
        else:
            click.echo(f"Error: {str(e)}")

        sys.exit(1)


@cli.command()
@click.argument('task_id', type=int)
@click.argument('content', type=str)
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
def update(task_id: int, content: str, json_output: bool):
    """Update the content of a task."""
    try:
        service = TaskService()
        task = service.update_task(task_id, content)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "content": task.content,
                        "completed": task.completed
                    }
                }
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(f"Task {task_id} updated successfully")
            sys.exit(0)
        else:
            if json_output:
                error_result = {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                    "error_code": 2
                }
                click.echo(json.dumps(error_result, indent=2))
            else:
                click.echo(f"Error: Task with ID {task_id} not found")
            sys.exit(2)
    except Exception as e:
        if json_output:
            error_result = {
                "success": False,
                "error": str(e),
                "error_code": 1
            }
            click.echo(json.dumps(error_result, indent=2))
        else:
            click.echo(f"Error: {str(e)}")

        sys.exit(1)


@cli.command()
@click.argument('task_id', type=int)
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
def delete(task_id: int, json_output: bool):
    """Delete a task from the todo list."""
    try:
        service = TaskService()
        success = service.delete_task(task_id)

        if success:
            if json_output:
                result = {
                    "success": True,
                    "message": f"Task {task_id} deleted successfully"
                }
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(f"Task {task_id} deleted successfully")
            sys.exit(0)
        else:
            if json_output:
                error_result = {
                    "success": False,
                    "error": f"Task with ID {task_id} not found",
                    "error_code": 2
                }
                click.echo(json.dumps(error_result, indent=2))
            else:
                click.echo(f"Error: Task with ID {task_id} not found")
            sys.exit(2)
    except Exception as e:
        if json_output:
            error_result = {
                "success": False,
                "error": str(e),
                "error_code": 1
            }
            click.echo(json.dumps(error_result, indent=2))
        else:
            click.echo(f"Error: {str(e)}")

        sys.exit(1)


if __name__ == '__main__':
    cli()