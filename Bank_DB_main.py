# importing all the required packages

from random import randint
from tabulate import tabulate
from datetime import datetime
import pymysql

# Take the credentials to MySQL as user input
username = input("Input the username for the MySQL database: ")
password = input("Input the password for the MySQL database: ")

# Connect to the Bank Database System
try:
    database = pymysql.connect(host='localhost',
                               user=username,
                               password=password,
                               charset='utf8mb4',
                               db='BankDatabaseSystem',
                               cursorclass=pymysql.cursors.DictCursor)
    print("Connection Successful!!!")

except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

cursor = database.cursor()


def displayMenu():
    print("     BANK MAIN MENU     ")
    print("************************")
    print("1) Register a new Branch")
    print("2) Register a new Customer")
    print("3) Register a new Account")
    print("4) Print the list of branches")
    print("5) Print the list of customers")
    print("6) Print the list of accounts")
    print("7) Delete a particular user/customer")
    print("8) Perform a new transaction")
    print("9) List all the transactions")
    print("10) Create a Loan")
    print("11) Create a claim")
    print("12) List all the claims")
    print("13) Update a particular Customer's Details")
    print("14) Transfer money from one account to another account")
    print("15) Exit")


def getMenuOption(options):
    while True:
        option = input("Please select an option: ")
        if option.isnumeric() and int(option) in options:
            return int(option)


if __name__ == '__main__':
    displayMenu()

    while True:
        option = getMenuOption(range(1, 16))
        # Register a new Branch
        if option == 1:
            branch_name = input("Enter branch name: ")
            branch_phone = input("Enter phone number: ")
            branch_city = input('Enter city where the branch is located: ')
            branch_state = input('Enter state where the branch is located: ')
            branch_zip = input('Enter zip code of the branch: ')

            # Check if there is a branch with the same name
            query = "SELECT * FROM `Branch` WHERE LOWER(`name`) = '" + branch_name.lower() + "'"
            cursor.execute(query)
            result = cursor.fetchall()
            if result != None and len(result) > 0:
                print("A branch with same name exists already!!!")
            else:
                # Since it is a new name, we can continue with the registration of the branch
                cursor.execute(
                    "INSERT INTO `Branch` (name, phone, city, state, zip) VALUES ('" + branch_name + "', '" + branch_phone + "', '" + branch_city + "', '" + branch_state + "', '" + branch_zip + "')")
                database.commit()
                print("A new Branch named " + branch_name + " is registered!!!")
        # Register a new Customer
        if option == 2:
            customer_fname = input("Enter the customer's first name: ")
            customer_lname = input("Enter the customer's last name: ")
            customer_phone = input("Enter the customer's phone number: ")
            customer_city = input('Enter city where the customer is located: ')
            customer_state = input('Enter state where the customer is located: ')
            customer_zip = input('Enter zip code where the customer is located: ')
            query = "INSERT INTO `Customer` (first_name, last_name, phone, city, state, zip) VALUES ('" + customer_fname + "', '" + customer_lname + "', '" + customer_phone + "', '" + customer_city + "', '" + customer_state + "', '" + customer_zip + "')"
            cursor.execute(query)
            database.commit()
            print("A new Customer named " + customer_fname + " " + customer_lname + " is registered!!!")

        # Register a new Account
        if option == 3:

            # Here, account number can be randomly generated using the randint() function
            while True:
                acc_number = str(randint(1111, 9999)) + "-" + str(randint(1111, 9999)) + "-" + str(
                    randint(1111, 9999)) + "-" + str(randint(1111, 9999))
                query = "SELECT * FROM `Account` WHERE `acc_number` = '" + acc_number + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                if result is None or len(result) == 0:
                    break

            while True:
                typ = input("Please select an account type (option 1 for checking, option 2 for savings): ")
                if typ.isnumeric() and int(typ) in [1, 2]:
                    if typ == 1:
                        typ_str = "Checking"
                    else:
                        typ_str = "Saving"
                    break

            balance = int(input("Enter your account balance: "))

            while True:
                branch_name = input("Please enter the name of the bank where you would like to open an account: ")
                query = "SELECT `id` FROM `Branch` WHERE LOWER(`name`) = '" + branch_name.lower() + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                if not result is None and len(result) > 0:  # bank exists and is valid, so we can continue
                    branch_id = result[0]['id']
                    break
                else:
                    print("We cannot open an account here as the bank name entered cannot be found")

            while True:
                print(balance)
                customer_id = input("Please enter the customer id to register an account: ")
                query = "SELECT * FROM `Customer` WHERE `id` = " + str(customer_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if not result is None and len(result) > 0:
                    # We can continue the registration of the account
                    query = "INSERT INTO ACCOUNT (`acc_number`, `acc_type`, `balance`, `branch_id`, `owner_id`) VALUES ('" + acc_number + "', '" + typ_str + "', " + str(balance) + ", " + str(branch_id) + "," + str(customer_id) + ")"
                    cursor.execute(query)
                    database.commit()
                    print("A New Account has been registered to the customer!!!")
                    break

        # Print the list of branches
        if option == 4:
            query = "SELECT * FROM `Branch`"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                header = result[0].keys()
                rows = [x.values() for x in result]
                print(tabulate(rows, headers=header))

        # Print the list of customers
        if option == 5:
            query = "SELECT * FROM `Customer`"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                header = result[0].keys()
                rows = [x.values() for x in result]
                print(tabulate(rows, headers=header))
            else:
                print("There are no registered customers in the database")

        # Print the list of accounts
        if option == 6:
            query = "SELECT * FROM `Account`"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                header = result[0].keys()
                rows = [x.values() for x in result]
                print(tabulate(rows, headers=header))
            else:
                print("There are no accounts in the database")

        # Delete a particular user/customer
        if option == 7:
            fname = input("Enter the first name of the user/customer to remove from the database: ")
            lname = input("Enter the last name of the user/customer to remove from the database: ")
            # First, We need to check if that user/customer exists in the database
            query = "SELECT * FROM `Customer` WHERE LOWER(`first_name`) = '" + fname.lower() + "'" "AND"" LOWER(`last_name`) = '" + lname.lower() + "'"
            cursor.execute(query)
            result = cursor.fetchall()

            if len(result) > 0:
                # The user/customer exists in the database and we can continue to delete
                cid = result[0]['id']
                query = "DELETE FROM `Customer` WHERE `id` = " + str(cid)
                cursor.execute(query)
                database.commit()
                print("The user/customer named " + fname + " " + lname + "is deleted from database.")
            else:
                print("There is no user/customer with the given name in the database.")

        # Perform a new transaction
        if option == 8:
            customer_id = input("Enter the customer id: ")
            if customer_id.isnumeric():
                # Check if the customer exists in the database
                customer_id = int(customer_id)
                query = "SELECT * FROM `Customer` WHERE `id` = " + str(customer_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:  # The customer exists in the database
                    query = "SELECT `id` FROM `Account` WHERE `owner_id` = " + str(customer_id)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) > 0:  # Account exists for that particular customer
                        account_id = result[0]['id']
                        balance = input("Please enter the balance to be deposited in the account: ")
                        if balance.isnumeric():
                            balance = float(balance)
                            branch_name = input("Enter the name of the bank where the transaction will be held: ")
                            query = "SELECT `id` FROM `Branch` WHERE LOWER(`name`) = '" + branch_name + "'"
                            cursor.execute(query)
                            result = cursor.fetchall()
                            if len(result) > 0:  # branch exists for that particular customer
                                branch_id = result[0]['id']
                                desc = input("Please enter the description of the transaction: ")
                                query = "INSERT INTO `transaction` (customer_id, account_id, amount, description) VALUES (" + str(
                                    customer_id) + ", " + str(account_id) + ", " + str(balance) + ", '" + desc + "')"
                                cursor.execute(query)
                                database.commit()
                                print("Transaction is performed successfully!!!.")
                            else:
                                print("There is no branch with that name.")
                        else:
                            print("You must enter a valid balance.")
                    else:
                        print("There is no account with that id.")
                else:
                    print("There is no customer with that id.")
            else:
                print("Please enter a valid customer id.")

        # List all the transactions
        if option == 9:  # list
            query = "SELECT * FROM `transaction`"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                header = result[0].keys()
                rows = [x.values() for x in result]
                print(tabulate(rows, headers=header))
            else:
                print("There are no transactions registered in the database.")

        # Create a Loan
        if option == 10:  # create loan
            customer_id = input("Enter the customer id: ")
            if customer_id.isnumeric():
                # Check if customer exists in the database
                customer_id = int(customer_id)
                query = "SELECT * FROM `Customer` WHERE `id` = " + str(customer_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:  # Customer exists in the database
                    query = "SELECT `id` FROM `Account` WHERE `owner_id` = " + str(customer_id)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) > 0:  # Account exists for that customer
                        account_id = result[0]['id']
                        amount = input("Please enter the amount of the loan: ")
                        if amount.isnumeric():
                            amount = float(amount)
                            rate = input("Enter the rate of interest: ")

                            if rate.isnumeric() and int(rate) > 0 and int(rate) <= 100:
                                rate = int(rate)
                                years = input("Enter the time (in years) for the loan: ")
                                if years.isnumeric() and int(years) > 0:
                                    years = int(years)
                                    query = "INSERT INTO `loan` (customer_id, account_id, amount, interest, years) VALUES (" + str(
                                        customer_id) + ", " + str(account_id) + ", " + str(amount) + ", " + str(
                                        rate) + ", " + str(years) + ")"
                                    cursor.execute(query)
                                    database.commit()
                                    print("Loan created!")
                                else:
                                    print("You must enter a valid number of years(should be greater than zero).")
                            else:
                                print("Interest rate must be a positive value being less or equal than 100%")
                        else:
                            print("You must enter a valid amount.")
                    else:
                        print("There is no account with that id.")
                else:
                    print("There is no customer with that id.")
            else:
                print("Please enter a valid customer id.")

        # Create a claim
        if option == 11:
            customer_id = input("Enter the customer id making the claim: ")
            if customer_id.isnumeric():
                # Check if customer exists
                customer_id = int(customer_id)
                query = "SELECT * FROM `Customer` WHERE `id` = " + str(customer_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:  # customer exists in the database
                    query = "SELECT `id` FROM `Account` WHERE `owner_id` = " + str(customer_id)
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) > 0:  # Account exists for that particular customer
                        account_id = result[0]['id']
                        description = input("Please enter the description of the claim: ")

                        query = "INSERT INTO `claim` (account_id, owner_id, description, date) VALUES (" + str(
                            account_id) + ", " + str(customer_id) + ", '" + description + "', '" + str(
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "')"
                        cursor.execute(query)
                        database.commit()
                        print("The Claim is added successfully!!!")
                    else:
                        print("There is no account with that id.")
                else:
                    print("There is no customer with that id.")
            else:
                print("Please enter a valid customer id.")

        # List all the claims
        if option == 12:
            query = "SELECT * FROM `claim`"
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) > 0:
                header = result[0].keys()
                rows = [x.values() for x in result]
                print(tabulate(rows, headers=header))
            else:
                print("There are no claims present in the database.")

        # Update a particular Customer's Details
        if option == 13:
            customer_id = input("Enter customer id who details need to be updated: ")
            if customer_id.isnumeric():
                customer_id = int(customer_id)
                query = "SELECT * FROM `Customer` WHERE `id` = " + str(customer_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:  # Customer exists in the database
                    cid = result[0]['id']
                    fname = input("Enter the new first name of the customer : ")
                    lname = input("Enter the new last name of the customer: ")
                    phoneno = input("Enter the new phone number of the customer: ")
                    ccity = input("Enter the new city of the customer : ")
                    cstate = input("Enter the new state of the customer : ")
                    czip = input("Enter the new zip code of the customer : ")
                    query = "UPDATE `Customer` SET `first_name` = \"" + fname + "\", `last_name` = \"" + lname + "\", `phone` = \"" + phoneno + "\", `city` = \"" + ccity + "\", `state` = \"" + cstate + "\", `zip` = \"" + czip + "\" WHERE `id` = " + str(
                        cid) + ";"
                    cursor.execute(query)
                    database.commit()
                    print("Deatils of the customer with id  " + str(cid) + " has been updated!")
                else:
                    print("There is no customer with that ID in the database.")
            else:
                print("Enter a Valid customer ID.")

        # Transfer money from one account to another account
        if option == 14:
            account_1_id = input("Enter the ID of the account from where the funds will be transferred: ")
            if account_1_id.isnumeric():
                account_1_id = int(account_1_id)
                query = "SELECT * FROM `Account` WHERE `id` = " + str(account_1_id)
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) > 0:  # Account 1 Exists
                    account_1_amount = result[0]['balance']
                    account_2_id = input("Enter the id of the account to which the funds will be received: ")
                    if account_2_id.isnumeric():
                        account_2_id = int(account_2_id)
                        query = "SELECT * FROM `Account` WHERE `id` = " + str(account_2_id)
                        cursor.execute(query)
                        result = cursor.fetchall()
                        if len(result) > 0:  # Account 2 Exists
                            amount = input("Please enter the amount to transfer: ")
                            if amount.isnumeric() and float(amount) > 0:
                                amount = float(amount)
                                if amount <= account_1_amount:
                                    # Sufficient funds are present in account 1 and transfer can start

                                    # Add amount to account 2
                                    query = "UPDATE `Account` SET `balance` = `balance` + " + str(
                                        amount) + " WHERE `id` = " + str(account_2_id) + ";"
                                    cursor.execute(query)
                                    database.commit()

                                    # Remove amount from account 1
                                    query = "UPDATE `Account` SET `balance` = `balance` - " + str(
                                        amount) + " WHERE `id` = " + str(account_1_id) + ";"
                                    cursor.execute(query)
                                    database.commit()
                                    print("A total of $" + str(amount) + " has been transferred from account " + str(
                                        account_1_id) + " to account " + str(account_2_id))
                                else:
                                    print("There is not enough balance to proceed with the transfer.")
                            else:
                                print("Enter a valid amount.")
                        else:
                            print("There is no account with that id.")
                    else:
                        print("Please enter a valid account id.")
                else:
                    print("There is no account with that id.")
            else:
                print("Please enter a valid account id.")

        if option == 15:
            print("Thank you for using the Bank Management System. Have a Good Day!!!")
            break
