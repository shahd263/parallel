import mysql.connector
from mysql.connector import Error

class DbConnector:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = '2003'
        self.dbname = 'taskreminder'
        self.conn=None

    def open_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbname
            )
            if self.conn.is_connected():
                return True
        except Error as e:
            print("Error:", e)
            return False

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.close()


    def select(self, tableName, attribute):
        try:
            cursor = self.conn.cursor()
           
            qry = f"SELECT {attribute} FROM {tableName}"
            cursor.execute(qry)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print("Error:", e)
            return None
        
   
    def insert(self, tableName, data):
        try:
          cursor = self.conn.cursor()  
          columns = ', '.join(data.keys())
          values = ', '.join(['%s'] * len(data))  
          qry = f"INSERT INTO {tableName} ({columns}) VALUES ({values})"
          cursor.execute(qry, tuple(data.values()))
          self.conn.commit() 
          cursor.close()
        except Error as e:
          print("Error:", e)


    def delete(self, tableName, row_id): 
      try:
           cursor = self.conn.cursor() 
           qry = f"DELETE FROM {tableName} WHERE id = %s"
           cursor.execute(qry, (row_id,)) 
           self.conn.commit() 
           return True
      except mysql.connector.Error as e:
           print("Error:", e)
           return False 
    

    def update(self, tableName, row_id, updates): 
        try:
             cursor = self.conn.cursor() 
             sett= ', '.join([f"{col} = %s" for col in updates.keys()])
             qry = f"UPDATE {tableName} SET {sett} WHERE id = %s" 
             params = list(updates.values()) + [row_id] 
             cursor.execute(qry, params) 
             self.conn.commit() 
             return True 
        except mysql.connector.Error as e: 
            print("Error:", e)
            return False 
