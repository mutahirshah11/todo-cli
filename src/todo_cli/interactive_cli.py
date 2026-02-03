import sys
import json
from typing import Optional
from cmd import Cmd
from .services.task_service import TaskService


class TodoCLI(Cmd):
    """Interactive Todo CLI application."""

    intro = 'Welcome to the Todo CLI application. Type help or ? to list commands.\n'
    prompt = '(todo) '

    def __init__(self):
        super().__init__()
        self.user_id = "cli-user"
        self.service = TaskService(user_id=self.user_id)

    def do_add(self, arg):
        """Add a new task: add <task title>"""
        if not arg.strip():
            print("Error: Task title is required")
            return
        try:
            # For interactive CLI, we'll treat the arg as title and empty description
            task = self.service.add_task(arg.strip(), "")
            print(f"Task added successfully with ID {task.id}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_list(self, arg):
        """List all tasks: list"""
        try:
            tasks = self.service.get_all_tasks()
            if not tasks:
                print("No tasks in the list.")
            else:
                for task in tasks:
                    status = "X" if task.completed else "O"
                    print(f"[{status}] {task.id}: {task.title}")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_complete(self, arg):
        """Mark a task as complete: complete <task_id>"""
        try:
            task_id = int(arg.strip())
            task = self.service.mark_complete(task_id)
            if task:
                print(f"Task {task_id} marked as complete")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Error: Please provide a valid task ID")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_update(self, arg):
        """Update a task: update <task_id> <new_title>"""
        try:
            parts = arg.split(' ', 1)
            if len(parts) < 2:
                print("Usage: update <task_id> <new_title>")
                return
            task_id = int(parts[0])
            new_title = parts[1]
            # Get existing task to preserve description if needed, or just update title
            current_task = self.service.get_task_by_id(task_id)
            if not current_task:
                print(f"Error: Task with ID {task_id} not found")
                return
                
            task = self.service.update_task(task_id, new_title, current_task.description)
            if task:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Error: Please provide a valid task ID")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_delete(self, arg):
        """Delete a task: delete <task_id>"""
        try:
            task_id = int(arg.strip())
            success = self.service.delete_task(task_id)
            if success:
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Error: Task with ID {task_id} not found")
        except ValueError:
            print("Error: Please provide a valid task ID")
        except Exception as e:
            print(f"Error: {str(e)}")

    def do_json(self, arg):
        """Toggle JSON output mode: json on/off"""
        print("JSON mode is not implemented in interactive mode. Use command-line for JSON output.")

    def do_quit(self, arg):
        """Exit the application: quit"""
        print("Goodbye!")
        return True

    def do_exit(self, arg):
        """Exit the application: exit"""
        print("Goodbye!")
        return True

    def do_help(self, arg):
        """Show help: help [command]"""
        commands = {
            'add': 'Add a new task: add <task title>',
            'list': 'List all tasks: list',
            'complete': 'Mark a task as complete: complete <task_id>',
            'update': 'Update a task: update <task_id> <new_title>',
            'delete': 'Delete a task: delete <task_id>',
            'quit': 'Exit the application: quit',
            'exit': 'Exit the application: exit',
            'help': 'Show help: help [command]'
        }

        if arg:
            if arg in commands:
                print(commands[arg])
            else:
                print(f"Unknown command: {arg}")
        else:
            print("Available commands:")
            for cmd, desc in commands.items():
                print(f"  {cmd:<10} - {desc}")


def main():
    """Start the interactive Todo CLI."""
    TodoCLI().cmdloop()


if __name__ == '__main__':
    main()