import sqlite3

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.create_user_table()
        self.create_todo_table()     
        self.create_tags_table()

    def create_tags_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Tags" (
          id INTEGER PRIMARY KEY,
          Tag TEXT
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_todo_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Todo" (
          id INTEGER PRIMARY KEY,
          Title TEXT,
          Description TEXT,
          _is_done boolean DEFAULT 0,
          _is_deleted boolean DEFAULT 0,
          CreatedOn Date DEFAULT CURRENT_DATE,
          DueDate Date,
          Priority INTEGER,
          Category TEXT,
          UserId INTEGER FOREIGNKEY REFERENCES User(_id)
        );
        """
        self.conn.execute(query)

    def create_user_table(self):
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

    def create(self, text, description):
        query = f'insert into {self.TABLENAME} ' \
                f'(Title, Description) ' \
                f'values ("{text}","{description}")'
        
        result = self.conn.execute(query)
        print(result.lastrowid)
        # return result 
        # uncomment above line and check what error occurs and why
        return result.lastrowid

    def list_items(self, where_clause=""):
        test_query = f"SELECT * " \
                f"from {self.TABLENAME} "
        print(test_query)
        test_result_set = self.conn.execute(test_query).fetchall()
        print(test_result_set)
        query = f"SELECT id, Title, Description, _is_done " \
                f"from {self.TABLENAME} WHERE _is_deleted != {1} " + where_clause
        print (query)
        result_set = self.conn.execute(query).fetchall()
        print(result_set)
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result