import argparse
import json
import os
from datetime import date, timedelta

data_file = "habits.json"

def load_data():
    if not os.path.exists(data_file):
        return {"habits": {}}
    with open(data_file, "r") as f:
        return json.load(f)

def save_data(data):
    with open(data_file, "w") as f:
        json.dump(data, f, indent=2)

def add_habit(name):
    data = load_data()
    if name in data["habits"]:
        print(f"Habit '{name}' already exists")
        return
    data["habits"][name] = {"created": str(date.today()), "logs": []}
    save_data(data)
    print(f"Added habit: {name}")

def mark_habit(name):
    data = load_data()
    today = str(date.today())
    if name not in data["habits"]:
        print(f"Habit '{name}' not found")
    if today in data["habits"][name]["logs"]:
        print(f"Habit '{name}' already done today")
        return
    data["habits"][name]["logs"].append(today)
    save_data(data)
    print(f"Marked '{name}' done today.")

def list_habits():
    data = load_data()
    today = str(date.today())
    for name, habit in data["habits"].items():
        status = "■" if today in habit["logs"] else "□"
        print(f"{name} : {status}")

def show(name, row_length=7):
    data = load_data()
    if name not in data["habits"]:
        print(f"Habit '{name}' not found.")
        return
    
    habit = data["habits"][name]
    created = date.fromisoformat(habit["created"])
    today = date.today()
    days_total = (today - created).days + 1 # Including today
    logs = set(habit["logs"])

    squares = []
    for i in range(days_total):
        day = created + timedelta(days=i)
        symbol = "■" if str(day) in logs else "□"
        squares.append(symbol)
    for i in range(0, len(squares), int(row_length)):
        print (" ".join(squares[i:i+int(row_length)]))

# Argument parsing
def main():
    parser = argparse.ArgumentParser(description = "simple habit tracking")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("name")
    show_parser.add_argument("row_length")

    done_parser = subparsers.add_parser("mark")
    done_parser.add_argument("name")


    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "add":
        add_habit(args.name)
    elif args.command == "list":
        list_habits()
    elif args.command == "show":
        show(args.name, args.row_length)
    elif args.command == "mark":
        mark_habit(args.name)

        