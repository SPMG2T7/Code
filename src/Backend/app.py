from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
import time
from datetime import datetime, timezone
from sqlalchemy import func
import meilisearch


# Loading from .env file
load_dotenv()
DB_URL = getenv('DB_URL')
SEARCH_MASTER_KEY = getenv('SEARCH_MASTER_KEY')

# Start-Connecting to MeiliSearch
client = meilisearch.Client('http://127.0.0.1:7700', SEARCH_MASTER_KEY)
# End-Connecting to MeiliSearch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_URL}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Calculate Days Left From Unix


def days_left_from_unix(unix_timestamp):
    current_time = int(time.time())
    seconds_left = unix_timestamp - current_time
    days_left = seconds_left // (60 * 60 * 24)
    return days_left

# Date Formatter Function to dd-MMM-yyyy from Unix


def convert_unix_to_custom_format(unix_timestamp):
    # Convert the Unix timestamp to a datetime object
    datetime_obj = datetime.utcfromtimestamp(unix_timestamp)

    # Format the datetime object in the desired format
    formatted_date = datetime_obj.strftime('%d-%b-%Y')  # e.g., 12-Dec-2023

    return formatted_date

# Date Formatter Function to convert FE parse data to Unix


def convert_to_unix_timestamp(date_str):
    # Define the format of the input date string
    date_format = "%a %b %d %Y %H:%M:%S GMT%z (%Z)"

    # Parse the date string
    dt = datetime.strptime(date_str, date_format)

    # Convert to UTC timezone
    dt = dt.replace(tzinfo=timezone.utc)

    # Calculate the Unix timestamp
    unix_timestamp = int(dt.timestamp())

    return unix_timestamp

# Define Access Right Object


class Access_Rights(db.Model):
    __tablename__ = 'access_rights'

    access_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False)

    def __init__(self, access_id, type):
        self.access_id = access_id
        self.type = type

    def json(self):
        return {"access_id": self.access_id, "type": self.type}

# Define Staff Object
# Added backref so you can reference all the staff_list under an access_id thr access_rights.staff_list


class Staff(db.Model):
    __tablename__ = 'staff'

    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    current_role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    access_rights = db.Column(db.Integer, db.ForeignKey(
        'access_rights.access_id'), nullable=False)

    # Add a relationship to the Access_Right class
    access_right = db.relationship(
        'Access_Rights', backref='staff_list', lazy=True)

    def __init__(self, staff_id, first_name, last_name, department, current_role, email, access_rights):
        self.staff_id = staff_id
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.current_role = current_role
        self.email = email
        self.access_rights = access_rights

    def json(self):
        return {"staff_id": self.staff_id, "first_name": self.first_name, "last_name": self.last_name,
                "department": self.department, "current_role": self.current_role, "email": self.email, "access_rights": self.access_rights
                }

# Define Role Object


class Role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)
    role_description = db.Column(db.String(256), nullable=False)
    listed_by = db.Column(db.Integer, nullable=False)
    no_of_pax = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    expiry_timestamp = db.Column(db.Integer, nullable=False)

    def __init__(self, role_name, role_description, listed_by, no_of_pax, department, location, expiry_timestamp):
        self.role_name = role_name
        self.role_description = role_description
        self.listed_by = listed_by
        self.no_of_pax = no_of_pax
        self.department = department
        self.location = location
        self.expiry_timestamp = expiry_timestamp

    def json(self):
        return {"role_id": self.role_id,
                "role_name": self.role_name,
                "role_description": self.role_description,
                "listed_by": self.listed_by,
                "no_of_pax": self.no_of_pax,
                "department": self.department,
                "location": self.location,
                "expiry_date": self.expiry_timestamp,
                }

# Define Skill Object


class Skill(db.Model):
    __tablename__ = 'skill'

    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(50), nullable=False)
    skill_description = db.Column(db.String(256), nullable=False)

    def __init__(self, skill_id, skill_name, skill_description):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.skill_description = skill_description

    def json(self):
        return {"skill_id": self.skill_id, "skill_name": self.skill_name, "skill_description": self.skill_description}

# Define Role_Skill Object
# Added backref so you can access all the skills_needed for the role thru role.skills_needed


class Role_Skill(db.Model):
    __tablename__ = 'role_skill'

    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.role_id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skill.skill_id'), primary_key=True)

    # Add a relationship to the foreign class
    role = db.relationship('Role', backref='skills_needed', lazy=True)
    skill = db.relationship('Skill', backref='skills_in_roles', lazy=True)

    def __init__(self, role_id, skill_id):
        self.role_id = role_id
        self.skill_id = skill_id

    def json(self):
        return {"role_id": self.role_id, "skill_id": self.skill_id}

# Define Staff_Skill Object
# Added backref so you can access all the skills staff has thru staff.staff_skills


class Staff_Skill(db.Model):
    __tablename__ = 'staff_skill'

    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.staff_id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey(
        'skill.skill_id'), primary_key=True)

    # Add a relationship to the foreign class
    staff = db.relationship('Staff', backref='staff_skills', lazy=True)
    skill = db.relationship('Skill', lazy=True)

    def __init__(self, staff_id, skill_id):
        self.staff_id = staff_id
        self.skill_id = skill_id

    def json(self):
        return {"staff_id": self.staff_id, "skill_id": self.skill_id}

# Define Role_Applicant Object
# Added backref so you can access staff info for a specific role thru role.applicants


class Role_Applicant(db.Model):
    __tablename__ = 'role_applicant'

    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.role_id'), primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'staff.staff_id'), primary_key=True)
    comments = db.Column(db.String(50), nullable=True)
    creation_timestamp = db.Column(db.Integer, nullable=False)

    # Add a relationship to the foreign class
    role = db.relationship('Role', backref='applicants', lazy=True)
    staff = db.relationship('Staff', lazy=True)

    def __init__(self, role_id, staff_id, comments, creation_timestamp):
        self.role_id = role_id
        self.staff_id = staff_id
        self.comments = comments
        self.creation_timestamp = creation_timestamp

    def json(self):
        return {"role_id": self.role_id, "staff_id": self.staff_id, "comments": self.comments, "creation_timestamp": self.creation_timestamp}

# Retrieving all staff data


@app.route("/staff/get_all")
def get_all_staff():
    staffs = Staff.query.all()
    staff_list = []
    if len(staffs) != 0:
        for staff in staffs:
            staff_skills = [
                skill.skill.skill_name for skill in staff.staff_skills]
            staff_data = {
                "staff_id": staff.staff_id,
                "first_name": staff.first_name,
                "last_name": staff.last_name,
                "email": staff.email,
                "department": staff.department,
                "current_role": staff.current_role,
                "access_rights": staff.access_rights,
                "staff_skills": staff_skills

            }
            staff_list.append(staff_data)

        return jsonify(
            {
                "code": 200,
                "data": {
                    "staffs": staff_list
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
    staff_data = {}
    if staff:
        staff_skills = [skill.skill.skill_name for skill in staff.staff_skills]
        staff_data = {
            "staff_id": staff.staff_id,
            "first_name": staff.first_name,
            "last_name": staff.last_name,
            "email": staff.email,
            "department": staff.department,
            "current_role": staff.current_role,
            "access_rights": staff.access_rights,
            "staff_skills": staff_skills
        }

        return jsonify(
            {
                "code": 200,
                "data": staff_data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Staff not found."
        }
    ), 404

# Retrieving all access data


@app.route("/access_rights/get_all")
def get_all_access():
    access_list = Access_Rights.query.all()
    if len(access_list) != 0:

        return jsonify(
            {
                "code": 200,
                "data": {
                    "accesses": [access.json() for access in access_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no access rights"
        }
    ), 404

# Retrieving specific access data


@app.route("/access_rights/<int:access_id>")
def find_by_access_id(access_id):
    access = Access_Rights.query.filter_by(access_id=access_id).first()
    if access:
        return jsonify(
            {
                "code": 200,
                "data": access.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Access not found."
        }
    ), 404

# Retrieving all role data


@app.route("/roles/get_all")
def get_all_roles():
    roles = Role.query.all()
    role_list = []
    if len(roles) != 0:
        for role in roles:
            skills_required = [
                skill.skill.skill_name for skill in role.skills_needed]
            count_of_applicant = Role_Applicant.query.filter_by(
                role_id=role.role_id).count()
            role_data = {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "role_description": role.role_description,
                "listed_by": role.listed_by,
                "no_of_pax": role.no_of_pax,
                "department": role.department,
                "location": role.location,
                "days_left": days_left_from_unix(role.expiry_timestamp),
                "expiry_date": convert_unix_to_custom_format(role.expiry_timestamp),
                # 1. Missing number of people that applied
                # Select count(role_id) from role_applicant where role_id = ?
                "count_applicant": count_of_applicant,
                # 2. Skills required for this role (should be multiple)
                "skills_required": skills_required

            }
            role_list.append(role_data)

        return jsonify(
            {
                "code": 200,
                "data": {
                    "roles": role_list
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no roles"
        }
    ), 404

# Retrieving specific access data


@app.route("/roles/<int:role_id>")
def find_by_role_id(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    role_data = {}
    if role:
        skills_required = [
            skill.skill.skill_name for skill in role.skills_needed]
        count_of_applicant = Role_Applicant.query.filter_by(
            role_id=role.role_id).count()
        role_data = {
            "role_id": role.role_id,
            "role_name": role.role_name,
            "role_description": role.role_description,
            "listed_by": role.listed_by,
            "no_of_pax": role.no_of_pax,
            "department": role.department,
            "location": role.location,
            "days_left": days_left_from_unix(role.expiry_timestamp),
            "expiry_date": convert_unix_to_custom_format(role.expiry_timestamp),
            # 1. Missing number of people that applied
            # Select count(role_id) from role_applicant where role_id = ?
            "count_applicant": count_of_applicant,
            # 2. Skills required for this role (should be multiple)
            "skills_required": skills_required

        }
        return jsonify(
            {
                "code": 200,
                "data": role_data
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Role not found."
        }
    ), 404

# Create Roles


@app.route("/roles/create", methods=["POST"])
def create_role():
    data = request.get_json()
    # Retrieve the parameters from the POST request data
    role_name = data['params']['role_name']
    role_description = data['params']['role_description']
    skills_required = data['params']['skills_required']
    listed_by = data['params']['listed_by']
    no_of_pax = data['params']['no_of_pax']
    department = data['params']['department']
    location = data['params']['location']
    expiry_timestamp = data['params']['expiry_timestamp']

    try:
        # Create a new instance of the Role model with the retrieved parameters
        role = Role(
            role_name=role_name,
            role_description=role_description,
            listed_by=listed_by,
            no_of_pax=no_of_pax,
            department=department,
            location=location,
            expiry_timestamp=convert_to_unix_timestamp(expiry_timestamp)
        )

        # Add the new role to the session
        db.session.add(role)

        # Create Role_Skill object and commit per skill
        for skill in skills_required:
            # Get Skill ID per Skill Name
            skill_id = Skill.query.filter_by(
                skill_name=skill).with_entities(Skill.skill_id).first()
            role_skill = Role_Skill(role.role_id, skill_id[0])
            db.session.add(role_skill)

        # Commit the session to save the new role to the database
        db.session.commit()
        
        # Start-Adding to MeiliSearch
        client.index('roles').add_documents([
            {
                "role_id": role.role_id,
                "role_name": role_name,
                "role_description": role_description,
                "listed_by": listed_by,
                "no_of_pax": no_of_pax,
                "department": department,
                "expiry_date": convert_unix_to_custom_format(role.expiry_timestamp),
                "skills_required": skills_required,
                "location": location,
                "days_left": days_left_from_unix(role.expiry_timestamp),
                "count_applicant": 0
            }
        ], primary_key='role_id')
        # End-Adding to MeiliSearch

    except Exception as e:
        error_message = str(e)
        return jsonify(
            {
                "code": 500,
                "data": error_message,
                "message": "Internal Server Error: An unexpected error occurred."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": role.json()
        }
    ), 201

# Retrieving all skills data


@app.route("/skills/get_all")
def get_all_skills():
    skill_list = Skill.query.all()
    if len(skill_list) != 0:

        return jsonify(
            {
                "code": 200,
                "data": {
                    "skills": [skill.json() for skill in skill_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skills"
        }
    ), 404

# Retrieving specific skill data
@app.route("/skills/<int:skill_id>")
def find_by_skill_id(skill_id):
    skill = Skill.query.filter_by(skill_id=skill_id).first()
    if skill:
        return jsonify(
            {
                "code": 200,
                "data": skill.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Skill not found."
        }
    ), 404

# Retrieve search result from the Search Index
@app.route("/search/", methods=["POST"])
def search():
    req = request.get_json()
    search_query = req['params']['search_query']
    if len(search_query) == 1:
        search_result = client.index('roles').search(search_query[0])
        if len(search_result["hits"]) != 0:
            return jsonify(
                {
                    "code": 200,
                    "data": search_result["hits"]
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "data": [],
                "message": "There are no results matching your query"
            }
        ), 404
    else:
        searches = []
        for query in search_query:
            # print(query)
            searches.append({'indexUid': 'roles', 'q': query})
        # print(searches)
        search_result = client.multi_search(searches)
        print(search_result['results'])
        if len(search_result["results"]) != 0:
            hits = []
            for entry in search_result['results']:
                for hit in entry['hits']:
                    hits.append(hit)
            return jsonify(
                {
                    "code": 200,
                    "data": hits
                }
            ), 200
        return jsonify(
            {
                "code": 404,
                "data": [],
                "message": "There are no results matching your query"
            }
        ), 404

# Retrieve all applications for a specific role
@app.route("/application/<int:role_id>_<int:staff_id>", methods=["GET"])
def get_application(role_id,staff_id):

    query_role_id = role_id
    query_staff_id = staff_id

    # Ensure that the application exists

    application = Role_Applicant.query.filter_by(role_id=query_role_id,staff_id = query_staff_id).first()
    if application:


        # Get all information regarding the role

        role = Role.query.filter_by(role_id=query_role_id).first()
        role_data = {}
        if role:
            skills_required = [
                skill.skill.skill_name for skill in role.skills_needed]
            count_of_applicant = Role_Applicant.query.filter_by(
                role_id=role.role_id).count()
            role_data = {
                "role_id": role.role_id,
                "role_name": role.role_name,
                "role_description": role.role_description,
                "listed_by": role.listed_by,
                "no_of_pax": role.no_of_pax,
                "department": role.department,
                "location": role.location,
                "days_left": days_left_from_unix(role.expiry_timestamp),
                "expiry_date": convert_unix_to_custom_format(role.expiry_timestamp),
                # 1. Missing number of people that applied
                # Select count(role_id) from role_applicant where role_id = ?
                "count_applicant": count_of_applicant,
                # 2. Skills required for this role (should be multiple)
                "skills_required": skills_required

            }

            # Get all information regarding the staff

            staff = Staff.query.filter_by(staff_id=query_staff_id).first()
            staff_data = {}
            if staff:
                staff_skills = [skill.skill.skill_name for skill in staff.staff_skills]
                staff_data = {
                    "staff_id": staff.staff_id,
                    "first_name": staff.first_name,
                    "last_name": staff.last_name,
                    "email": staff.email,
                    "department": staff.department,
                    "current_role": staff.current_role,
                    "access_rights": staff.access_rights,
                    "staff_skills": staff_skills
                }

                return jsonify(
                    {
                        "code": 200,
                        "data": {'role_data': role_data,'staff_data':staff_data}
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Staff not found."
                    }
                ), 404
        
        else:
            return jsonify(
                {
                    "code": 404,
                    "message": "Role not found."
                }
            ), 404
    else:

        return jsonify(
            {
                "code": 404,
                "message": "Application not found."
            }
        ), 404


# Apply for Role
@app.route("/roles/apply", methods=["POST"])
def apply_role():
    data = request.get_json()
    # Retrieve the parameters from the POST request data
    role_id = data['params']['role_id']
    staff_id = data['params']['staff_id']
    comments = data['params']['comments']

    try:
        # Create a new instance of the Role model with the retrieved parameters
        role_applicant = Role_Applicant(
            role_id=role_id,
            staff_id=staff_id,
            comments=comments,
            creation_timestamp=int(time.time())
        )

        # Add the new role to the session
        db.session.add(role_applicant)

        # Commit the session to save the new role to the database
        db.session.commit()
        
    except Exception as e:
        error_message = str(e)
        return jsonify(
            {
                "code": 500,
                "data": error_message,
                "message": "Internal Server Error: An unexpected error occurred."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": role_applicant.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
