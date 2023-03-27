from flask import Flask,render_template,request,flash,redirect,url_for
from flask_login import login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hello'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    _id = db.Column('id',db.Integer,primary_key=True)
    email = db.Column('email',db.String(100),nullable = False , unique = True)
    password = db.Column('password',db.String(100),nullable = False)

    def __init__(self,email,password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'

class feedback(db.Model):
    __tablename__ = 'feedback'
    _id = db.Column('id',db.Integer,primary_key=True)
    customer = db.Column('customer',db.String(100),nullable = False)
    product = db.Column('product',db.String(100),nullable = False)
    rating = db.Column('rating',db.Integer)
    comment = db.Column('comment',db.String(500))

    def __init__(self,customer,product,rating,comment):
        self.customer = customer
        self.product = product
        self.rating = rating
        self.comment = comment

@app.route('/' , methods=['POST','GET'])
def start():
    if request.method == 'GET':
        return render_template('base.html')
    email = request.form['email']
    password = request.form['password']
    found_user = User.query.filter_by(email=email).first()
    if not found_user or not found_user.password == password:
        return render_template('base.html', message='Invalid username or password')
    # login_user(found_user)
    return redirect(url_for('submit'))

@app.route('/new_user', methods=['POST','GET'])
def new_user():
    if request.method == 'GET':
        return render_template('new.html')
    email = request.form['email']
    password = request.form['password']
    found_email = User.query.filter_by(email=email).first()
    if found_email:
        return render_template('new.html', message='Username already exists')
    usr = User(email = email,password = password)
    db.session.add(usr)
    db.session.commit()
    flash("New User Added!!!")
    return redirect(url_for('start'))


@app.route('/submit',methods = ['GET','POST'])
# @login_required
def submit():
    if request.method == 'GET':
        return render_template('user.html')
    customer = request.form['customer']
    product = request.form['product']
    rating = request.form['rating']
    comment = request.form['comment']
    if customer=='' or product=='':
        return render_template('user.html',message='Please fill required Data')
    feedback_exist = feedback.query.filter(feedback.customer==customer,feedback.product==product).first()
    if not feedback_exist:
        review = feedback(customer=customer,product=product,rating=rating,comment=comment)
        db.session.add(review)
        db.session.commit()
        return render_template('view.html' , values=feedback.query.all(), message='The modified Database')
    else:
        return render_template('user.html', message='You have already submitted feedback.You can Update it')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    customer = request.form['customer']
    product = request.form['product']
    rating = request.form['rating']
    comment = request.form['comment']
    feedback_exist = feedback.query.filter(feedback.customer==customer,feedback.product==product).first()
    if feedback_exist:
        feedback_exist.rating = rating
        feedback_exist.comment = comment
        db.session.add(feedback_exist)
        db.session.commit()
    return render_template('view.html', values=feedback.query.all(), message='The modified Database')

@app.route('/delete' , methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    customer = request.form['customer']
    product = request.form['product']
    rating = request.form['rating']
    comment = request.form['comment']
    feedback_delete = feedback.query.filter(feedback.customer==customer,feedback.product==product).first()
    if feedback_delete:
        feedback_delete.rating = rating
        feedback_delete.comment = comment
        db.session.delete(feedback_delete)
        db.session.commit()
    return render_template('view.html', values=feedback.query.all(), message='The modified Database')

@app.route('/logout')
# @login_required
def logout():
    # logout_user()
    return redirect(url_for('start'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)