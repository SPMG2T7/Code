from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = getenv('DB_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_URL}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Define Reward Object
class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    access_rights = db.Column(db.Integer, nullable=False)

    def __init__ (self, staff_id, first_name, last_name, department, email, access_rights):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.email = email
        self.access_rights = access_rights


    def json(self):
        return {"staff_id": self.staff_id, "first_name": self.first_name, "last_name": self.last_name,
                "department": self.department, "email": self.email, "access_rights": self.access_rights
                }

# Retrieving all staff data
@app.route("/staff")
def get_all():
    staff_list = Staff.query.all()
    if len(staff_list) != 0:

        return jsonify(
            {
                "code": 200,
                "data": {
                    "staffs": [staff.json() for staff in staff_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no staffs"
        }
    ), 404

# Retrieving specific staff data
@app.route("/staff/<int:staff_id>")
def find_by_staff_id(staff_id):
    staff = Staff.query.filter_by(staff_id=staff_id).first()
    if staff_id:
        return jsonify(
            {
                "code": 200,
                "data": staff.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)