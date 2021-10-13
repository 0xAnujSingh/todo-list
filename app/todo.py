import sqlite3
from app.db import conn

class TodoItem:
    def __init__(self, id, description, list, createdAt, done = False):
        self.msg = msg
        self.done = done

    def complete(self):
        self.done = True

    def status(self):
        print(self.done, self.msg)

    ## Store a new todo item
    @classmethod
    def new(cls, desc, list):
        pass

    ## Get all the todo items for a given list id
    @classmethod
    def findByList(cls, listId):
        pass

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
            cursor.execute("SELECT * FROM `list` WHERE `id` = ?", (cursor.lastrowid, ))
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

        print("item added")

    def display(self):
        print(self.name)

        index = 0
        for item in self.items:
            print(index, item.done, item.msg)
            index += 1

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