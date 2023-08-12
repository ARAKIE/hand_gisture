from flask import g
import sqlite3 

def connect_to_database():
    sql = sqlite3.connect('C:/Users/3rakey/Documents/hand_recogintion/handrecogintion.db')
    sql.row_factory = sqlite3.Row
    return sql 


def get_database():
    if not hasattr(g, 'handrecogintion_db'):
        g.handrecogintion_db = connect_to_database()
    return g.handrecogintion_db


