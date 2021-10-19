from flask import Flask
app = Flask(__name__)

@app.route('/lists', methods = ['POST'])
def createList():
    return {
        "title" : "Lists"
    }

@app.route('/lists')
def getAllLists():
    return {
        "description" : "Lists"
    }

@app.route('/lists/<listId>')
def getListById(listId):
    return {
        "listId" : listId
    }
    

@app.route('/lists/<listId>/items', methods = ['POST'])
def createItem(listId):
    return {
        "listId": listId
    }

@app.route('/lists/<listId>/items')
def getAllItems(listId):
    return {
        "listId" : listId
    }

@app.route('/lists/<listId>/items/<itemId>')
def getItemById(listId, itemId):
    return {
        "listId": listId,
        "itemId" : itemId
    }

@app.route('/lists/<listId>/items/<itemId>/done')
def done(listId, itemId):
    return {
        "listId": listId,
        "itemId" : itemId
    }

@app.route('/lists/<listId>/items/<itemId>/undo')
def undo(listId, itemId):
    return {
        "listId": listId,
        "itemId" : itemId
    }
