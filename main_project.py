# SETTING UP MYSQL DATABASE CONNECTION
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0178",
    database="ecommerce"
)

user_id = 1001
sale_id = 1
invoice_id = 1

# SIGN UP PAGE
def signup():
    global user_id

    print("-" * 25, "Signup", "-" * 25)

    username = input("Enter Username: ")
    password = input("Enter Password: ")
    print("Role Options: 1. Admin  2. Customer")
    role_choice = int(input("Enter Role (1 for Admin, 2 for Customer): "))

    if role_choice == 1:
        role = "admin"
    else:
        role = "customer"

    cursor = connection.cursor()
    try:
        check_query = "SELECT COUNT(*) FROM users WHERE username = '{}'".format(username)
        cursor.execute(check_query)
        result = cursor.fetchone()
        if result[0] > 0:
            print("Error: Username already exists. Please try a different username.")
            return

        query = "INSERT INTO users (id, username, password, role) VALUES ({}, '{}', '{}', '{}')"
        cursor.execute(query.format(user_id, username, password, role))
        connection.commit()
        print("Signup successful! Please login to continue.")
        print(f"User ID assigned: {user_id}\n")
        user_id += 1
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

#CUSTOMER MENU AND FUNCTIONS
def view_products():
    cursor = connection.cursor()
    query = "SELECT id, name, price, quantity FROM products WHERE quantity > 0"
    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    if products:
        print("\nAvailable Products: ")
        for prod in products:
            print(f"Product ID: {prod[0]}, Product Name: {prod[1]}, Product Price: {prod[2]}, Quantity: {prod[3]}")
    else:
        print("No products available!")
    print("-"*50)


def generate_invoice(invoice_id):
    cursor = connection.cursor()

    query = """
    SELECT 
        invoices.id AS invoice_id,
        sales.product_id,
        products.name AS product_name,
        products.price AS product_price,
        sales.quantity_sold,
        invoices.total_amount
    FROM invoices
    JOIN sales ON invoices.sales_id = sales.id
    JOIN products ON sales.product_id = products.id
    WHERE invoices.id = {}
    """
    cursor.execute(query.format(invoice_id))
    invoice = cursor.fetchone()
    cursor.close()

    if invoice:
        print("\n--- Invoice ---")
        print(f"Invoice ID: {invoice[0]}")
        print(f"Product Name: {invoice[2]}")
        print(f"Price per Unit: ₹{invoice[3]}")
        print(f"Quantity: {invoice[4]}")
        print(f"Total Amount: ₹{invoice[5]}")
        print("----------------")
    else:
        print("Error: Unable to retrieve invoice details.")


def place_order():
    global sale_id
    global invoice_id
    view_products()

    product_id = int(input("\nEnter the Product ID you want to buy: "))
    quantity = int(input("Enter the quantity: "))

    cursor = connection.cursor()
    query = "SELECT name, price, quantity FROM products WHERE id = {}"
    cursor.execute(query.format(product_id))
    product = cursor.fetchone()

    if not product:
        print("Invalid Product ID")
        return

    product_name, product_price, available_quantity = product
    if quantity > available_quantity:
        print(f"Only{available_quantity} units of {product_name} are available.")
        return

    new_quantity = available_quantity - quantity
    update_quantity_query = "UPDATE products SET quantity = {} WHERE id = {}"
    cursor.execute(update_quantity_query.format(new_quantity, product_id))

    update_query = "INSERT INTO sales (id, product_id, quantity_sold) VALUES ({}, {}, {})"
    cursor.execute(update_query.format(sale_id, product_id, quantity))

    fetch_query = "SELECT MAX(id) FROM sales"
    cursor.execute(fetch_query)
    sale_id = cursor.fetchone()[0]

    invoice_query = "INSERT INTO invoices (id, sales_id, total_amount) VALUES ({}, {}, {})"
    total_amount = product_price * quantity
    cursor.execute(invoice_query.format(invoice_id, sale_id, total_amount))

    sale_id += 1
    invoice_id += 1

    connection.commit()
    cursor.close()
    print(f"Order placed successfully for {quantity} unit(s) of {product_name}. Total Amount: ₹{total_amount}")

    while True:
        choice = input("Do you want Invoice for your Order ? \n1. Yes \n2. No")
        if choice == "1":
            generate_invoice(invoice_id)
        elif choice == "2":
            break
        else:
            print("Enter a Valid Input !!")
    print("-"*50)


def customer_menu():
    while True:
        print("\nCustomer Menu:")
        print("1. View Products")
        print("2. Place an Order")
        print("3. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            view_products()
        elif choice == 2:
            place_order()
        elif choice == 3:
            break
        else:
            print("Invalid choice. Try again.")

# ADMIN MENU AND FUNCTIONS
def add_product():
    prod_id = int(input("Enter Product ID: "))
    name = input("Enter Product Name: ")
    description = input("Enter Product Description: ")
    price = float(input("Enter Product Price: "))
    quantity = int(input("Enter Product Quantity: "))
    cursor = connection.cursor()
    query = "INSERT INTO products (id, name, description, price, quantity) VALUES ({}, '{}', '{}', {}, {})"
    cursor.execute(query.format(prod_id, name, description, price, quantity))
    connection.commit()
    cursor.close()
    print("Product added successfully.")


def view_products():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

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

    cursor = connection.cursor()
    query = "UPDATE products SET name = '{}', description = '{}', price = {}, quantity = {} WHERE id = {}"
    cursor.execute(query.format(name, description, price, quantity, product_id))
    connection.commit()
    cursor.close()
    print("Product updated successfully.")


def delete_product():
    view_products()
    product_id = int(input("Enter the Product ID to Delete: "))

    cursor = connection.cursor()
    query = "DELETE FROM products WHERE id = {}"
    cursor.execute(query.format(product_id,))
    connection.commit()
    cursor.close()
    print("Product deleted successfully.")

def view_invoices():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM invoices")
    invoices = cursor.fetchall()
    cursor.close()

    print("\nInvoices:")
    for invoice in invoices:
        print(f"Invoice ID: {invoice[0]}, Sale ID: {invoice[1]}, Total Amount: {invoice[2]}, Date: {invoice[3]}")

def view_sales():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()
    cursor.close()

    print("\nSales:")
    for sale in sales:
        print(f"Sale ID: {sale[0]}, Product ID: {sale[1]}, Quantity Sold: {sale[2]}, Sale Date and Time: {sale[3]}")

def admin_menu():
    while True:
        print("\nAdmin Menu:")
        print("1. View Products")
        print("2. Add Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. View Invoices")
        print("6. View Sales")
        print("7. Back to Main Menu")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            view_products()
        elif choice == 2:
            add_product()
        elif choice == 3:
            update_product()
        elif choice == 4:
            delete_product()
        elif choice == 5:
            view_invoices()
        elif choice == 6:
            view_sales()
        elif choice == 7:
            break
        else:
            print("Invalid choice. Try again.")


# LOGIN PAGE
def login():
    print("\nLogin:")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    cursor = connection.cursor()
    query = "SELECT role FROM users WHERE username = '{}' AND password = '{}'"
    cursor.execute(query.format(username, password))
    result = cursor.fetchone()

    if result:
        role = result[0]
        print(f"\nWelcome, {username}!")
        if role == "admin":
            admin_menu()
        elif role == "customer":
            customer_menu()
    else:
        print("Invalid username or password. Please try again.")

def main_menu():
    while True:
        print("\nMenu:")
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

connection.close()
main_menu()
