import mysql.connector

connection = mysql.connector.connect(user = "root", database = "example", password = "Krishna#1")

def check_balance(account_number, pin):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounting WHERE account_number = %s AND pin = %s", (account_number, pin))
    balance = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return balance

# deposit funds into a specific account
def deposit(account_number, pin, amount):
    cursor = connection.cursor()
    cursor.execute("UPDATE accounting SET balance = balance + %s WHERE account_number = %s AND pin = %s", (amount, account_number, pin))
    connection.commit()
    cursor.close()
    connection.close()

# withdraw funds from a specific account
def withdraw(account_number, pin, amount):
    cursor = connection.cursor()
    cursor.execute("SELECT balance FROM accounting WHERE account_number = %s AND pin = %s", (account_number, pin))
    balance = cursor.fetchone()[0]
    if balance < amount:
        raise ValueError("Insufficient funds")
    cursor.execute("UPDATE accounting SET balance = balance - %s WHERE account_number = %s AND pin = %s", (amount, account_number, pin))
    connection.commit()
    cursor.close()
    connection.close()

# create a new account
def create_account(owner_id, pin):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO accounting (owner_id, pin, balance) VALUES (%s, %s, 0)", (owner_id, pin))
    account_number = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return account_number

# delete an existing account
def delete_account(account_number, pin):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM accounting WHERE account_number = %s AND pin = %s", (account_number, pin))
    connection.commit()
    cursor.close()
    connection.close()

# modify an existing account
def modify_account(account_number, pin, field, value):
    cursor = connection.cursor()
    cursor.execute("UPDATE accounting SET {} = %s WHERE account_number = %s AND pin = %s".format(field), (value, account_number, pin))
    connection.commit()
    cursor.close()
    connection.close()

# create tables for user and account data
def create_tables():
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS new_table (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), username VARCHAR(20), password VARCHAR(20), email VARCHAR(50), phone VARCHAR(20), role ENUM('customer', 'admin'))")
    cursor.execute("CREATE TABLE IF NOT EXISTS accounting (account_number INT PRIMARY KEY AUTO_INCREMENT, owner_id INT, FOREIGN KEY (owner_id) REFERENCES users(id), balance DECIMAL(10, 2))")
    connection.commit()
    cursor.close()
    connection.close()
create_tables()