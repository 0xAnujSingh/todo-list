from flask import Flask, request
from app.todo import TodoItem, TodoList

app = Flask(__name__)

@app.route('/lists', methods = ['POST'])
def createList():
    data = request.json

    title = data['title']
    description = data['description']

    newList = TodoList.new(title, description)

    return newList.toJSON()

@app.route('/lists')
def getAllLists():
    lists = TodoList.getAll()
    result = []

    for li in lists:
        result.append(li.toJSON())

    return {
        "lists": result
    }

@app.route('/lists/<listId>')
def getListById(listId):
    lists = TodoList.findById(listId)
    result = []

    for li in lists:
        result.append(li.toJSON())

    return {
        "listId" : result
    }
    

@app.route('/lists/<listId>/items', methods = ['POST'])
def createItem(listId):
    items = TodoItem.new(listId)

    return items.toJSON()

@app.route('/lists/<listId>/items')
def getAllItems(listId):
    items = TodoItem.findByList(listId)
    result = []
    for item in items:
        result.append(item.toJSON())

    return {
        "listId" : result
    }

@app.route('/lists/<listId>/items/<itemId>')
def getItemById(listId, itemId):
    items = TodoList.findById(listId)
    result = []

    for item in items:
        result.append(item.toJSON())

    return {
        "listId": listId,
        "itemId" : itemId
    }

@app.route('/lists/<listId>/items/<itemId>/done')
def done(listId, itemId):
    item = TodoItem.findById(itemId)

    if (item is None):
        return { "error": "Todo Item not found" }

    if (item.listId != int(listId)):
        return { "error": "This item does not belong in this list" }

    item.complete()

    return item.toJSON()

@app.route('/lists/<listId>/items/<itemId>/undo')
def undo(listId, itemId):
    item = TodoItem.findById(itemId)
    
    if (item is None):
        return {"error": "Todo item not found"} 

    if (item.listId != int(listId)):
        return {"error" : "This item does not belong in this list"}

    item.undo()
    return item.toJSON()
