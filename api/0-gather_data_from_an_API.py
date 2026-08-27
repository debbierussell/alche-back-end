#!/usr/bin/python3
"""
0-gather_data_from_an_API.py
Fetches and displays an employee's TODO list progress from a REST API.
Usage: python3 0-gather_data_from_an_API.py <employee_id>
"""

import sys
import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def get_employee_todo_progress(employee_id):
    """Fetch and display TODO list progress for a given employee ID."""
    base_url = "https://jsonplaceholder.typicode.com"
    try:
        # Fetch user
        user_url = "{}/users/{}".format(base_url, employee_id)
        with urlopen(user_url) as response:
            user_data = json.loads(response.read().decode())
            employee_name = user_data.get("name")

        # Fetch todos
        todos_url = "{}/todos?userId={}".format(base_url, employee_id)
        with urlopen(todos_url) as response:
            todos = json.loads(response.read().decode())

    except HTTPError as e:
        if e.code == 404:
            print("Error: Employee with ID {} not found.".format(employee_id))
        else:
            print("HTTP error: {}".format(e.code))
        sys.exit(1)
    except URLError:
        print("Error: Could not reach the API. Check your internet connection.")
        sys.exit(1)

    total_tasks = len(todos)
    done_tasks = [todo for todo in todos if todo.get("completed")]
    number_done = len(done_tasks)

    # First line
    print("Employee {} is done with tasks({}/{}):".format(employee_name, number_done, total_tasks))

    # Completed  note: tab + space before the titletasks 
    for task in done_tasks:
        print("\t {}".format(task.get('title')))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    get_employee_todo_progress(emp_id)
