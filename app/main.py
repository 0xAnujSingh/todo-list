from flask import Flask, request, jsonify
from app.todo import TodoList

app = Flask(__name__)

lists = {
    'task': TodoList('Task List')
}

activeList = lists['task']

@app.route('/ram')
def greet():
    return { "msg": "Jai Shree Ram 🙏🙏" }

## Create a new list
@app.route('/list/new/<name>', methods=['POST'])
def newList(title):
    if title in lists:
        return { "msg" : "List with this title already exists." }, 400

    lists[title] = TodoList(title)

    return { "msg" : "list added" }

## Change the active list
@app.route('/list/change/<name>')
def changeList(name):
    if name not in lists:
        return { 'msg' : 'List does not exist' }, 404

    activeList = lists[name]

    return { 'msg' : 'List change' }

## Add item to the list
@app.route('/list/add/<item>')
def add(item):
    activeList.add(item)
    return { 'msg' : 'Item added' }

## List items in the list
@app.route('/list')
def list():
    res = ''

    res += activeList.name + '\n'

    index = 0
    for item in activeList.items:
        res += f'[{index}][{item.done}] {item.msg}\n'
        index += 1

    return { 'msg' : res }

## Mark an item as done
@app.route('/list/done/<item>')
def done(item):
    try:
        activeList.done(int(item))
    except:
        return { 'msg': 'something went wrong' }, 500
    return { 'msg' : 'item done' }


## Mark an item as not done
@app.route('/list/undo/<item>')
def undo(item):
    try:
        activeList.undo(int(item))
    except:
        return { 'msg': 'something went wrong' }, 500
    return { 'msg' : 'Item un-done' }


## Flush a list
@app.route('/list/flush')
def flush():
    activeList.flush()
    return { 'msg' : 'flush' }