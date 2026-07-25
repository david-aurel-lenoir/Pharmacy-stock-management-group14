# Pharmacy Stock Management System
# Group 14 - Beginner Python project
# Database: MySQL (Aiven cloud)
 
import mysql.connector
from datetime import datetime, timedelta
 
# ---------- database connection info ----------
HOST = "mysql-38078a6a-alustudent-15.a.aivencloud.com"
PORT = 23193
USER = "avnadmin"
PASSWORD = "AVNS_T_4s-plq9OVOiSGcOQZ"
DATABASE = "defaultdb"
 
LOW_STOCK = 10           # quantity at or below this = low stock
DAYS_BEFORE_EXPIRY = 30  # warn when a medicine expires within this many days

def connect():
    # opens the connection to our online MySQL database
    return mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        use_pure=True
    )


def setup_database():
    # creates the tables the first time the program runs
    conn = connect()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS medicines (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    quantity INT,
                    price DECIMAL(10,2),
                    expiry_date DATE)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    description VARCHAR(255),
                    request_date DATE)""")
    conn.commit()
    cur.close()
    conn.close()
