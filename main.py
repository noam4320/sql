from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # In-memory database for tests

db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    def to_dict(self):
        return {"id":self.id,"name":self.name,"email":self.email}

with app.app_context():

    db.create_all()


@app.route('/')
def index():
    return "this is a database experiment"


@app.route('/person', methods=['POST'])
def create_person():
    post_data = request.get_json()


    new_person = Person( name=post_data["name"],email= post_data["email"])
    db.session.add(new_person)
    db.session.commit()

    return jsonify("ok"), 201


@app.route('/person/<person_id>',methods=['GET'])
def get_person(person_id):
    person = db.session.get(Person, person_id)
    if person_id is None:
        return "user not found",400


    return jsonify(person),200


@app.route('/person/<person_id>', methods=['PATCH'])
def update_person(person_id):
    patch_data = request.get_json()
    if patch_data is None:
        return "no data sent", 400

    user = db.session.query(Person).get(person_id)

    if user is None:
        return "user not found", 400
    if "name" in patch_data:
        user.name = patch_data["name"]
    if "email" in patch_data:
        user.email = patch_data["email"]
    db.session.commit()
    return "user updated ", 200


@app.route('/person/<person_id>', methods=['DELETE'])
def person_delete(person_id):

    user = db.session.get(Person, person_id)
    if user is None:
        return "user not found",400
    db.session.delete(user)
    db.session.commit()
    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)
