from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
# from sqlalchemy.exc import OperationalError



app= Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "restaurent"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/restaurent'
db= SQLAlchemy(app)
app.secret_key="set_anything_what_you_wont"

mysql= MySQL(app)



class Orders(db.Model):
    
    #  sr_no    category    dish    drink    table_no

    __tablename__ = 'orders'
    sr_no = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), unique=False, nullable=False)
    dish = db.Column(db.String(50), unique=False, nullable=False)
    drink = db.Column(db.String(50), unique=False, nullable=False)
    table_no = db.Column(db.String(50), nullable=False)


class Review(db.Model):
    
    #  sr_no    name    email    review

    sr_num = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    review = db.Column(db.String(120), nullable=False)




@app.route("/")
def harsh():
    return render_template("index.html")

@app.route('/Home')
def harsh_home():
    return render_template("index.html")

@app.route('/Order-food', methods = ['GET', 'POST'])
def harsh_orderfood():
    if (request.method =='POST'):
        ''' add entry to the databace '''
        slct1= request.form.get('slct1')
        slct2= request.form.get('slct2')
        drink= request.form.get('drink')
        table= request.form.get('table')

        #  sr_no    category    dish    drink    table_no

        entry= Orders(category= slct1, dish= slct2, drink= drink, table_no= table)
        db.session.add(entry)
        db.session.commit()

    return render_template("order_food.html")       #sucess1="Order send Sucessfully"


@app.route('/About')
def harsh_about():
    return render_template("about.html")

@app.route('/Review', methods = ['GET', 'POST'])
def harsh_review():
    if (request.method =='POST'):
        ''' add entry to the databace '''
        name= request.form.get('name')
        mail= request.form.get('mail')
        review= request.form.get('review')  
        
        # sr_num    name    email    review
        
        entry1= Review(name=name, email=mail, review=review)
        db.session.add(entry1)
        db.session.commit()
    
    return render_template("review.html")                #sucess1="Review send Sucessfully"



@app.route('/Login')
def harsh_login():
    return render_template("login.html")
database={'admin':'1234','harsh':'1234','mhatre':'2222'}




@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']

    if name1 not in database:
	    return render_template('login.html', info='Invalid Username or Password')
    else:
        if database[name1]!=pwd:
            return render_template('login.html', info='Invalid Username or Password')
        else:    
            cur = mysql.connection.cursor()
            orders = cur.execute("SELECT * FROM orders")     
            if orders > 0:
                ordersDetails = cur.fetchall()

            cur = mysql.connection.cursor()
            review = cur.execute("SELECT * FROM review")     
            if review > 0:
                reviewDetails = cur.fetchall()

            return render_template('admin_page.html', name=name1, ordersDetails=ordersDetails , reviewDetails=reviewDetails)
        

@app.route('/logout',methods=['POST','GET'])
def harsh_logout():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)