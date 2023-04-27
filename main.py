import os
import mysql.connector
import re

connection = mysql.connector.connect(user = "root", database = "example", password = input("Password:"))
cursor = connection.cursor(buffered=True)

def sign_in():
    print("==============================")
    print("|        Welcome to          |")
    print("|         The Vault          |")
    print("==============================")
    accountid = input("Please Enter Your Account ID: ")
    accountpin = input("Please Enter Your Account pin: ") 
    cursor.execute(f"SELECT * FROM user WHERE ID=%s AND pin=%s", (accountid, accountpin))
    result = cursor.fetchall()
    if result:
        signed_in = True
        while signed_in:
            signed_in = menu(accountid)
    else:
        input("==============================\n"
              "|   Incorrect ID or pin      |\n"
              "|   Press enter to go back.  |\n"
              "==============================") 


def new_user():
    print("===========THE VAULT===========")
    accountname = input("Your name: ")
    accountpin = input("Your pin: ")
    cursor.execute("insert into user (name, pin) values (%s, %s)", (accountname, accountpin))
    connection.commit()
    cursor.execute("SELECT LAST_INSERT_ID()")
    result = cursor.fetchone()
    if result is not None:
        accountid = result[0]
        input(f"Your account ID is: {accountid}\nPress enter to continue.")
    else:
        print("Error: User was not inserted.")

def check_balance(account_id):
    cursor.execute(f"select format(balance, 2) from user where ID={account_id}")
    balance = cursor.fetchone()[0]
    input(f"""===========THE VAULT===========
Your balance is ${balance}
Press enter to continue.
==========================
""")
    return 0

def deposit(account_id):
    print("===========THE VAULT===========\nDeposit")
    while True:
        amount = input("Please enter the amount of money to deposit: ")
        if re.match("^[0-9]{1,9}(\.[0-9]{1,2})?$", amount):
            break
        else:
            print("Invalid input.")
    input(float(amount))
    cursor.execute("update user set balance = balance + %s where ID = %s", (float(amount), account_id))
    connection.commit()
    return 0

def withdraw(account_id):
    cursor.execute(f"select balance from user where ID={account_id}")
    balance = cursor.fetchone()[0]
    prompt = "Amount to withdraw: "
    print(f"===========THE VAULT===========\n{prompt.strip(' :')} some money.")
    while True:
        amount = input(prompt)
        if re.match("^[0-9]{1,9}(\.[0-9]{1,2})?$", amount) and float(amount) <= float(balance):
            break
        print("Invalid input.")
    cursor.execute("update user set balance = balance - %s where ID = %s", (float(amount), account_id))
    connection.commit()
    return 0

def modify_account(account_id):
    print("""\n╔═════════════════════════╗
║      THE VAULT          ║
╟─────────────────────────╢
║ 1 - Edit Name           ║
║ 2 - Edit Pin            ║
║ O - Cancel              ║
╚═════════════════════════╝""")
    
    answer = take_answer(['1', '2', 'C'])
    
    if answer == '1':
        new_name = input("Please enter your new name: ")
        cursor.execute("UPDATE user SET name = %s WHERE ID = %s", (new_name, account_id))
        connection.commit()
        print("Name updated.")
    elif answer == '2':
        new_pin = input("Please enter your new pin: ")
        cursor.execute("UPDATE user SET pin = %s WHERE ID = %s", (new_pin, account_id))
        connection.commit()
        print("Pin updated.")
    else:
        print("Cancelled.")
    return True

def take_answer(options):
    answer = input("Select option: ")
    while answer not in options:
        print(f"That is not an option.\nOptions are {options}")
        answer = input("Select option: ")
    return answer

def entrypage():
    print("""
╭─────────────╮
│     THE     │
│    VAULT    │
│             │
│   1 - Sign  │
│     in      │
│             │
│2 - Create   │
│   Account   │
╰─────────────╯""")

    answer = take_answer(['1', '2'])

    if answer == '1':
        sign_in()
    else:
        new_user()


def menu(account_id):
    print("""
            ┌─────────────┐
            │   THE VAULT │
            ├─────────────┤
            │ 1 - Check Balance  │
            │ 2 - Deposit        │
            │ 3 - Withdraw       │
            │ 4 - Modify Account │
            │ 0 - Logout         │
            └─────────────┘
        """)

    answer = take_answer(['1', '2', '3', '4', '0'])

    if answer == '1':
        check_balance(account_id)
        return True
    elif answer == '2':
        deposit(account_id)
        return True
    elif answer == '3':
        withdraw(account_id)
        return True
    elif answer == '4':
        modify_account(account_id)
        return True
    else:
        return False


def main():
    while True:
        entrypage()

main()
connection.close()
