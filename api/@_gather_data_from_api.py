#!/usr/bin/python3
"""
Gather data from an API and display TODO list progress for a given employee ID.
Uses requests module to fetch user and todo data from JSONPlaceholder API.
"""

import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        sys.exit(1)

    user_url = "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    todos_url = "https://jsonplaceholder.typicode.com/todos?userId={}".format(employee_id)

    try:
        user_response = requests.get(user_url)
        user_response.raise_for_status()
        user_data = user_response.json()
        employee_name = user_data.get('name')

        todos_response = requests.get(todos_url)
        todos_response.raise_for_status()
        todos_data = todos_response.json()

    except requests.exceptions.RequestException:
        sys.exit(1)

    if not employee_name:
        sys.exit(1)

    total_tasks = len(todos_data)
    done_tasks = [todo for todo in todos_data if todo.get('completed')]
    number_done = len(done_tasks)

    print("Employee {} is done with tasks({}/{}):".format(employee_name, number_done, total_tasks))
    for task in done_tasks:
        print("\t {}".format(task.get('title')))
