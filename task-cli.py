from pydantic import conbytes
from database.database import JSONDatabase
from database.models import Task, Status
import os

class UserInput():
    def __init__(self, base_prompt: str, base_commands: list) -> None:
        self.base_prompt = base_prompt
        self.base_commands = base_commands
        self.prompt = ''
        self.command = ''
        self.args = ''
    
    @property
    def is_valid(self) -> bool:
        return self.base_prompt.lower() == self.prompt and self.command in self.base_commands

    def callInput(self) -> 'UserInput':
        self.prompt = ''
        self.command = ''
        self.args = []
        line = input()
        for i, arg in enumerate(line.split()):
            if i == 0: self.prompt = arg.lower()
            elif i == 1: self.command = arg.lower()
            else: self.args.append(arg)
        self.args = ' '.join(self.args)
        os.system('clear')
        print(f"\n{self.prompt} {self.command} {self.args}")
        return self
    
    def __str__(self) -> str:
        return f'{self.prompt} {self.command} {self.args}'
        

class TaskCLI():
    def __init__(self) -> None:
        os.system('clear')
        self.database = JSONDatabase()
        self.commands = ['add', 'update', 'delete', 'list', 'mark-in-progress', 'mark-done', 'mark-todo', 'mark-not-done']
        self.prompt = 'task-cli'

    def process(self, command: str, args: str) -> None:
        if command == 'add':
            if not args.startswith('"') and not args.endswith('"'):
                print('[ERROR] Description of task should be in commas: "..."')
                return
            self.database.put(task=Task(description=args))
            print(f"[SUCCESS] Added task (ID={Task._object_count})")
        elif command == "delete":
            if not args.isdigit():
                print('[ERROR] Argument of id should be digit!')
                return
            if isinstance(self.database.delete(int(args)), Task):
                print(f"[SUCCESS] Deleted task with id {int(args)}")
                return
            else:
                print(f'[ERROR] Task with id {int(args)} not found!')
                return
        elif command == 'list':
            tasks = self.database.get()
            if len(tasks) == 0:
                print("You have 0 tasks, add something to task-list...")
                return
            if args == '':
                print('\nAll your tasks: ')
                for task in tasks:
                    print(str(task))
                return
            else:
                try:
                    if args.lower() == 'todo': status = Status.NOT_DONE
                    else: status = Status(args.lower())
                    tasks: list[Task]
                    tasks = [task for task in tasks if task.status == status]
                    if len(tasks) == 0:
                        print(f'You have no tasks with "{status.value}" status...')
                        return
                    
                    print(f'\nAll your "{status.value}" tasks: ')
                    for task in tasks:
                        print(str(task))
                except ValueError:
                    print(f"[ERROR] '{args.lower()}' Is not valid status. You can use 'done, not-done/todo, in-progress'")
        elif command == 'update':
            if len(args.split(maxsplit=1)) < 2:
                print(f'[ERROR] query is invalid. For update command it should look like: update 1 "desc"!')
                return
            
            id, description = args.split(maxsplit=1)
            if not id.isdigit():
                print('[ERROR] Argument of id should be digit!')
                return
            if not description.startswith('"') and not description.endswith('"'):
                print('[ERROR] Description of task should be in commas: "..."')
                return
            
            task = self.database.get(int(id))
            if task is None:
                print(f"[ERROR] Task with id {int(id)} not found!")
                return
            
            task.description = description

            print(f"[SUCCESS] Updated task with id {int(id)}")
            return
        elif command == 'mark-in-progress':
            if not args.isdigit():
                print('[ERROR] Argument of id should be digit!')
                return
            task = self.database.get(int(args))
            if task is None:
                print(f'[ERROR] Task with id {int(args)} not found!')
                return
            task.status = Status.IN_PROGRESS
            self.database.update(task)
            print(f"[SUCCESS] Marked task with id {int(args)} as in-progress")
            return
        elif command == 'mark-done':
            if not args.isdigit():
                print('[ERROR] Argument of id should be digit!')
                return
            task = self.database.get(int(args))
            if task is None:
                print(f'[ERROR] Task with id {int(args)} not found!')
                return
            task.status = Status.DONE
            self.database.update(task)
            print(f"[SUCCESS] Marked task with id {int(args)} as done")
            return
        elif command in ['mark-todo', 'mark-not-done']:
            if not args.isdigit():
                print('[ERROR] Argument of id should be digit!')
                return
            task = self.database.get(int(args))
            if task is None:
                print(f'[ERROR] Task with id {int(args)} not found!')
                return
            task.status = Status.NOT_DONE
            self.database.update(task)
            print(f"[SUCCESS] Marked task with id {int(args)} as todo")
            return
    
    def run_CLILoop(self):
        UserIN = UserInput(self.prompt, self.commands)
        while True:
            user_input = UserIN.callInput()
            if not user_input.is_valid:
                print("""\nCommands for task-cli:
----------------
IMPORTANT:
* - required argument
words 'todo' and 'not-done' is synonyms

task-cli add *[description] - Add task to your list
task-cli delete *[Task ID] - Removes task from your list
task-cli update *[Task ID] *[description] - Updates description of task

task-cli list [done/in-progress/todo] - list your tasks

task-cli mark-todo *[Task ID] - Marks your task as not done                 
task-cli mark-in-progress *[Task ID] - Marks your task as in-progress
task-cli mark-done *[Task ID] - Marks your task as done
"""
                      )
            self.process(user_input.command, user_input.args)
            self.database.save()
            print("\n")

if __name__ == "__main__":
    TaskCLI().run_CLILoop()