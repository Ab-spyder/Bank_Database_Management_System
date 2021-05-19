# *** Bank Database Management System ***
# A simple terminal application coded in python is used as frontend.
# Oracle’s MySQL is used as the backend database system

# Import pymysql package to provide a simple interface to MySQL Database.

import pymysql
# Take the credentials to MySQL as user input
username = input("Input the username for the MySQL database: ")
password = input("Input the password for the MySQL database: ")

try:
    connection = pymysql.connect(host='localhost',
                                 user=username,
                                 password=password,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    print("Connection Successful!!!")

except pymysql.err.OperationalError as e:
    print('Error: %d: %s' % (e.args[0], e.args[1]))

# Create the database called Bank Database System

cursor = connection.cursor()
query = 'CREATE DATABASE IF NOT EXISTS `BankDatabaseSystem`'
cursor.execute(query)
print("Database created successfully")

# Connect to the created Database

database = pymysql.connect(host='localhost',
                           user=username,
                           password=password,
                           charset='utf8mb4',
                           db='BankDatabaseSystem',
                           cursorclass=pymysql.cursors.DictCursor)

try:
    cursor = database.cursor()

    # Create table Bank Branch
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Branch`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `name` VARCHAR(50) NOT NULL,
                        `phone` VARCHAR(20) NOT NULL,
                        `city` VARCHAR(50) NOT NULL,
                        `state` CHAR(2) NOT NULL,
                        `zip` VARCHAR(20) NOT NULL                        
                )""")

    # Create table Customer
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Customer`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `first_name` VARCHAR(50) NOT NULL,
                        `last_name` VARCHAR(50) NOT NULL,
                        `phone` VARCHAR(20) NOT NULL,
                        `city` VARCHAR(50) NOT NULL,
                        `state` CHAR(2) NOT NULL,
                        `zip` VARCHAR(20) NOT NULL                        
                )""")

    # Create table Account
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Account`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `acc_number` VARCHAR(20) NOT NULL,
                        `acc_type` VARCHAR(20) NOT NULL,
                        `balance` DOUBLE DEFAULT 0.0,
                        `branch_id` INT NOT NULL,
                        `owner_id` INT NOT NULL,
                        FOREIGN KEY(`owner_id`) REFERENCES `customer`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(`branch_id`) REFERENCES `Branch`(`id`) ON UPDATE CASCADE ON DELETE CASCADE                        
                )""")

    # Create Table Loan
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Loan`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `customer_id` INT NOT NULL,
                        `account_id` INT NOT NULL,
                        `amount` INT DEFAULT 0,
                        `interest` DOUBLE NOT NULL DEFAULT 0.0,
                        `years` INT NOT NULL DEFAULT 2,
                        FOREIGN KEY(`customer_id`) REFERENCES `Customer`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(`account_id`) REFERENCES `Account`(`id`) ON UPDATE CASCADE ON DELETE CASCADE
                )""")

    # Create Table Transaction
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Transaction`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `customer_id` INT NOT NULL,
                        `account_id` INT NOT NULL,
                        `amount` INT DEFAULT 0,
                        `description` VARCHAR(255) NOT NULL DEFAULT "",
                        FOREIGN KEY(`customer_id`) REFERENCES `Customer`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(`account_id`) REFERENCES `Account`(`id`) ON UPDATE CASCADE ON DELETE CASCADE
                )""")

    # Create Table Claim
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS `Claim`
                (
                        `id` INT PRIMARY KEY AUTO_INCREMENT,
                        `account_id` INT NOT NULL,
                        `owner_id` INT NOT NULL,
                        `description` VARCHAR(255) NOT NULL DEFAULT "",
                        `date` DATETIME NOT NULL,
                        FOREIGN KEY(`account_id`) REFERENCES `Account`(`id`) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY(`owner_id`) REFERENCES `Customer`(`id`) ON UPDATE CASCADE ON DELETE CASCADE
                )""")
    print("All tables are created successfully in the Bank Database System")

    # Now, we need to insert some sample data for demonstration purposes

    cursor.execute(
        "INSERT INTO `Branch` (name, phone, city, state, zip) VALUES ('Grafton', '9784439888', 'Cambridge', 'MA', '02341')")
    cursor.execute(
        "INSERT INTO `Branch` (name, phone, city, state, zip) VALUES ('Maple', '6264439888', 'Stockton', 'CA', '95219')")
    cursor.execute(
        "INSERT INTO `Branch` (name, phone, city, state, zip) VALUES ('Valley', '8062797843', 'Austin', 'TX', '79065')")

    cursor.execute(
        "INSERT INTO `customer` (first_name, last_name, phone, city, state, zip) VALUES ('Lisa', 'White', '9788477697', 'Cambridge', 'MA', '02341' )")
    cursor.execute(
        "INSERT INTO `customer` (first_name, last_name, phone, city, state, zip) VALUES ('Sarah', 'Walling', '4132555381', 'Springfield', 'MA', '01103' )")
    cursor.execute(
        "INSERT INTO `customer` (first_name, last_name, phone, city, state, zip) VALUES ('Ronald', 'Lutz', '2093049067', 'Stockton', 'CA', '95201' )")
    cursor.execute(
        "INSERT INTO `customer` (first_name, last_name, phone, city, state, zip) VALUES ('Kristin', 'Cook', '2096628424', 'Stockton', 'CA', '95217' )")
    cursor.execute(
        "INSERT INTO `customer` (first_name, last_name, phone, city, state, zip) VALUES ('Barbara', 'Baker', '5126085577', 'Austin', 'TX', '78746' )")

    cursor.execute(
        "INSERT INTO `account` (acc_number, acc_type, balance, branch_id, owner_id) VALUES ('2345-8756-9876-5432', 'Savings', 250000.2, 1, 1)")
    cursor.execute(
        "INSERT INTO `account` (acc_number, acc_type, balance, branch_id, owner_id) VALUES ('2345-8756-9876-5498', 'Savings', 32693.3, 1, 2)")
    cursor.execute(
        "INSERT INTO `account` (acc_number, acc_type, balance, branch_id, owner_id) VALUES ('9867-4520-0956-1764', 'Savings', 290000.7, 2, 3)")

    print("Sample Data inserted successfully")
    database.commit()


except pymysql.Error as err:
    print('Error: %d: %s' % (err.args[0], err.args[1]))
