import sqlite3
from collections import namedtuple

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_todo_table()     
        self.create_tags_table()

    def create_tags_table(self):
        print("Creating tags table")
        query = """
        CREATE TABLE IF NOT EXISTS "Tags" (
          id INTEGER PRIMARY KEY,
          Tag TEXT,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_todo_table(self):
        print("Creating todo table")
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done INTEGER NOT NULL DEFAULT 0 CHECK(_is_done in (0,1)),
          _is_deleted INTEGER NOT NULL DEFAULT 0 CHECK(_is_deleted in (0,1)),
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          Priority INTEGER,
          Category TEXT,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
        print("Creating user table")
        query = """
        CREATE TABLE IF NOT EXISTS "User" (
          id INTEGER PRIMARY KEY,
          Email TEXT,
          Name TEXT
        );
        """
        self.conn.execute(query)

class ToDoModel:
    TABLENAME = "Todo"

    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

    def create(self, text, description):
        print(text)
        print(description)
        query = f'insert into {self.TABLENAME}' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'
        print(query)
        result = self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        return result.lastrowid

    def list_items(self, where_clause=""):
        # test_query = f"SELECT * " \
        #         f"from {self.TABLENAME} "
        # print(test_query)
        # test_result_set = self.cursor.execute(test_query).fetchall()
        # print(test_result_set)
        fields = ['id', 'Title', 'Description', 'Is_done']
        todo = namedtuple('todo', fields)
        query = f"SELECT id, Title, Description, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        result_set = self.conn.execute(query).fetchall()
        result = [todo(*column)._asdict()
                  for i, column in enumerate(result_set)]
        return result

