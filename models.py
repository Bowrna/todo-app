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
        query = f'insert into {self.TABLENAME}' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'
        result = self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        return result.lastrowid

    def list_items(self, where_clause=""):
        fields = ['id', 'Title', 'Description', 'Is_done']
        todo = namedtuple('todo', fields)
        query = f"SELECT id, Title, Description, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        result_set = self.conn.execute(query).fetchall()
        result = [todo(*column)._asdict()
                  for i, column in enumerate(result_set)]
        return result

    def delete(self, id):
        # Missing out space can lead to error. Consider using ORM
        query = f'UPDATE {self.TABLENAME} ' \
                f'SET _is_deleted = {1} ' \
                f'WHERE id = {id}'
        print(query)
        result = self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        return result.lastrowid
    
    def update(self, id, update_params):
        set_query = ", ".join([f'{column} = {value}'
                     for column, value in update_params.items()])
        query = f'UPDATE {self.TABLENAME} ' \
                f'SET {set_query} ' \
                f'WHERE id = {id}'
        result = self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        return self.get_by_id(id)

    def get_by_id(self, id):
        where_clause = f'AND id={id}'
        self.list_items(where_clause=where_clause)
        

class User:
  TABLENAME = "User"
  def __init__(self):
      self.conn = sqlite3.connect('todo.db')
      self.cursor = self.conn.cursor()

  def create_user(self, email, username):
        query = f'insert into {self.TABLENAME}' \
                f'(Email, Name) ' \
                f'values ("{email}","{username}")'
        result = self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        return result.lastrowid