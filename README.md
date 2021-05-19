# Bank Database Management System
## Database Management Systems (CS 5200)

This project aims to demonstrate the working and basic functionality of a bank management system. 

### Description of the Application:
To begin with, a bank entity must be registered in the application. Any number of banking
entities can be registered, but there must be at least one registered to use the main functions.
Secondly, the customer must also be registered with name and contact information. Only then
they can proceed to open a bank account in the chosen bank. Once the bank has been created,
the customer can obtain a loan with specifying the time in years, loan amount and interest rate.
The application also allows you to display the list of banks, accounts, clients, loans, and
transactions.
The main functions (CRUD operations) of the database are as follows:
1. Register a new Branch
2. Register a new Customer
3. Register a new Account
4. Print the list of branches
5. Print the list of customers
6. Print the list of accounts
7. Delete a particular customer
8. Perform a new transaction
9. List all the transactions
10. Create a Loan
11. Create a claim
12. List all the claims
13. Update a particular Customer's Details
14. Transfer money from one account to another account 

### Tools and Technologies Used:
* A simple terminal application coded in python is used as Frontend.
* Oracle’s MySQL is used as the backend database system
*  MySQL workbench version 8.022 is used as a database client
*  PyCharm version 2020.2 is used as IDE.

### Usage:
There are 2 python files provided: *Bank_DB_init.py* and *Bank_DB_main.py*.

The file ***Bank_DB_init.py*** should be run first. This file is used to create the database and all the bank
entities required for the bank database system. This file also inserts some sample data to start.

One important package to install is PyMySQL. This package provides an interface for connecting to a MySQL database from Python3.
Credentials to the database are accepted from the user. Please provide your username and password to connect to the database on your system.
 
The file ***Bank_DB_main.py*** provides the Menu to interact with the database and should be run after running the first file.

Few important packages to install before running the second file are:
* Random – Used to generate a random integer used for account numbers in the Account table
* Tabulate – Used to print tabular data in nicely formatted tables
* Datetime – Used for working with date and time in python

The conceptual and logical diagrams are also included in the Project Report. Do watch the *Project_Demo.mp4* video included above for more information!
