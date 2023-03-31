import sqlite3
from contextlib import closing

class A_database():
    def __init__(self, db_name, table_name):
        self.file_name = db_name
        self.table_name = table_name
        self.connection = sqlite3.connect(self.file_name)
    
    ############################
    def Delete_All_record(self):
        connection = sqlite3.connect(self.file_name)
        cursor = connection.cursor()
        command = "DELETE FROM " + self.table_name + ";"  
        cursor.execute(command,)
    
        connection.commit()
        cursor.close()
        connection.close()
    ############################   
    def Select_all(self):
        cur = self.connection.cursor()
        command = "SELECT * FROM " + self.table_name
        res = cur.execute(command)

        return res.fetchall()
    ############################
    def Create_table(self):
        connection = sqlite3.connect(self.file_name)
        command = "CREATE TABLE " + self.table_name + "("+ "i integer,"+ "Description TEXT,"+ "int_ID TEXT,"+ "IP TEXT,"+ "Profile TEXT,"+ "Int_type TEXT,"+ "Router_Name TEXT,"+ "int_Name TEXT)" 
        cur = connection.execute(command)
      
        connection.commit()
        cur.close()
        connection.close()
    ############################
    def Insert_record(self, a_record):
        command = "INSERT INTO "+ self.table_name + " VALUES (?,?,?,?,?,?,?,?,?,?)" 
        self.cur = self.connection.execute(command, (a_record[0], a_record[1], a_record[2], a_record[3], a_record[4], a_record[5], a_record[6],a_record[7],a_record[8],a_record[9]))
       
        self.connection.commit()
        #cur.close()
        #connection.close()  
    
    ############################
    def Close_connect(self):
        #self.cur.close()
        self.connection.close()
    
    ############################
    def Select_specific_columns(self):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute('''
                       SELECT "seat_id", "price"  FROM "Seat" 
                       ''')
        result = cursor.fetchall()
        connection.close()
        cursor.close()
        return result
    ############################
    def Select_with_conditions(self):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute('''
                       SELECT "seat_id", "price"  FROM "Seat" WHERE "price">80
                       ''')
        #"SELECT name, species, tank_number FROM fish WHERE name = ?", (target_fish_name,),
        result = cursor.fetchall()
        connection.close()
        cursor.close()
        return result
        '''
        with closing(sqlite3.connect("aquarium.db")) as connection:
            with closing(connection.cursor()) as cursor:
                rows = cursor.execute("SELECT 1").fetchall()
                print(rows)
        '''
    ############################   
    def Update_value(self):
        connection = sqlite3.connect("cinema.db")
        connection.execute('''
                       UPDATE "Seat" SET "taken" = "0" WHERE "seat_id" = "A1"
                       ''')
        connection.commit()
        connection.close()
        #new_tank_number = 2
        #moved_fish_name = "Sammy"
        #cursor.execute(
        #    "UPDATE fish SET tank_number = ? WHERE name = ?",
        #    (new_tank_number, moved_fish_name))
    ############################
    def Delete_record(self):
        connection = sqlite3.connect("cinema.db")
        connection.execute('''
                       DELETE FROM "Seat" WHERE "seat_id" = "A1" OR "seat_id" = "A2"
                       ''')
        connection.commit()
        connection.close()
        #released_fish_name = "Sammy"
        #cursor.execute(
        #    "DELETE FROM fish WHERE name = ?",
        #    (released_fish_name,))
      
    def Update_value_parameter(self, occupied, seat_id):
        connection = sqlite3.connect("cinema.db")
        connection.execute('''
                       UPDATE "Seat" SET "taken" = ? WHERE "seat_id" = ?
                       ''', [occupied, seat_id])
        connection.commit()
        connection.close()
        
    ############################

