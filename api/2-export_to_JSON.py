#!/usr/bin/python3
"""
2-export_to_JSON.py
Exports an employee's TODO list to a JSON file.
Usage: python3 2-export_to_JSON.py <employee_id>
"""

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def export_todo_json(employee_id):
    """Fetch and export TODO list for a given employee to JSON."""
    base_url = "https://jsonplaceholder.typicode.com"

    try:
        # Fetch user
        user_url = "{}/users/{}".format(base_url, employee_id)
        with urlopen(user_url) as response:
            user_data = json.loads(response.read().decode())
            username = user_data.get("username")

        # Fetch todos
        todos_url = "{}/todos?userId={}".format(base_url, employee_id)
        with urlopen(todos_url) as response:
            todos = json.loads(response.read().decode())

    except HTTPError as e:
        if e.code == 404:
            print("Error: Employee with ID {} not found."
                  .format(employee_id))
        else:
            print("HTTP error: {}".format(e.code))
        sys.exit(1)
    except URLError:
        print("Error: Could not reach the API. "
              "Check your internet connection.")
        sys.exit(1)

    # Build the task list with keys in the expected order
    task_list = []
    for todo in todos:
        task_dict = {
            "task": todo.get("title"),
            "completed": todo.get("completed"),
            "username": username
        }
        task_list.append(task_dict)

    # Create the final JSON structure
    output_data = {str(employee_id): task_list}

    # Write to file (compact JSON, no indentation)
    filename = "{}.json".format(employee_id)
    with open(filename, "w") as f:
        json.dump(output_data, f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 2-export_to_JSON.py <employee_id>")
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    export_todo_json(emp_id)
