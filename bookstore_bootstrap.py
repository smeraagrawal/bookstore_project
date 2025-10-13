"""
bookstore_bootstrap.py
- Initializes DB (creates database, tables, seed data if absent)
- Then either runs CLI menu or launches Streamlit app.
Usage:
  1) Initialize & run CLI menu:
       python bookstore_bootstrap.py
  2) Initialize & launch Streamlit:
       python bookstore_bootstrap.py --streamlit
Requirements:
  pip install mysql-connector-python pandas streamlit
Make sure MySQL server is running and update DB credentials below if needed.
"""

import mysql.connector
from mysql.connector import errorcode
from datetime import date
import os
import sys
import subprocess
import time

# ---------- CONFIG ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "bookstore"
}
# ----------------------------

def connect_server():
    """Connect to MySQL server (without specifying database)."""
    cfg = DB_CONFIG.copy()
    cfg_no_db = {k: v for k, v in cfg.items() if k != "database"}
    return mysql.connector.connect(**cfg_no_db)

def connect_db():
    """Connect to MySQL server and use bookstore database."""
    return mysql.connector.connect(**DB_CONFIG)

def ensure_database_exists():
    try:
        cnx = connect_server()
        cur = cnx.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET 'utf8mb4'".format(DB_CONFIG['database']))
        cnx.commit()
        cur.close()
        cnx.close()
        print("✅ Database ensured.")
    except Exception as e:
        print("Error creating database:", e)
        sys.exit(1)

def create_tables():
    """Create required tables (IF NOT EXISTS)."""
    statements = [
        """
        CREATE TABLE IF NOT EXISTS Authentication (
            login_id VARCHAR(50) PRIMARY KEY,
            password VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS Customer (
            cust_id INT PRIMARY KEY,
            c_name VARCHAR(100) NOT NULL,
            address VARCHAR(200) NOT NULL,
            phoneno VARCHAR(15) NOT NULL,
            login_id VARCHAR(50),
            FOREIGN KEY (login_id) REFERENCES Authentication(login_id)
               ON DELETE SET NULL ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS Author (
            a_id INT PRIMARY KEY,
            a_name VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS Books (
            b_id INT PRIMARY KEY,
            b_name VARCHAR(100) NOT NULL,
            a_name VARCHAR(100) NOT NULL,
            genre VARCHAR(50) NOT NULL,
            quantity INT NOT NULL CHECK (quantity >= 0),
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0)
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS Staff (
            s_id INT PRIMARY KEY,
            s_name VARCHAR(100) NOT NULL,
            s_phone VARCHAR(15) NOT NULL,
            designation VARCHAR(50) NOT NULL
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS Reports (
            r_no INT PRIMARY KEY,
            b_id INT,
            c_id INT,
            date_of_purchase DATE NOT NULL,
            quantity INT NOT NULL CHECK (quantity > 0),
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            FOREIGN KEY (b_id) REFERENCES Books(b_id) ON DELETE SET NULL ON UPDATE CASCADE,
            FOREIGN KEY (c_id) REFERENCES Customer(cust_id) ON DELETE SET NULL ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """,
        """
        CREATE TABLE IF NOT EXISTS BookAuthor (
            b_id INT,
            a_id INT,
            PRIMARY KEY (b_id, a_id),
            FOREIGN KEY (b_id) REFERENCES Books(b_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (a_id) REFERENCES Author(a_id) ON DELETE CASCADE ON UPDATE CASCADE
        ) ENGINE=InnoDB;
        """
    ]

    try:
        cnx = connect_db()
        cur = cnx.cursor()
        for s in statements:
            cur.execute(s)
        cnx.commit()
        cur.close()
        cnx.close()
        print("✅ Tables created/verified.")
    except Exception as e:
        print("Error creating tables:", e)
        sys.exit(1)

def seed_data_if_empty():
    """Insert seed data only if tables are empty."""
    try:
        cnx = connect_db()
        cur = cnx.cursor()
        # Authentication
        cur.execute("SELECT COUNT(*) FROM Authentication")
        if cur.fetchone()[0] == 0:
            auth_rows = [
                ('chirag', 'admin'),
                ('prachi', '1234'),
                ('tirthraj', '1234'),
                ('smera', '1234'),
                ('ayush', '1234'),
                ('sairaj', '1234'),
                ('sankalp', '1234')
            ]
            cur.executemany("INSERT INTO Authentication (login_id, password) VALUES (%s, %s)", auth_rows)
            print("  - Authentication seeded")

        # Customer
        cur.execute("SELECT COUNT(*) FROM Customer")
        if cur.fetchone()[0] == 0:
            cust_rows = [
                (1, 'chirag', 'Mumbai', '9999999999', 'chirag'),
                (2, 'prachi', 'Pune', '9876543210', 'prachi'),
                (3, 'tirthraj', 'Delhi', '9123456780', 'tirthraj'),
                (4, 'smera', 'Chennai', '9988776655', 'smera'),
                (5, 'ayush', 'Bangalore', '9112233445', 'ayush'),
                (6, 'sairaj', 'Hyderabad', '9900887766', 'sairaj'),
                (7, 'sankalp', 'Ahmedabad', '9877898765', 'sankalp')
            ]
            cur.executemany(
                "INSERT INTO Customer (cust_id, c_name, address, phoneno, login_id) VALUES (%s, %s, %s, %s, %s)",
                cust_rows
            )
            print("  - Customer seeded")

        # Author
        cur.execute("SELECT COUNT(*) FROM Author")
        if cur.fetchone()[0] == 0:
            author_rows = [
                (1, 'J.K. Rowling'),
                (2, 'George Orwell'),
                (3, 'Chetan Bhagat'),
                (4, 'Jane Austen'),
                (5, 'Dan Brown'),
                (6, 'Agatha Christie'),
                (7, 'Paulo Coelho'),
                (8, 'Mark Manson'),
                (9, 'Stephen King'),
                (10, 'Khaled Hosseini')
            ]
            cur.executemany("INSERT INTO Author (a_id, a_name) VALUES (%s, %s)", author_rows)
            print("  - Author seeded")

        # Books
        cur.execute("SELECT COUNT(*) FROM Books")
        if cur.fetchone()[0] == 0:
            books_rows = [
                (101, 'Harry Potter', 'J.K. Rowling', 'Fantasy', 10, 499.00),
                (102, '1984', 'George Orwell', 'Dystopian', 8, 349.00),
                (103, '2 States', 'Chetan Bhagat', 'Romance', 15, 299.00),
                (104, 'Pride and Prejudice', 'Jane Austen', 'Classic', 12, 399.00),
                (105, 'The Da Vinci Code', 'Dan Brown', 'Thriller', 20, 450.00),
                (106, 'Murder on the Orient Express', 'Agatha Christie', 'Mystery', 14, 375.00),
                (107, 'The Alchemist', 'Paulo Coelho', 'Philosophy', 18, 320.00),
                (108, 'You Are Not Alone', 'Mark Manson', 'Self-Help', 22, 299.00),
                (109, 'The Shining', 'Stephen King', 'Horror', 9, 425.00),
                (110, 'The Kite Runner', 'Khaled Hosseini', 'Drama', 16, 380.00)
            ]
            cur.executemany("INSERT INTO Books (b_id, b_name, a_name, genre, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)", books_rows)
            print("  - Books seeded")

        # BookAuthor
        cur.execute("SELECT COUNT(*) FROM BookAuthor")
        if cur.fetchone()[0] == 0:
            ba_rows = [(101,1),(102,2),(103,3),(104,4),(105,5),(106,6),(107,7),(108,8),(109,9),(110,10)]
            cur.executemany("INSERT INTO BookAuthor (b_id, a_id) VALUES (%s, %s)", ba_rows)
            print("  - BookAuthor seeded")

        # Reports (empty initially) - skip

        cnx.commit()
        cur.close()
        cnx.close()
        print("✅ Seed data inserted (if tables were empty).")
    except Exception as e:
        print("Error seeding data:", e)
        sys.exit(1)

# ----------------- CLI menu implementation (adapted from your main code) -----------------
def get_connection():
    return connect_db()

def add_book_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        b_id = int(input("Book ID: "))
        b_name = input("Book Name: ")
        a_name = input("Author Name: ")
        genre = input("Genre: ")
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        cur.execute("INSERT INTO Books (b_id, b_name, a_name, genre, quantity, price) VALUES (%s,%s,%s,%s,%s,%s)",
                    (b_id, b_name, a_name, genre, quantity, price))
        conn.commit()
        print("Book added.")
    except Exception as e:
        print("Error adding book:", e)
    finally:
        cur.close()
        conn.close()

def delete_book_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        b_id = int(input("Enter Book ID to delete: "))
        cur.execute("DELETE FROM Books WHERE b_id = %s", (b_id,))
        conn.commit()
        print("Book deleted.")
    except Exception as e:
        print("Error deleting book:", e)
    finally:
        cur.close()
        conn.close()

def view_books_cli():
    conn = get_connection()
    df_cur = conn.cursor()
    df_cur.execute("SELECT * FROM Books WHERE quantity > 0")
    for book in df_cur.fetchall():
        print(book)
    df_cur.close()
    conn.close()

# Customer functions
def add_customer_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        c_id = int(input("Customer ID: "))
        c_name = input("Customer Name: ")
        address = input("Address: ")
        phoneno = input("Phone: ")
        login_id = input("Login ID (unique): ")
        cur.execute("INSERT INTO Customer (cust_id, c_name, address, phoneno, login_id) VALUES (%s,%s,%s,%s,%s)",
                    (c_id, c_name, address, phoneno, login_id))
        conn.commit()
        print("Customer added.")
    except Exception as e:
        print("Error adding customer:", e)
    finally:
        cur.close()
        conn.close()

def delete_customer_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        c_id = int(input("Enter Customer ID to delete: "))
        cur.execute("DELETE FROM Customer WHERE cust_id = %s", (c_id,))
        conn.commit()
        print("Customer deleted.")
    except Exception as e:
        print("Error deleting customer:", e)
    finally:
        cur.close()
        conn.close()

def view_customers_cli():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Customer")
    for r in cur.fetchall():
        print(r)
    cur.close()
    conn.close()

# Staff
def add_staff_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        s_id = int(input("Staff ID: "))
        s_name = input("Staff Name: ")
        s_phone = input("Phone: ")
        designation = input("Designation: ")
        cur.execute("INSERT INTO Staff (s_id, s_name, s_phone, designation) VALUES (%s,%s,%s,%s)",
                    (s_id, s_name, s_phone, designation))
        conn.commit()
        print("Staff added.")
    except Exception as e:
        print("Error adding staff:", e)
    finally:
        cur.close()
        conn.close()

def delete_staff_cli():
    try:
        conn = get_connection()
        cur = conn.cursor()
        s_id = int(input("Enter Staff ID to delete: "))
        cur.execute("DELETE FROM Staff WHERE s_id = %s", (s_id,))
        conn.commit()
        print("Staff deleted.")
    except Exception as e:
        print("Error deleting staff:", e)
    finally:
        cur.close()
        conn.close()

def view_staff_cli():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Staff")
    for r in cur.fetchall():
        print(r)
    cur.close()
    conn.close()

# Reports & buying
def view_reports_cli():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Reports")
    for r in cur.fetchall():
        print(r)
    cur.close()
    conn.close()

def buy_book_cli(cust_id):
    conn = get_connection()
    cur = conn.cursor()
    view_books_cli()
    try:
        b_id = int(input("Enter Book ID to buy: "))
        qty = int(input("Enter quantity: "))
        cur.execute("SELECT quantity, price FROM Books WHERE b_id = %s", (b_id,))
        res = cur.fetchone()
        if not res:
            print("Book not found.")
            return
        stock, price = res
        if qty > stock:
            print("Not enough stock.")
            return
        total = price * qty
        today = date.today()
        cur.execute("SELECT MAX(r_no) FROM Reports")
        rno = cur.fetchone()[0]
        rno = 1 if rno is None else rno + 1
        cur.execute("INSERT INTO Reports (r_no, b_id, c_id, date_of_purchase, quantity, price) VALUES (%s,%s,%s,%s,%s,%s)",
                    (rno, b_id, cust_id, today, qty, total))
        cur.execute("UPDATE Books SET quantity = quantity - %s WHERE b_id = %s", (qty, b_id))
        conn.commit()
        print("Purchase successful. Total:", total)
    except Exception as e:
        print("Error during purchase:", e)
    finally:
        cur.close()
        conn.close()

def view_purchase_history_cli(cust_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Reports WHERE c_id = %s", (cust_id,))
    recs = cur.fetchall()
    if recs:
        for r in recs:
            print(r)
    else:
        print("No purchases yet.")
    cur.close()
    conn.close()

# Login & Menus
def admin_menu():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Book Management")
        print("2. Customer Management")
        print("3. Staff Management")
        print("4. View Reports")
        print("5. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            book_management_menu()
        elif choice == "2":
            customer_management_menu()
        elif choice == "3":
            staff_management_menu()
        elif choice == "4":
            view_reports_cli()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def book_management_menu():
    while True:
        print("\n--- BOOK MANAGEMENT ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Delete Book")
        print("4. Back to Admin Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            add_book_cli()
        elif choice == "2":
            view_books_cli()
        elif choice == "3":
            delete_book_cli()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def customer_management_menu():
    while True:
        print("\n--- CUSTOMER MANAGEMENT ---")
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Delete Customer")
        print("4. Back to Admin Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            add_customer_cli()
        elif choice == "2":
            view_customers_cli()
        elif choice == "3":
            delete_customer_cli()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def staff_management_menu():
    while True:
        print("\n--- STAFF MANAGEMENT ---")
        print("1. Add Staff")
        print("2. View All Staff")
        print("3. Delete Staff")
        print("4. Back to Admin Menu")
        choice = input("Enter choice: ")
        if choice == "1":
            add_staff_cli()
        elif choice == "2":
            view_staff_cli()
        elif choice == "3":
            delete_staff_cli()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def customer_menu(cust_id):
    while True:
        print("\n--- CUSTOMER MENU ---")
        print("1. View Books")
        print("2. Buy Book")
        print("3. View Purchase History")
        print("4. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            view_books_cli()
        elif choice == "2":
            buy_book_cli(cust_id)
        elif choice == "3":
            view_purchase_history_cli(cust_id)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def login_cli():
    login_id = input("Login ID: ").strip()
    password = input("Password: ").strip()
    # check Authentication table
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password FROM Authentication WHERE login_id = %s", (login_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and row[0] == password:
        if login_id == "chirag":
            admin_menu()
        else:
            # get cust_id
            conn2 = get_connection()
            cur2 = conn2.cursor()
            cur2.execute("SELECT cust_id FROM Customer WHERE login_id = %s", (login_id,))
            r = cur2.fetchone()
            cur2.close()
            conn2.close()
            if r:
                customer_menu(r[0])
            else:
                print("Customer record not found.")
    else:
        print("Invalid credentials.")

def run_cli_loop():
    while True:
        print("\n--- BOOKSTORE MANAGEMENT SYSTEM ---")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            login_cli()
        elif choice == "2":
            break
        else:
            print("Invalid option.")

# ----------------- MAIN -----------------
def main():
    print("Initializing bookstore database...")
    ensure_database_exists()
    # small delay to ensure DB ready
    time.sleep(0.5)
    create_tables()
    seed_data_if_empty()

    # Decide what to run
    if len(sys.argv) > 1 and sys.argv[1] == "--streamlit":
        # Launch streamlit app (assumes streamlit_app.py in same folder)
        print("Launching Streamlit app...")
        # Use subprocess so this script doesn't block the shell if you want to keep logs
        try:
            subprocess.run(["streamlit", "run", "streamlit_app.py"], check=True)
        except Exception as e:
            print("Failed to launch Streamlit. Make sure streamlit is installed and streamlit_app.py is present.")
            print(e)
    else:
        # Default: run CLI menu
        run_cli_loop()
        print("Exiting. Goodbye!")

if __name__ == "__main__":
    main()
