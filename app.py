from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kharanshu23',
    'database': 'db2'
}

# Function to fetch customer data
def get_customers():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID, FirstName, LastName, Email, Phone, Status FROM Customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

# Function to fetch contacts and sales data for a given CustomerID
def get_related_data(customer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Fetch contacts data
    cursor.execute("SELECT ContactID FROM Contacts WHERE CustomerID = %s", (customer_id,))
    contacts = cursor.fetchall()

    # Fetch sales data
    cursor.execute("SELECT SaleID, ProductID FROM Sales WHERE CustomerID = %s", (customer_id,))
    sales = cursor.fetchall()

    conn.close()
    return contacts, sales

# Route for displaying customer list
@app.route('/')
def customer_list():
    customers = get_customers()
    return render_template('customer_list.html', customers=customers)

# Route for displaying customer details
@app.route('/customer/<int:customer_id>')
def customer_details(customer_id):
    customer = None
    contacts = None
    sales = None

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Fetch customer details
    cursor.execute("SELECT CustomerID, FirstName, LastName, Email, Phone, Status FROM Customers WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()

    # Fetch related data (contacts and sales)
    if customer:
        contacts, sales = get_related_data(customer_id)

    conn.close()
    return render_template('customer_details.html', customer=customer, contacts=contacts, sales=sales)

if __name__ == '__main__':
    app.run(debug=True)
