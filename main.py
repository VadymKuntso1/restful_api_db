from flask import Flask, jsonify,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin1':
        return 'password1'
    return None

@auth.error_handler
def unauthorized():
    return 'Unknown user'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable=False)
    disc = db.Column(db.String(200), nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    endTime = db.Column(db.DateTime, default=datetime.utcnow)
    def __str__(self):
        return 'Task: '+str(self.title)

class Applyied(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    disc = db.Column(db.String(200), nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    endTime = db.Column(db.DateTime, default=datetime.utcnow)
    def __str__(self):
        return 'Task: '+str(self.title)


@app.route('/',methods=['GET'])
@auth.login_required
def index():
    list1 = []
    list = ToDoList.query.order_by(ToDoList.createTime).all()
    for element in list:
        list1.append({
        'title': element.title,
        'discription': element.disc,
        'Durings': str(element.endTime - element.createTime)[0:7]
        })
    return jsonify(list1)


@app.route('/add',methods=['post'])
@auth.login_required
def add():
    try:
        tdl = ToDoList()
        tdl.title = request.json.get('title','')
        tdl.disc = request.json.get('discription','')
        tdl.endTime = datetime.utcnow() + timedelta(days = int(request.json.get('days','10')))
        db.session.add(tdl)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return str(e)


@app.route('/remove/<int:id>',methods=['DELETE'])
@auth.login_required
def remove(id):
    try:
        obj = ToDoList.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return str(e)


@app.route('/Apply/<int:id>',methods=['PUT'])
@auth.login_required
def apply(id):
    obj = ToDoList.query.get(id)
    applied = Applyied()
    applied.title = obj.title
    applied.disc = obj.disc
    applied.createTime = obj.createTime
    applied.endTime = obj.endTime
    db.session.delete(obj)
    db.session.add(applied)
    db.session.commit()
    return redirect('/AppliedList')


@app.route('/AppliedList',methods=['GET'])
@auth.login_required
def Appliedlist():
    list1 = []
    list = Applyied.query.order_by(Applyied.createTime).all()
    for element in list:
        list1.append({
            'title': element.title,
            'discription': element.disc,
            'Durings': str(element.endTime - element.createTime)[0:7]
        })
    return jsonify(list1)


@app.route('/removeApplied/<int:id>',methods=['DELETE'])
@auth.login_required
def removeApplied(id):
    try:
        obj = Applyied.query.get(id)
        db.session.delete(obj)
        db.session.commit()
        return redirect('/AppliedList')
    except Exception as E:
        return str(E)

if __name__ == '__main__':
    app.run(debug=True)