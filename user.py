from dbWrapper import *

class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def save_to_db(self):
        cur = get_db()
        try:
            output = cur.execute('select max(u_id) from users').fetchone()

            if output[0] >= 1: 
                newId = output[0] + 1
            else:
                newId = 1
            print ("newId %s" %newId)
            out = cur.execute('INSERT INTO users (u_id, u_name, password) VALUES (?, ?, ?)', (newId, self.username, self.password))
            print (out)
        except Exception as e:
            print("Error %s" %e)
            raise DBConnectionError(e)

        finally:
            cur.commit()
            close_db_connection()
    
    @classmethod
    def find_by_username(cls, username):
        print (dir(get_db()))
        cur = get_db()
        
        try:
            data = cur.execute('SELECT * FROM users WHERE u_name=?', (username,)).fetchone()
            if data:
                return cls(data[1], data[2])
        finally:
            close_db_connection()
