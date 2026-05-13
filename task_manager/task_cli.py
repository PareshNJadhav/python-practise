import json
import os
import sys
from datetime import datetime
from opcode import opname

"""file handling"""
tasks_storage_path  = "./storage/tasks.json"


def load_tasks():
    if not os.path.exists(tasks_storage_path):
        with open(tasks_storage_path, 'w') as file:
            json.dump([],file)

    with open(tasks_storage_path ,'r')  as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_task(tasks):
    with open(tasks_storage_path, 'w') as file:
        json.dump(tasks,file,indent=4)

"""Helper functions"""
def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

def find_task(tasks,task_id):
    for t in tasks:
        if task_id == t["id"]:
            return t
    return None

def current_time():
    return datetime.now().isoformat()

def clean_tasks():
    tasks = load_tasks()
    tasks.clear()
    save_task(tasks)
    print("All tasks are cleared!")

"""task scheduling feature"""
def add_task(description:str) -> list:
    tasks = load_tasks()
    task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",

        "createdAt": current_time(),
        "updatedAt": current_time()
    }
    tasks.append(task)
    save_task(tasks)
    print(f"Task added successfully (ID: {task['id']})")


def list_tasks(filter_status=None):
    tasks = load_tasks()

    if filter_status:
        tasks = [task for task in tasks if task["status"] == filter_status]

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(f"""
                ID: {task['id']}
                Description: {task['description']}
                Status: {task['status']}
                Created At: {task['createdAt']}
                Updated At: {task['updatedAt']}
                """)

def update_task(task_id:int,new_description:str) -> None:
    tasks = load_tasks()
    task = find_task(tasks,task_id)
    if task is None:
        print("No task found to update")
        return
    else:
        task["description"] = new_description
        task["updatedAt"] = current_time()

    save_task(tasks)
    print("Task updated for task_id %s with description %s"%(task_id,new_description))

def mark_task(task_id:int,status:str) -> None:
    tasks = load_tasks()
    task = find_task(tasks,task_id)
    if task is None:
        print("No task found to mark status")
        return
    else:
        task["status"] = status
        task["updatedAt"] = current_time()

    save_task(tasks)
    print("Task updated for task_id %s with status %s"%(task_id,status))

def delete_task(task_id:int) -> None:
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]


    if len(updated_tasks) == len(tasks):
        print("No task found to delete")
        return

    save_task(updated_tasks)
    print("Task deleted for task_id %s " % task_id)

"""CLI handling"""
def print_usage():
    print("""
Usage:
    python task_cli.py add "Task description"
    python task_cli.py update <id> "New description"
    python task_cli.py delete <id>
    python task_cli.py mark-in-progress <id>
    python task_cli.py mark-done <id>
    python task_cli.py list
    python task_cli.py list done
    python task_cli.py list todo
    python task_cli.py list in-progress
""")



def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Description is required.")
                return

            description = sys.argv[2]
            add_task(description)

        elif command == "update":
            if len(sys.argv) < 4:
                print("Task ID and new description are required.")
                return

            task_id = int(sys.argv[2])
            new_description = sys.argv[3]

            update_task(task_id, new_description)

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Task ID is required.")
                return

            task_id = int(sys.argv[2])

            delete_task(task_id)

        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Task ID is required.")
                return

            task_id = int(sys.argv[2])

            mark_task(task_id, "in-progress")

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Task ID is required.")
                return

            task_id = int(sys.argv[2])

            mark_task(task_id, "done")

        elif command == "list":
            if len(sys.argv) == 2:
                list_tasks()
            else:
                status = sys.argv[2]

                valid_statuses = ["todo", "done", "in-progress"]

                if status not in valid_statuses:
                    print("Invalid status.")
                    return

                list_tasks(status)

        else:
            print("Unknown command.")
            print_usage()

    except ValueError:
        print("Invalid task ID.")


if __name__ == "__main__":
    main()
#
# if __name__ == '__main__':
#     clean_tasks()
#     add_task("Buy grocery")
#     add_task("read book")
#     list_tasks()
#     update_task(2, "read the History books")
#     mark_task(2,"complete")
#     delete_task(1)
#     list_tasks()
