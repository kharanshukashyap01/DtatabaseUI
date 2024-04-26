from flask import Flask, render_template, request, redirect, url_for
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

# Route for editing customer details
@app.route('/edit_customer/<int:customer_id>')
def edit_customer(customer_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT CustomerID, FirstName, LastName, Email, Phone, Status FROM Customers WHERE CustomerID = %s", (customer_id,))
    customer = cursor.fetchone()

    conn.close()
    return render_template('edit_customer.html', customer=customer)

# Route for updating customer details
@app.route('/update_customer/<int:customer_id>', methods=['POST'])
def update_customer(customer_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    status = request.form['status']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Customers SET FirstName=%s, LastName=%s, Email=%s, Phone=%s, Status=%s WHERE CustomerID=%s",
                   (first_name, last_name, email, phone, status, customer_id))
    conn.commit()

    # Fetch updated customer list
    customers = get_customers()

    conn.close()
    return redirect(url_for('customer_details', customer_id=customer_id))

# Route for deleting customer details
@app.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    if request.method == 'POST':
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Perform deletion operation
        cursor.execute("DELETE FROM Customers WHERE CustomerID = %s", (customer_id,))
        conn.commit()
        conn.close()

        # Redirect to the customer list page after deletion
        return redirect(url_for('customer_list'))
    else:
        # For GET requests, you might want to show a confirmation page
        return render_template('confirm_delete.html', customer_id=customer_id)


@app.route('/contact/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    if request.method == 'GET':
        # Fetch contact details from the database based on contact_id
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT ContactID, CustomerID, ContactType, ContactValue FROM contacts WHERE ContactID = %s AND CustomerID = %s", (contact_id, customer_id))
        contact_details = cursor.fetchone()
        conn.close()

        # Print or log the contact details to verify
        print("Contact details:", contact_details)

        # Render a template for editing the contact details
        return render_template('edit_contact.html', contact=contact_details)
    elif request.method == 'POST':
        # Update contact details in the database based on the form submission

        # Fetch the CustomerID of the edited contact
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT CustomerID FROM contacts WHERE ContactID = %s", (contact_id,))
        customer_id = cursor.fetchone()[0]  # Fetch the first column of the result
        conn.close()

        # Redirect to the customer details page
        return redirect(url_for('customer_details', customer_id=customer_id))


@app.route('/contact/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    # Fetch the CustomerID of the contact to redirect to the correct customer details page
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID FROM contacts WHERE ContactID = %s", (contact_id,))
    customer_id = cursor.fetchone()[0]  # Fetch the first column of the result
    conn.close()

    # Delete the contact from the database based on contact_id
    # Redirect to the customer details page
    return redirect(url_for('customer_details', customer_id=customer_id))

@app.route('/customer/<int:customer_id>/add_contact', methods=['GET', 'POST'])
def add_contact(customer_id):
    if request.method == 'GET':
        # Render a template for adding a new contact
        return render_template('add_contact.html', customer_id=customer_id)
    elif request.method == 'POST':
        # Add the new contact to the database based on the form submission
        # Redirect to the customer details page
        return redirect(url_for('customer_details', customer_id=customer_id))


if __name__ == '__main__':
    app.run(debug=True)


