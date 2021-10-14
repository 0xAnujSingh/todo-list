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

    def undo(self):
        self.undo = undo

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
            cursor.execute("SELECT `id`, `description`, `done`, `list_id`, `created_at` FROM item WHERE list_id = ?;",(listId, ))

            data = cursor.fetchall()
        except:
            raise Exception("error: unable to fetch data")
        finally:
            cursor.close()

        for item in data:
            result.append(cls(item[0], item[1], item[2], item[3], item[4]))

        return result

class TodoList:
    def __init__(self, listId, title, description, createdAt):
        self.id = listId
        self.title = title
        self.description = description
        self.createdAt = createdAt

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

    @property
    def items(self):
        return TodoItem.findByList(self.id)

    def add(self, msg):
        item = TodoItem.new(msg, self.id)

        return item

    def done(self, idx):
        try:
            item = self.items[idx]
            item.complete()
            print("Item marked as Done!")
        except IndexError:
            print("Index not found")

    def undo(self, idx):
        try:
            item = self.items[idx]
            item.done = False
            print("Item marked as Not Done!")
        except IndexError:
            print("Index not found")

    def flush(self):
        self.items.clear()
        print("flush")