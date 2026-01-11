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
@click.argument('title', type=str)
@click.argument('description', type=str, default="")
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def add(title: str, description: str, user_id: str, json_output: bool):
    """Add a new task to the todo list."""
    try:
        service = TaskService(user_id=user_id)
        task = service.add_task(title, description)

        if json_output:
            result = {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "user_id": task.user_id
                }
            }
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo(f"Task '{task.title}' added successfully with ID {task.id}")

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
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the tasks')
def list(user_id: str, json_output: bool):
    """List all tasks in the todo list."""
    try:
        service = TaskService(user_id=user_id)
        tasks = service.get_all_tasks()

        if json_output:
            result = {
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                        "user_id": task.user_id
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
                    click.echo(f"[{status}] {task.id}: {task.title}")

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
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def complete(task_id: int, user_id: str, json_output: bool):
    """Mark a task as complete."""
    try:
        service = TaskService(user_id=user_id)
        task = service.mark_complete(task_id)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                        "user_id": task.user_id
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
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def incomplete(task_id: int, user_id: str, json_output: bool):
    """Mark a task as incomplete."""
    try:
        service = TaskService(user_id=user_id)
        task = service.mark_incomplete(task_id)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                        "user_id": task.user_id
                    }
                }
                click.echo(json.dumps(result, indent=2))
            else:
                click.echo(f"Task {task_id} marked as incomplete")
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
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def toggle(task_id: int, user_id: str, json_output: bool):
    """Toggle the completion status of a task."""
    try:
        service = TaskService(user_id=user_id)
        task = service.toggle_completion(task_id)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                        "user_id": task.user_id
                    }
                }
                click.echo(json.dumps(result, indent=2))
            else:
                status = "complete" if task.completed else "incomplete"
                click.echo(f"Task {task_id} marked as {status}")
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
@click.argument('title', type=str)
@click.argument('description', type=str, default="")
@click.option('--json', 'json_output', is_flag=True, help='Output in JSON format')
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def update(task_id: int, title: str, description: str, user_id: str, json_output: bool):
    """Update the title and description of a task."""
    try:
        service = TaskService(user_id=user_id)
        task = service.update_task(task_id, title, description)

        if task:
            if json_output:
                result = {
                    "success": True,
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat(),
                        "user_id": task.user_id
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
@click.option('--user-id', 'user_id', default='default_user', help='User ID for the task')
def delete(task_id: int, user_id: str, json_output: bool):
    """Delete a task from the todo list."""
    try:
        service = TaskService(user_id=user_id)
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