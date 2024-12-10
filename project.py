# SETTING UP MYSQL DATABASE CONNECTION
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0178",
        database="ecommerce"
    )

# PRODUCT MANAGEMENT

def add_product():

    name = input("Enter Product Name: ")
    description = input("Enter Product Description: ")
    price = float(input("Enter Product Price: "))
    quantity = int(input("Enter Product Quantity: "))

    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO products (name, description, price, quantity) VALUES ('{}', '{}', {}, {})"
    cursor.execute(query.format(name, description, price, quantity))
    db.commit()
    db.close()
    print("Product added successfully.")


def view_products():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    db.close()

    print("\nCurrent Products:")
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[3]}, Quantity: {product[4]}")


def update_product():
    view_products()
    product_id = int(input("Enter the Product ID to Update: "))
    name = input("Enter New Name: ")
    description = input("Enter New Description: ")
    price = float(input("Enter New Price: "))
    quantity = int(input("Enter New Quantity: "))

    db = connect_db()
    cursor = db.cursor()
    query = "UPDATE products SET name = '{}', description = '{}', price = {}, quantity = %s WHERE id = %s"
    cursor.execute(query, (name, description, price, quantity, product_id))
    db.commit()
    db.close()
    print("Product updated successfully.")


def delete_product():
    view_products()
    product_id = int(input("Enter the Product ID to Delete: "))

    db = connect_db()
    cursor = db.cursor()
    query = "DELETE FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))
    db.commit()
    db.close()
    print("Product deleted successfully.")


# CUSTOMER MENU

def view_products():
    db = connect_db()
    cursor = db.cursor()
    query = "SELECT id, name, price, quantity FROM products WHERE quantity > 0"
    cursor.execute(query)
    products = cursor.fetchall()
    db.close()

    if products:
        print("\nAvailable Products: ")
        for prod in products:
            print(f"Product ID: {prod[0]}, Product Name: {prod[1]}, Product Price: {prod[2]}, Quantity: {prod[3]}")
    else:
        print("No products available!")
    print("-"*50)

def place_order():

    view_products()

    product_id = int(input("\nEnter the Product ID you want to buy: "))
    quantity = int(input("Enter the quantity: "))

    db = connect_db()
    cursor = db.cursor
    query = "SELECT name, price, quantity FROM products WHERE id = {}"
    cursor.execute(query.format(product_id))
    product = cursor.fetchone()

    if not product:
        print("Invalid Product ID")
        db.close()
        return

    product_name, product_price, available_quantity = product
    if quantity > available_quantity:
        print(f"Only{ available_quantity} units of {product_name} are available.")
        db.close()
        return

    new_quantity = available_quantity - quantity
    cursor.execute("UPDATE products SET quantity = {} WHERE id = {}".format(new_quantity, product_id))

    cursor.execute(
        "INSERT INTO sales (product_id, quantity_sold) VALUES ({}, {})".format(product_id, quantity)
    )
    sale_id = cursor.lastrowid

    total_amount = product_price * quantity
    cursor.execute(
        "INSERT INTO invoices (sales_id, total_amount) VALUES ({}, {})".format(sale_id, total_amount)
    )

    db.commit()
    db.close()

    print(f"Order placed successfully for {quantity} unit(s) of {product_name}. Total Amount: ₹{total_amount}")

    print("-"*50)
import mysql.connector
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="0178",
        database="ecommerce"
    )

# SIGN UP PAGE
def signup():
    print("\nSignup:")

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    print("Role Options: 1. Admin  2. Customer")
    role_choice = int(input("Enter Role (1 for Admin, 2 for Customer): "))

    if role_choice == 1:
        role = "admin"
    else:
        role = "customer"

    db = connect_db()
    cursor = db.cursor()

    # try:
    query = "INSERT INTO users (username, password, role) VALUES ('{}', '{}', '{}')"
    cursor.execute(query.format(username, password, role))
    db.commit()
    print("Signup successful! Please login to continue.")
    # except:
    #     print("Username already exists. Please try again.")
    # db.close()

# LOGIN PAGE
def login():
    print("\nLogin:")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    db = connect_db()
    cursor = db.cursor()

    query = "SELECT role FROM users WHERE username = '{}' AND password = '{}'"
    cursor.execute(query.format(username, password))
    result = cursor.fetchone()
    db.close()

    if result:
        role = result[0]
        print(f"Welcome, {username}!")
        if role == "admin":
            admin_menu()
        elif role == "customer":
            customer_menu()
    else:
        print("Invalid username or password. Please try again.")

# MAIN MENU
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            login()
        elif choice == 2:
            signup()
        elif choice == 3:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

main_menu()