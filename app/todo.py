import sqlite3
from app.db import conn

class TodoItem:
    def __init__(self, itemId, description, listId, createdAt, done = False):
        self.id = itemId
        self.done = done
        self.description = description
        self.listId = listId
        self.createdAt = createdAt

    def complete(self):
        self.done = True

        cursor = conn.cursor()
        try:
            ##where 0 = false, 1 = true in dbms
            cursor.execute("UPDATE item SET done = 1 WHERE id = ?;", (self.id, ))

            conn.commit()
        except:
            raise Exception("item with this id doesn't exists")
        finally:
            cursor.close()

    def undo(self):
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE item SET done = 0 WHERE id = ?;", (self.id, ))

            conn.commit()
        except:
            raise Exception("item with this id doesn't exists")
        finally:
            cursor.close()


    ## Store a new todo item
    @classmethod
    def new(cls, description, listid):
        cursor = conn.cursor()
        data = None

        try:
            cursor.execute("INSERT INTO item(`description`, `list_id`) VALUES (?, ?);", (description, listid))
            cursor.execute("SELECT  `id`, `description`, `done`, `list_id`, `created_at` FROM `item` WHERE `id` = ?", (cursor.lastrowid, ))
            data = cursor.fetchone()

            conn.commit()
        except:
            raise Exception("item with this name already exists")
        finally:
            cursor.close()

        return cls(data[0], data[1], data[2], data[3], data[4])        

    ## Get all the todo items for a given list id
    @classmethod
    def findByList(cls, listId):

        cursor = conn.cursor()
        result = []
        data = None

        try:
            cursor.execute("SELECT `id`, `description`, `done`, `list_id`, `created_at` FROM `item` WHERE list_id = ?;",(listId, ))

            data = cursor.fetchall()
        except:
            raise Exception("error: unable to fetch data")
        finally:
            cursor.close()

        for item in data:
            result.append(cls(item[0], item[1], item[2], item[3], item[4]))

        return result

    @classmethod
    def findById(cls, itemId):
        cursor = conn.cursor()
        data = None

        try:
            cursor.execute("SELECT `id`, `description`, `list_id`, `created_at`, `done` FROM `item` WHERE `id` = ?", (itemId, ))
            data = cursor.fetchone()
            
        except:
            raise Exception("Something Went Wrong while getting item")
        finally:
            cursor.close()

        if data is None:
            return None

        return cls(data[0], data[1], data[2], data[3], data[4])

    def toJSON(self):
        return {
            "id" : self.id,
            "done" : self.done,
            "description" : self.description,
            "listId" : self.listId,
            "createdAt" : self.createdAt
        }


class TodoList:
    def __init__(self, listId, title, description, createdAt):
        self.id = listId
        self.title = title
        self.description = description
        self.createdAt = createdAt

    ## Class Methods

    @classmethod
    def new(cls, title, description):
        cursor = conn.cursor()
        data = None

        try:
            cursor.execute("INSERT INTO list(`title`, `description`) VALUES (?, ?);", (title, description))
            cursor.execute("SELECT `id`, `title`, `description`, `created_at` FROM `list` WHERE `id` = ?", (cursor.lastrowid, ))
            data = cursor.fetchone()

            conn.commit()
        except:
            raise Exception("List with this name already exists")
        finally:
            cursor.close()

        return cls(data[0], data[1], data[2], data[3])

    @classmethod
    def getAll(cls):
        cursor = conn.cursor()
        data = None
        result = []

        try:
            cursor.execute("SELECT * FROM `list`")
            data = cursor.fetchall()

            conn.commit()
        except:
            raise Exception("List with this name already exists")
        finally:
            cursor.close()

        for item in data:
            result.append(cls(item[0], item[1], item[2], item[3]))

        return result

    @classmethod
    def findById(cls, listId):
        cursor = conn.cursor()
        data = None

        try:
            cursor.execute("SELECT * FROM `list` WHERE `id` = ?", (listId, ))
            data = cursor.fetchone()
            
        except:
            raise Exception("Something Went Wrong while getting list")
        finally:
            cursor.close()

        if data is None:
            raise Exception("List not found")

        return cls(data[0], data[1], data[2], data[3])
    ## Properties

    @property
    def items(self):
        return TodoItem.findByList(self.id)

    ## Object Methods

    def add(self, msg):
        item = TodoItem.new(msg, self.id)

        return item

    def done(self, itemId):
        item = TodoItem.findById(itemId)

        if item is None:
            raise Exception("Item not found")

        item.complete()

    def undo(self, itemId):
        item : TodoItem.findById(itemId)

        if item is None:
            raise Exception("Item not found")

        item.undo()
        
    def toJSON(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "createdAt": self.createdAt
        }
        