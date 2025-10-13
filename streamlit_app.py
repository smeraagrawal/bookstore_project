import streamlit as st
import mysql.connector
import pandas as pd
from datetime import date


# Function to establish database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='bookstore',
            user='root',  # Replace with your MySQL username
            password='root'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None


# User Login Function
# User Login Function
def user_login():
    st.title("Bookstore Management System 📚")
    login_id = st.text_input("Login ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_id and password:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM authentication WHERE login_id = %s AND password = %s", (login_id, password))
            user = cursor.fetchone()
            if user:
                if login_id == "chirag":  # Admin login
                    st.session_state.user_role = "admin"
                    admin_dashboard()
                else:  # Customer login
                    st.session_state.user_role = "customer"
                    cursor.execute("SELECT cust_id FROM customer WHERE login_id = %s", (login_id,))
                    row = cursor.fetchone()
                    if row:
                        st.session_state.cust_id = row['cust_id']  # Store customer ID in session state
                        customer_dashboard()  # Navigate to the customer dashboard
                    else:
                        st.error("Customer record not found.")
            else:
                st.error("Invalid credentials.")
            connection.close()
        else:
            st.error("Please enter both login ID and password.")




# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard 🔐")
    menu = ["Book Management", "Author Management", "Staff Management", "Customer Management", "Reports", "Logout"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Book Management":
        book_management()
    elif choice == "Author Management":
        author_management()
    elif choice == "Staff Management":
        staff_management()
    elif choice == "Customer Management":
        customer_management()
    elif choice == "Reports":
        view_reports()
    elif choice == "Logout":
        logout()


# Book Management
def book_management():
    st.subheader("Book Management")
    menu = ["Add Book", "Delete Book", "View All Books", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Book":
        add_book()
    elif choice == "Delete Book":
        delete_book()
    elif choice == "View All Books":
        view_books()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


# Add Book
def add_book():
    st.subheader("Add New Book")
    b_id = st.number_input("Book ID", min_value=1)
    b_name = st.text_input("Book Name")
    a_name = st.text_input("Author Name")
    genre = st.text_input("Genre")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price", min_value=0.01)

    if st.button("Add Book"):
        if b_name and a_name:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO books (b_id, b_name, a_name, genre, quantity, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (b_id, b_name, a_name, genre, quantity, price))
            connection.commit()
            st.success(f"Book '{b_name}' added successfully!")
            connection.close()
        else:
            st.error("Please fill in all fields.")


# Delete Book
def delete_book():
    st.subheader("Delete Book")
    b_id = st.number_input("Enter Book ID to delete", min_value=1)
    if st.button("Delete Book"):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM books WHERE b_id = %s", (b_id,))
        connection.commit()
        st.success(f"Book with ID {b_id} deleted successfully!")
        connection.close()


# View Books
def view_books():
    st.subheader("View All Books")
    connection = get_db_connection()
    query = "SELECT * FROM books"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()


# Author Management
def author_management():
    st.subheader("Author Management")
    menu = ["Add Author", "Delete Author", "View All Authors", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Author":
        add_author()
    elif choice == "Delete Author":
        delete_author()
    elif choice == "View All Authors":
        view_authors()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


# Add Author
def add_author():
    st.subheader("Add New Author")
    a_id = st.number_input("Author ID", min_value=1)
    a_name = st.text_input("Author Name")

    if st.button("Add Author"):
        if a_name:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO author (a_id, a_name) VALUES (%s, %s)", (a_id, a_name))
            connection.commit()
            st.success(f"Author '{a_name}' added successfully!")
            connection.close()
        else:
            st.error("Please enter author name.")


# Delete Author
def delete_author():
    st.subheader("Delete Author")
    a_id = st.number_input("Enter Author ID to delete", min_value=1)
    if st.button("Delete Author"):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM author WHERE a_id = %s", (a_id,))
        connection.commit()
        st.success(f"Author with ID {a_id} deleted successfully!")
        connection.close()


# View Authors
def view_authors():
    st.subheader("View All Authors")
    connection = get_db_connection()
    query = "SELECT * FROM author"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()


# Staff Management
def staff_management():
    st.subheader("Staff Management")
    menu = ["Add Staff", "Delete Staff", "View All Staff", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Staff":
        add_staff()
    elif choice == "Delete Staff":
        delete_staff()
    elif choice == "View All Staff":
        view_staff()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


# Add Staff
def add_staff():
    st.subheader("Add New Staff")
    s_id = st.number_input("Staff ID", min_value=1)
    s_name = st.text_input("Staff Name")
    s_phone = st.text_input("Phone")
    designation = st.text_input("Designation")

    if st.button("Add Staff"):
        if s_name and s_phone and designation:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO staff (s_id, s_name, s_phone, designation) VALUES (%s, %s, %s, %s)",
                           (s_id, s_name, s_phone, designation))
            connection.commit()
            st.success(f"Staff '{s_name}' added successfully!")
            connection.close()
        else:
            st.error("Please fill in all fields.")


# Delete Staff
def delete_staff():
    st.subheader("Delete Staff")
    s_id = st.number_input("Enter Staff ID to delete", min_value=1)
    if st.button("Delete Staff"):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM staff WHERE s_id = %s", (s_id,))
        connection.commit()
        st.success(f"Staff with ID {s_id} deleted successfully!")
        connection.close()


# View Staff
def view_staff():
    st.subheader("View All Staff")
    connection = get_db_connection()
    query = "SELECT * FROM staff"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()


# Customer Management
def customer_management():
    st.subheader("Customer Management")
    menu = ["Add Customer", "Delete Customer", "View All Customers", "Back to Admin Menu"]
    choice = st.selectbox("Select an option", menu)

    if choice == "Add Customer":
        add_customer()
    elif choice == "Delete Customer":
        delete_customer()
    elif choice == "View All Customers":
        view_customers()
    elif choice == "Back to Admin Menu":
        admin_dashboard()


# Add Customer
def add_customer():
    st.subheader("Add New Customer")
    cust_id = st.number_input("Customer ID", min_value=1)
    c_name = st.text_input("Customer Name")
    address = st.text_input("Address")
    phoneno = st.text_input("Phone Number")

    if st.button("Add Customer"):
        if c_name and address and phoneno:
            connection = get_db_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO customer (cust_id, c_name, address, phoneno) VALUES (%s, %s, %s, %s)",
                               (cust_id, c_name, address, phoneno))
                connection.commit()
                st.success(f"Customer '{c_name}' added successfully!")
            except mysql.connector.Error as e:
                st.error(f"Failed to add customer: {e}")
            finally:
                connection.close()
        else:
            st.error("Please fill in all fields.")


# Delete Customer
def delete_customer():
    st.subheader("Delete Customer")
    cust_id = st.number_input("Enter Customer ID to delete", min_value=1)
    if st.button("Delete Customer"):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM customer WHERE cust_id = %s", (cust_id,))
            connection.commit()
            st.success(f"Customer with ID {cust_id} deleted successfully!")
        except mysql.connector.Error as e:
            st.error(f"Error deleting customer: {e}")
        finally:
            connection.close()


# View Customers
def view_customers():
    st.subheader("View All Customers")
    connection = get_db_connection()
    query = "SELECT * FROM customer"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()



# Reports
def view_reports():
    st.subheader("View Reports")
    connection = get_db_connection()
    query = "SELECT * FROM reports"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()


# Customer Dashboard
def customer_dashboard():
    st.title("Customer Dashboard 🛍")
    menu = ["View Books", "Buy Book", "View Purchase History", "Logout"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "View Books":
        view_books_for_customer()
    elif choice == "Buy Book":
        buy_book()
    elif choice == "View Purchase History":
        view_purchase_history()
    elif choice == "Logout":
        logout()


def view_books_for_customer():
    st.subheader("View Available Books")
    connection = get_db_connection()
    query = "SELECT * FROM books WHERE quantity > 0"
    df = pd.read_sql(query, connection)
    st.dataframe(df)
    connection.close()

def view_purchase_history():
    if 'cust_id' not in st.session_state:
        st.error("Customer not logged in.")
        return

    st.subheader("View Purchase History")
    connection = get_db_connection()
    query = f"SELECT * FROM reports WHERE c_id = {st.session_state.cust_id}"
    df = pd.read_sql(query, connection)
    if df.empty:
        st.write("No purchases yet.")
    else:
        st.dataframe(df)
    connection.close()

def logout():
    del st.session_state.user_role
    if "cust_id" in st.session_state:
        del st.session_state.cust_id
    st.success("Logged out successfully.")
    user_login()


def buy_book():
    st.subheader("Buy Book")
    b_id = st.number_input("Enter Book ID to buy", min_value=1, key="buy_book_id")
    qty = st.number_input("Enter quantity", min_value=1, key="buy_quantity")

    if st.button("Buy"):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT quantity, price FROM books WHERE b_id = %s", (b_id,))
        result = cursor.fetchone()

        if result:
            stock, price = result
            if qty <= stock:
                total_price = qty * float(price)
                today = date.today()
                cursor.execute(
                    "INSERT INTO reports (b_id, c_id, date_of_purchase, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                    (b_id, st.session_state.cust_id, today, qty, total_price)
                )

                cursor.execute("UPDATE books SET quantity = quantity - %s WHERE b_id = %s", (qty, b_id))
                connection.commit()
                st.success(f"Purchase successful! Total: ₹{total_price:.2f}")
            else:
                st.error("Not enough stock available.")
        else:
            st.error("Book not found.")
        connection.close()


# Run app
if __name__ == "__main__":
    if "user_role" not in st.session_state:
        user_login()
    elif st.session_state.user_role == "admin":
        admin_dashboard()
    else:
        customer_dashboard()