import sqlite3

def connect():
    # connect to database
    DATABASE_NAME = "odk-mailer"
    con = sqlite3.connect(f"odk_mailer/{DATABASE_NAME}.db")
    
    print(con.total_changes)