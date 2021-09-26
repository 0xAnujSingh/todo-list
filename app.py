from flask import Flask, request, jsonify
from todo import TodoList

app = Flask(__name__)

lists = {
    'task': TodoList('Task List')
}

activeList = lists['task']

## Create a new list
@app.route('/list/new/<name>', methods=['POST'])
def newList(name):
    if name in lists:
        return "List with this name already exists."

    lists[name] = TodoList(name)

    return "list added"

## Change the active list
@app.route('/list/change/<name>')
def changeList(name):
    if name not in lists:
        return 'List does not exist'

    activeList = lists[name]

    return 'List change'

## Add item to the list
@app.route('/list/add/<item>')
def add(item):
    activeList.add(item)
    return 'Item added'

## List items in the list
@app.route('/list')
def list():
    res = ''

    res += activeList.name + '\n'

    index = 0
    for item in activeList.items:
        res += f'[{index}][{item.done}] {item.msg}\n'
        index += 1

    return res
       
## Mark an item as done
@app.route('/list/done/<item>')
def done(item):
    try:
        activeList.done(int(item))
    except:
        return 'something went wrong'
    return 'item done'


## Mark an item as not done
@app.route('/list/undo/<item>')
def undo(item):
    try:
        activeList.undo(int(item))
    except:
        return 'something went wrong'
    return 'Item un-done'


## Flush a list
@app.route('/list/flush')
def flush():
    activeList.flush()
    return 'flush'