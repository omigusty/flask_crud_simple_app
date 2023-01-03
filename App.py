from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = 'e889af71d15a324c18a29b1029e1b629'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flask_simple_crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    title = 'Home'
    employees = Employee.query.all()
    return render_template('index.html', title=title, employees=employees)


@app.route('/insert', methods=['POST'])
def insertData():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        dataEmployee = Employee(name, email, phone)
        db.session.add(dataEmployee)
        db.session.commit()
        flash('Employee inserted successfuly')

        return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def editData():
    dataEmployee = Employee.query.get(request.form.get('id'))

    dataEmployee.name = request.form['name']
    dataEmployee.email = request.form['email']
    dataEmployee.phone = request.form['phone']

    db.session.commit()
    flash('Data updated successfuly')

    return redirect(url_for('index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def deleteData(id):
    dataEmployee = Employee.query.get(id)
    db.session.delete(dataEmployee)
    db.session.commit()
    flash('Employee deleted successfuly')

    return redirect(url_for('index'))
