import sys
import os
from typing import Optional
from .services.task_service import TaskService


class MenuDrivenTodoCLI:
    """Menu-driven Todo CLI application."""

    def __init__(self, user_id: str = "cli-user"):
        self.user_id = user_id
        self.service = TaskService(user_id=self.user_id)

    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("           TODO CLI APPLICATION")
        print("="*50)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task Complete")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. View Task Details")
        print("7. Clear All Tasks")
        print("8. Exit")
        print("="*50)
        print("Choose an option (1-8): ", end="")

    def get_user_input(self):
        """Get user input."""
        try:
            choice = input().strip()
            return choice
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)

    def add_task(self):
        """Add a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        description = input("Enter task description (optional): ").strip()

        if not title:
            print("Error: Task title cannot be empty!")
            return

        try:
            task = self.service.add_task(title, description)
            print(f"✓ Task added successfully with ID {task.id}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    def list_tasks(self):
        """List all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks in the list.")
            return

        print(f"{'ID':<4} {'Status':<8} {'Title'}")
        print("-" * 50)

        for task in tasks:
            status = "✓ Done" if task.completed else "○ Pending"
            print(f"{task.id:<4} {status:<8} {task.title}")

    def clear_all_tasks(self):
        """Clear all tasks from the list."""
        print("\n--- Clear All Tasks ---")

        tasks = self.service.get_all_tasks()
        if not tasks:
            print("No tasks to clear!")
            return

        confirm = input(f"Are you sure you want to delete ALL {len(tasks)} tasks? (y/N): ").strip().lower()

        if confirm in ['y', 'yes']:
            # Delete all tasks one by one
            for task in tasks:
                self.service.delete_task(task.id)
            print(f"✓ All {len(tasks)} tasks have been deleted!")
        else:
            print("Operation cancelled.")

    def mark_complete(self):
        """Mark a task as complete."""
        print("\n--- Mark Task Complete ---")
        try:
            task_id = int(input("Enter task ID to mark complete: "))
            task = self.service.mark_complete(task_id)

            if task:
                print(f"✓ Task {task_id} marked as complete!")
            else:
                print(f"✗ Error: Task with ID {task_id} not found!")
        except ValueError:
            print("✗ Error: Please enter a valid task ID!")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    def update_task(self):
        """Update a task."""
        print("\n--- Update Task ---")
        try:
            task_id = int(input("Enter task ID to update: "))
            current_task = self.service.get_task_by_id(task_id)

            if not current_task:
                print(f"✗ Error: Task with ID {task_id} not found!")
                return

            print(f"Current title: {current_task.title}")
            print(f"Current description: {current_task.description}")
            
            new_title = input("Enter new title (leave blank to keep current): ").strip()
            new_description = input("Enter new description (leave blank to keep current): ").strip()

            final_title = new_title if new_title else current_task.title
            final_description = new_description if new_description else current_task.description

            updated_task = self.service.update_task(task_id, final_title, final_description)
            if updated_task:
                print(f"✓ Task {task_id} updated successfully!")
            else:
                print(f"✗ Error: Could not update task {task_id}!")
        except ValueError:
            print("✗ Error: Please enter a valid task ID!")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    def delete_task(self):
        """Delete a task."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: "))
            success = self.service.delete_task(task_id)

            if success:
                print(f"✓ Task {task_id} deleted successfully!")
            else:
                print(f"✗ Error: Task with ID {task_id} not found!")
        except ValueError:
            print("✗ Error: Please enter a valid task ID!")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    def view_task_details(self):
        """View detailed information about a specific task."""
        print("\n--- View Task Details ---")
        try:
            task_id = int(input("Enter task ID to view: "))
            task = self.service.get_task_by_id(task_id)

            if task:
                print(f"\nTask Details:")
                print(f"ID: {task.id}")
                print(f"Title: {task.title}")
                print(f"Description: {task.description}")
                print(f"Status: {'Completed' if task.completed else 'Pending'}")
            else:
                print(f"✗ Error: Task with ID {task_id} not found!")
        except ValueError:
            print("✗ Error: Please enter a valid task ID!")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo CLI Application!")

        while True:
            self.display_menu()
            choice = self.get_user_input()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.mark_complete()
            elif choice == '4':
                self.update_task()
            elif choice == '5':
                self.delete_task()
            elif choice == '6':
                self.view_task_details()
            elif choice == '7':
                self.clear_all_tasks()
            elif choice == '8':
                print("\nThank you for using Todo CLI Application!")
                print("Goodbye! 👋")
                break
            else:
                print("✗ Invalid option! Please choose 1-8.")

            # Pause to let user see the result before showing menu again
            input("\nPress Enter to continue...")


def main():
    """Start the menu-driven Todo CLI."""
    app = MenuDrivenTodoCLI()
    app.run()


if __name__ == '__main__':
    main()