import threading
import time
lock = threading.Lock()
from dbConnector import DbConnector
import login 

class Task:
    _next_id = 1  # Class-level variable to keep track of the next ID
    
    def __init__(self, taskName, dateTask, timeTask):
        self._id = Task._next_id
        Task._next_id += 1
        self.taskName = taskName
        self.timeTask = timeTask
        self.dateTask = dateTask
        userid = login.current_user
        db_connector = DbConnector()
        db_connector.open_connection()
        data = {
            "nameTask": self.taskName,
            "dateT": self.dateTask,
            "timeT": self.timeTask, 
            "userID"  : userid
        }
        lock.acquire()
        db_connector.insert("tasks",data)
        db_connector.close_connection()
        lock.release()
    def get_remaining_time(self):
        current_time = time.time()
        task_time = time.strptime(self.timeTask, "%H:%M:%S")
        task_time = time.mktime(task_time)
        remaining_time = task_time - current_time
        return remaining_time

    def run(self):
        remaining_time = self.get_remaining_time()
        time.sleep(remaining_time)
         
        lock.acquire()
        try:
           db_connector = DbConnector()
           db_connector.open_connection()
           try:
            result =db_connector.select("tasks",self.id)
           
           except Exception as e:
            return
           #call methd send mail send task id for it
           
           db_connector.delete("Tasks",self._id)
           db_connector.close_connection()
        finally:
            lock.release()