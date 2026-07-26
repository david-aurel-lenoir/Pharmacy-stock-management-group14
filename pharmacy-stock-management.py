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
    cur.execute("SELECT id, name, quantity, price, expiry_date FROM medicines ORDER BY id")
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

def update_medicine():
    view_stock()
    med_id = ask_number("Enter the ID of the medicine you want to update: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT name, quantity FROM medicines WHERE id = %s", (med_id,))
    row = cur.fetchone()
    if row is None:
        print("That ID does not exist.")
        cur.close()
        conn.close()
        return
 
    print("Press N to change the name, Q for the quantity, P for the price")
    choice = input("Your choice: ").upper()
 
    if choice == "N":
        new_name = input("Enter the new name: ")
        cur.execute("UPDATE medicines SET name = %s WHERE id = %s", (new_name, med_id))
        print("Name updated successfully!")
    elif choice == "Q":
        action = input("Press A to add quantity or S to deduct quantity: ").upper()
        amount = ask_number("Enter the amount: ")
        if action == "A":
            new_quantity = row[1] + amount
        elif action == "S":
            new_quantity = row[1] - amount
            if new_quantity < 0:
                print("You cannot deduct more than what is in stock.")
                cur.close()
                conn.close()
                return
        else:
            print("Wrong choice.")
            cur.close()
            conn.close()
            return
        cur.execute("UPDATE medicines SET quantity = %s WHERE id = %s", (new_quantity, med_id))
        print(row[0] + "'s quantity updated successfully! New quantity: " + str(new_quantity))
    elif choice == "P":
        new_price = ask_price("Enter the new price: ")
        cur.execute("UPDATE medicines SET price = %s WHERE id = %s", (new_price, med_id))
        print("Price updated successfully!")
    else:
        print("Wrong choice.")
 
    conn.commit()
    cur.close()
    conn.close()
 
 
def delete_medicine():
    view_stock()
    med_id = ask_number("Enter the ID of the medicine you want to delete: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT name, quantity FROM medicines WHERE id = %s", (med_id,))
    row = cur.fetchone()
    if row is None:
        print("That ID does not exist.")
    else:
        if row[1] > 0:
            confirm = input("There are still " + str(row[1]) + " left in stock. Delete anyway? (Y/N): ")
            if confirm.upper() != "Y":
                print("Deletion cancelled.")
                cur.close()
                conn.close()
                return
        cur.execute("DELETE FROM medicines WHERE id = %s", (med_id,))
        # renumber the remaining medicines so ids stay contiguous (1, 2, 3, ...)
        cur.execute("""UPDATE medicines m
                        JOIN (SELECT id, ROW_NUMBER() OVER (ORDER BY id) AS new_id
                              FROM medicines) t ON m.id = t.id
                        SET m.id = t.new_id""")
        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM medicines")
        next_id = cur.fetchone()[0]
        cur.execute("ALTER TABLE medicines AUTO_INCREMENT = %s", (next_id,))
        conn.commit()
        print(row[0] + " deleted successfully!")
    cur.close()
    conn.close()

 
def medicine_alerts():
    today = datetime.now().date()
    soon = today + timedelta(days=DAYS_BEFORE_EXPIRY)
    conn = connect()
    cur = conn.cursor()
 
    print("\n--- EXPIRED MEDICINES ---")
    cur.execute("SELECT name, quantity, expiry_date FROM medicines WHERE expiry_date < %s", (today,))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("None")
    for row in rows:
        print(row[0] + " | expired on " + row[2].strftime("%d/%m/%Y") + " | quantity: " + str(row[1]))
 
    print("\n--- EXPIRING SOON ---")
    cur.execute("SELECT name, quantity, expiry_date FROM medicines WHERE expiry_date >= %s AND expiry_date <= %s",
                (today, soon))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("None")
    for row in rows:
        print(row[0] + " | expires on " + row[2].strftime("%d/%m/%Y") + " | quantity: " + str(row[1]))
 
    print("\n--- LOW STOCK ---")
    cur.execute("SELECT name, quantity FROM medicines WHERE quantity <= %s", (LOW_STOCK,))
    rows = cur.fetchall()
    if len(rows) == 0:
        print("None")
    for row in rows:
        print(row[0] + " | only " + str(row[1]) + " left")
 
    cur.close()
    conn.close()
 

def make_request():
    name = input("Name of the medicine being requested: ")
    description = input("Write a brief description: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO requests (name, description, request_date) VALUES (%s, %s, %s)",
                (name, description, datetime.now().date()))
    conn.commit()
    cur.close()
    conn.close()
    print("Request made successfully!")

 
def inventory_report():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(quantity), SUM(quantity * price) FROM medicines")
    row = cur.fetchone()
    total_meds = row[0]
    total_items = row[1]
    total_value = row[2]
    if total_items is None:
        total_items = 0
    if total_value is None:
        total_value = 0
 
    print("\n===== INVENTORY REPORT =====")
    print("Date: " + datetime.now().strftime("%d/%m/%Y"))
    print("Different medicines: " + str(total_meds))
    print("Total items in stock: " + str(total_items))
    print("Total stock value: " + str(total_value))
 
    print("\nRequests made:")
    cur.execute("SELECT name, description, request_date FROM requests")
    rows = cur.fetchall()
    if len(rows) == 0:
        print("None")
    for row in rows:
        print("- " + row[0] + " (" + row[2].strftime("%d/%m/%Y") + "): " + row[1])
    print("============================")
    cur.close()
    conn.close()
 
 
def main():
    setup_database()
    print("Welcome to the Pharmacy Stock Management System")
    running = True
    while running:
        print("\n***** What do you want to do? *****")
        print("1. Add medicine")
        print("2. View medicine stocks")
        print("3. Search medicine")
        print("4. Update medicine")
        print("5. Delete medicine")
        print("6. Medicine alerts")
        print("7. Requests")
        print("8. Reports")
        print("9. Exit")
        choice = input("Choose an option (1-9): ")
 
        if choice == "1":
            add_medicine()
        elif choice == "2":
            view_stock()
        elif choice == "3":
            search_medicine()
        elif choice == "4":
            update_medicine()
        elif choice == "5":
            delete_medicine()
        elif choice == "6":
            medicine_alerts()
        elif choice == "7":
            make_request()
        elif choice == "8":
            inventory_report()
        elif choice == "9":
            print("Goodbye!")
            running = False
        else:
            print("Wrong option, please choose between 1 and 9.")
 
 
main()
