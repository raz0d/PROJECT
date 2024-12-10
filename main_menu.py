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

    try:
        query = "INSERT INTO users (username, password, role) VALUES ('{}', '{}', '{}')"
        cursor.execute(query.format(username, password, role))
        db.commit()
        print("Signup successful! Please login to continue.")
    except:
        print("Username already exists. Please try again.")
    db.close()

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