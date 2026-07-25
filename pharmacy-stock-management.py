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

def ask_number(question):
    # keeps asking until the user types a real number
    while True:
        answer = input(question)
        if answer.isdigit():
            return int(answer)
        print("Please type a number.")


def ask_date(question):
    # keeps asking until the user types a real date
    while True:
        answer = input(question)
        try:
            return datetime.strptime(answer, "%d/%m/%Y").date()
        except ValueError:
            print("Wrong format. Please use dd/mm/yyyy.")


def ask_price(question):
    # keeps asking until the user types a real price (whole number or decimal)
    while True:
        answer = input(question)
        try:
            price = float(answer)
            if price < 0:
                print("Price cannot be negative.")
                continue
            return price
        except ValueError:
            print("Please type a number.")


def add_medicine():
    conn = connect()
    cur = conn.cursor()
    again = "Y"
    while again.upper() == "Y":
        name = input("Enter the name of the medicine: ")
        quantity = ask_number("Enter the quantity: ")
        price = ask_price("Enter the price: ")
        expiry = ask_date("Enter the expiry date (dd/mm/yyyy): ")
        cur.execute("INSERT INTO medicines (name, quantity, price, expiry_date) VALUES (%s, %s, %s, %s)",
                    (name, quantity, price, expiry))
        conn.commit()
        print(name + " added successfully!")
        again = input("Do you want to add another? (Y/N): ")
    cur.close()
    conn.close()


def view_stock():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, quantity, price, expiry_date FROM medicines ORDER BY name")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("The inventory is empty.")
    else:
        print("\nID | Name | Quantity | Price | Expiry date")
        print("-" * 45)
        for row in rows:
            print(str(row[0]) + " | " + row[1] + " | " + str(row[2]) + " | " +
                  str(row[3]) + " | " + row[4].strftime("%d/%m/%Y"))
    cur.close()
    conn.close()


def search_medicine():
    name = input("Enter the medicine name to search: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, quantity, price, expiry_date FROM medicines WHERE name LIKE %s",
                ("%" + name + "%",))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("No medicine found with that name.")
    else:
        for row in rows:
            print(str(row[0]) + " | " + row[1] + " | quantity: " + str(row[2]) +
                  " | price: " + str(row[3]) + " | expires: " + row[4].strftime("%d/%m/%Y"))
    cur.close()
    conn.close()
