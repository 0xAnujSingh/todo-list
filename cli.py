from todo import TodoList
from termcolor import colored

## Interface
print("ToDo Application Commands List\n")
print("add: To add new item")
print("list: To display all items")
print("done: To mark an item as done")
print("flush: To flush the list")
print("exit: To close the application\n")

lists = {
    'task': TodoList('Task List')
}

activeList = lists['task']

def startApp():
    global activeList

    while True:
        print("\n", end="")
        print(activeList.name, end=": ")
        cmd = input(colored("Enter A Command: ", "green"))

        if cmd == "new":
            name = input('List Name: ')
            
            if name in lists:
                print("List with this name already exists.")
                continue

            lists[name] = TodoList(name)

        elif cmd == "change":
            listName = input('Which List?')
            
            if listName not in lists:
                print('List does not exist')
                continue

            activeList = lists[listName]

        elif cmd == "add":
            item = input("Enter Item: ")
            activeList.add(item)

        elif cmd == "list":
            activeList.display()

        elif cmd == "done":
            item = int(input("Which Item? "))
            activeList.done(item)

        elif cmd == "undo":
            item = int(input("Which Item? "))
            activeList.undo(item)

        elif cmd == "flush":
            activeList.flush()

        elif cmd == "exit":
            break

        else:
            print("Invalid Command. Please try from the given options")

startApp()
