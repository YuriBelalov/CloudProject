# Main file for Shirts4Mike

# Import statement
from flask import (
    Flask,
    render_template,
    Markup,
    url_for,
    flash,
    redirect,
    request,
    jsonify,
    session
)

import mysql.connector
import sendgrid
from datetime import date

# App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"

# Get details for sendgrid details
sendgrid_file = "/opt/sendgrid.txt"
sendgrid_details = []

with open(sendgrid_file) as f:
    sendgrid_details = f.readlines()
    sendgrid_details = [x.strip("\n") for x in sendgrid_details]


# Global Variables
products_info = [
    {
        "id": "101",
        "name": "Logo Shirt, Red",
        "img": "shirt-101.jpg",
        "price": 18,
        "paypal": "LNRBY7XSXS5PA",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "102",
        "name": "Mike the Frog Shirt, Black",
        "img": "shirt-102.jpg",
        "price": 20,
        "paypal": "XP8KRXHEXMQ4J",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "103",
        "name": "Mike the Frog Shirt, Blue",
        "img": "shirt-103.jpg",
        "price": 20,
        "paypal": "95C659J3VZGNJ",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "104",
        "name": "Logo Shirt, Green",
        "img": "shirt-104.jpg",
        "price": 18,
        "paypal": "Z5EY4SJN64SLU",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "105",
        "name": "Mike the Frog Shirt, Yellow",
        "img": "shirt-105.jpg",
        "price": 25,
        "paypal": "RYAGP5EWG4V4G",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "106",
        "name": "Logo Shirt, Gray",
        "img": "shirt-106.jpg",
        "price": 20,
        "paypal": "QYHDD4N4SMUKN",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "107",
        "name": "Logo Shirt, Teal",
        "img": "shirt-107.jpg",
        "price": 20,
        "paypal": "RSDD7RPZFPQTQ",
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "108",
        "name": "Mike the Frog Shirt, Orange",
        "img": "shirt-108.jpg",
        "price": 25,
        "paypal": "LFRHBPYZKHV4Y",
        "sizes": ["Small", "Medium", "Large"]
    }
]

# Functions


def get_list_view_html(product):
    """Function to return html for given shirt

    The product argument should be a dictionary in this structure:
    {
        "id": "shirt_id",
        "name": "name_of_shirt",
        "img": "image_name.jpg",
        "price": price_of_shirt_as_int_or_flat,
        "paypal": "paypal_id"
        "sizes": ["array_of_sizes"]
    }

    The html is returned in this structure:
    <li>
      <a href="shirt/shirt_id">
        <img src="/static/shirt_img" alt="shirt_name">
        <p>View Details</p>
      </a>
    </li>
    """
    output = ""
    image_url = url_for("static", filename=product["img"])
    shirt_url = url_for("shirt", product_id=product["id"])
    output = output + "<li>"
    output = output + '<a href="' + shirt_url + '">'
    output = (
        output + '<img src="' + image_url +
        '" al  t="' + product["name"] + '">')
    output = output + "<p>View Details</p>"
    output = output + "</a>"
    output = output + "</li>"

    return output


# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    if 'username' not in session:
        return render_template("login.html", **context)
    """Function for Shirts4Mike Homepage"""
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    counter = 0
    product_data = []
    for product in products_info:
        counter += 1
        if counter < 5:  # Get first 4 shirts
            product_data.append(
                Markup(get_list_view_html(product))
            )
    context["product_data"] = Markup("".join(product_data))
    context['username'] = session['username']
    return render_template("index.html", **context)


@app.route("/shirts")
def shirts():
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    if 'username' not in session:
        return render_template("login.html", **context)
    """Function for the Shirts Listing Page"""
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    product_data = []
    for product in products_info:
        product_data.append(Markup(get_list_view_html(product)))
    context["product_data"] = Markup("".join(product_data))
    context['username'] = session['username']
    return render_template("shirts.html", **context)


@app.route("/shirt/<product_id>")
def shirt(product_id):
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    if 'username' not in session:
        return render_template("login.html", **context)
    """Function for Individual Shirt Page"""
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    my_product = ""
    for product in products_info:
        if product["id"] == product_id:
            my_product = product
    context["product"] = my_product
    context['username'] = session['username']
    return render_template("shirt.html", **context)


@app.route("/receipt")
def receipt():
    """Function to display receipt after purchase"""
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    return render_template("receipt.html", **context)


@app.route("/contact")
def contact():
    """Function for contact page"""
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    return render_template("contact.html", **context)


# Route to send email
@app.route("/send", methods=['POST'])
def send():
    """Function to send email using sendgrid API"""
    sendgrid_object = sendgrid.SendGridClient(
        sendgrid_details[0], sendgrid_details[1])
    message = sendgrid.Mail()
    sender = request.form["email"]
    subject = request.form["name"]
    body = request.form["message"]
    message.add_to("charlie.thomas@attwoodthomas.net")
    message.set_from(sender)
    message.set_subject(subject)
    message.set_html(body)
    sendgrid_object.send(message)
    flash("Email sent.")
    return redirect(url_for("contact"))

# Process order
@app.route("/order", methods=['POST'])
def order():
    item = request.form.get('item_name')
    size = request.form.get('os0')
    username = session['username']
    add_item = ("REPLACE INTO cart "
              "(user, item, size) "
              "VALUES (%s, %s, %s)")
    item_data = (username,item,size)
    cursor.execute(add_item,item_data)
    cnx.commit()
    return redirect('/')

# Handle login
@app.route('/login', methods=['GET', 'POST'])
def login():
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    if request.method == 'GET':
        if 'username' not in session:
            return render_template("login.html", **context)
        else:
            return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_password(username,password)==True:
            session['username'] = username
            return redirect('/')
        else:
            return render_template("login.html", **context)

@app.route('/cart', methods=['GET'])
def cart():
    context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    query = "select * from cart where user = '{}'"
    cursor.execute(query.format(session['username']))
    rows = ''
    for (a,b,c,d) in cursor:
        rows += "{},{},{},{}<br>".format(a,b,c,d)
    context['cart'] = rows
    context['test'] = 'test'
    return render_template("cart.html", **context)

# Handle logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/login')

def check_password(username,password):
    if username == 'yuri':
        if password == '123456':
            return True
    return False

# Run application
if __name__ == "__main__":
    cnx = mysql.connector.connect(user='admin', password='admin123456',
                              host='mysql-project.choogkasoh9t.us-east-1.rds.amazonaws.com',
                              database='shop')
    cursor = cnx.cursor()
    app.run(debug=True,host='0.0.0.0')
