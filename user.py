from dbConnector import DbConnector
import threading
lock = threading.Lock()


class User:
    _next_id = 1  # Class-level variable to keep track of the next ID

    def __init__(self, name: str, mail: str, password: str):
        self._name = name
        self._password = password
        self._mail = mail
      
        db_connector = DbConnector()
        db_connector.open_connection()
        data = {
            "name": self._name,
            "email": self._mail,
            "password": self._password
        }

        lock.acquire()
        db_connector.insert("users",data)
        db_connector.close_connection()
        lock.release()
        db_connector.close_connection()


    def _str_(self):
        return f"User(name='{self._name}', mail='{self._mail}')"
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if any(char.isdigit() for char in name):  # Check if name contains any digits
            raise ValueError("Name cannot contain numbers.")
        self._name = name

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self._password = password

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, mail: str):
        if "@" not in mail or "." not in mail.split("@")[-1]:
            raise ValueError("Invalid email address.")
        self._mail = mail