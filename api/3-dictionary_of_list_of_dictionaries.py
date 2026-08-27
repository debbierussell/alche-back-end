#!/usr/bin/python3
"""
3-dictionary_of_list_of_dictionaries.py
Exports all employees' TODO lists to a JSON file.
Usage: python3 3-dictionary_of_list_of_dictionaries.py
"""

import json
import sys
from collections import OrderedDict
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def fetch_all_employees_todos():
    """Fetch all users and their todos, export to JSON."""
    base_url = "https://jsonplaceholder.typicode.com"

    try:
        # Fetch all users
        users_url = "{}/users".format(base_url)
        with urlopen(users_url) as response:
            users = json.loads(response.read().decode())
    except (HTTPError, URLError):
        sys.stderr.write("Error: Could not fetch users from API.\n")
        sys.exit(1)

    all_data = OrderedDict()

    for user in users:
        user_id = user.get("id")
        username = user.get("username")

        try:
            todos_url = "{}/todos?userId={}".format(base_url, user_id)
            with urlopen(todos_url) as response:
                todos = json.loads(response.read().decode())
        except (HTTPError, URLError):
            sys.stderr.write("Error: Could not fetch todos for user {}.\n"
                             .format(user_id))
            continue

        task_list = []
        for todo in todos:
            task_dict = OrderedDict([
                ("username", username),
                ("task", todo.get("title")),
                ("completed", todo.get("completed"))
            ])
            task_list.append(task_dict)

        all_data[str(user_id)] = task_list

    # Write to file in current working directory
    filename = "todo_all_employees.json"
    with open(filename, "w") as f:
        json.dump(all_data, f)


if __name__ == "__main__":
    fetch_all_employees_todos()
