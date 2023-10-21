import flask_testing
import unittest
import json
from app import app, db, Access_Rights, Staff, Role, Skill, Role_Skill, Staff_Skill, Role_Applicant, days_left_from_unix
from unittest.mock import patch

class TestApp(flask_testing.TestCase):
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestGetStaff(TestApp):
    # Testing for the endpoint /staff/get_all
    def test_get_all_staff(self):
        access_rights1 = Access_Rights(access_id=1, type="Admin")
        access_rights2 = Access_Rights(access_id=2, type="User")
        access_rights3 = Access_Rights(access_id=3, type="Manager")
        db.session.add(access_rights1)
        db.session.add(access_rights2)
        db.session.add(access_rights3)
        db.session.commit()

        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        staff3 = Staff(staff_id=3, first_name="Zong", last_name="Wei",
                       email="ZongWei@gmail.com", department="IT", current_role="Software Junior",
                       access_rights=2)
        staff4 = Staff(staff_id=4, first_name="Poppy", last_name="Lim",
                       email="Poppy@gmail.com", department="Sales", current_role="Sales manager",
                       access_rights=3)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.add(staff3)
        db.session.add(staff4)
        db.session.commit()

        response = self.client.get(
            '/staff/get_all', content_type='application/json')

        self.assertEqual(response.json["data"]["staffs"], [
            {
                "access_rights": 1,
                "current_role": "Software Engineer",
                "department": "IT",
                "email": "JohnTan@gmail.com",
                "first_name": "John",
                "last_name": "Tan",
                "staff_id": 1,
                "staff_skills": [

                ]
            },
            {
                "access_rights": 2,
                "current_role": "Ops Engineer",
                "department": "OT",
                "email": "TonyLin@gmail.com",
                "first_name": "Tony",
                "last_name": "Lim",
                "staff_id": 2,
                "staff_skills": [

                ]
            },
            {
                "access_rights": 2,
                "current_role": "Software Junior",
                "department": "IT",
                "email": "ZongWei@gmail.com",
                "first_name": "Zong",
                "last_name": "Wei",
                "staff_id": 3,
                "staff_skills": [

                ]
            },
            {
                "access_rights": 3,
                "current_role": "Sales manager",
                "department": "Sales",
                "email": "Poppy@gmail.com",
                "first_name": "Poppy",
                "last_name": "Lim",
                "staff_id": 4,
                "staff_skills": [
                ]
            },
        ]
        )

    def test_get_all_staff_empty(self):
        response = self.client.get(
            '/staff/get_all', content_type='application/json')

        self.assertEqual(response.json["message"], 'There are no staffs')

    # Testing for the endpoint /staff/<int:staff_id>
    def test_get_specific_staff(self):
        access_rights1 = Access_Rights(access_id=1, type="Admin")
        access_rights2 = Access_Rights(access_id=2, type="User")
        access_rights3 = Access_Rights(access_id=3, type="Manager")

        db.session.add(access_rights1)
        db.session.add(access_rights2)
        db.session.add(access_rights3)
        db.session.commit()

        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        staff3 = Staff(staff_id=3, first_name="Zong", last_name="Wei",
                       email="ZongWei@gmail.com", department="IT", current_role="Software Junior",
                       access_rights=2)
        staff4 = Staff(staff_id=4, first_name="Poppy", last_name="Lim",
                       email="Poppy@gmail.com", department="Sales", current_role="Sales manager",
                       access_rights=3)

        db.session.add(staff1)
        db.session.add(staff2)
        db.session.add(staff3)
        db.session.add(staff4)
        db.session.commit()

        response = self.client.get(
            '/staff/1', content_type='application/json')

        self.assertEqual(response.json[0]['data'], {
            'access_rights': 1,
            'current_role': 'Software Engineer',
            'department': 'IT',
            'email': 'JohnTan@gmail.com',
            'first_name': 'John',
            'last_name': 'Tan',
            'staff_id': 1,
            'staff_skills': []
        }
        )

    def test_get_specific_staff_not_found(self):
        response = self.client.get(
            '/staff/5', content_type='application/json')

        self.assertEqual(response.json["message"], 'Staff not found.')


class TestGetRoles(TestApp):
    # Testing for the endpoint /role/get_all
    def test_get_all_role_listing(self):
        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        role3 = Role(role_name="Software Junior", role_description="Develop software", listed_by=1,
                     no_of_pax=1, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role4 = Role(role_name="Sales manager", role_description="Manage sales", listed_by=3,
                     no_of_pax=1, department="Sales", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.add(role4)
        db.session.commit()

        response = self.client.get(
            '/roles/get_all', content_type='application/json')

        self.assertEqual(response.json["data"]["roles"],
                         [
            {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                                    "role_id": 1,
                                    "role_name": "Software Engineer",
                                    "skills_required": []
            },
            {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "OT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 2,
                "location": "Singapore",
                "no_of_pax": 2,
                "role_description": "Maintain servers",
                                    "role_id": 2,
                                    "role_name": "Ops Engineer",
                                    "skills_required": []
            },
            {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 1,
                "role_description": "Develop software",
                                    "role_id": 3,
                                    "role_name": "Software Junior",
                                    "skills_required": []
            },
            {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "Sales",
                "expiry_date": "01-Dec-2023",
                "listed_by": 3,
                "location": "Singapore",
                "no_of_pax": 1,
                "role_description": "Manage sales",
                                    "role_id": 4,
                                    "role_name": "Sales manager",
                                    "skills_required": []
            }
        ]
        )

    def test_get_all_role_listing_empty(self):
        response = self.client.get(
            '/roles/get_all', content_type='application/json')

        self.assertEqual(response.json["message"], 'There are no roles')

    # Testing for the endpoint /roles/get_all_by_staff/<int:staff_id>
    def test_get_all_role_listing_by_staff(self):
        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        role3 = Role(role_name="Software Junior", role_description="Develop software", listed_by=1,
                     no_of_pax=1, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role4 = Role(role_name="Sales manager", role_description="Manage sales", listed_by=3,
                     no_of_pax=1, department="Sales", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.add(role4)
        db.session.commit()

        access_rights1 = Access_Rights(access_id=1, type="Admin")
        access_rights2 = Access_Rights(access_id=2, type="User")
        access_rights3 = Access_Rights(access_id=3, type="Manager")
        db.session.add(access_rights1)
        db.session.add(access_rights2)
        db.session.add(access_rights3)
        db.session.commit()

        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.commit()

        role_applicant1 = Role_Applicant(
            role_id=1, staff_id=1, comments="test", creation_timestamp=1695174041)
        role_applicant2 = Role_Applicant(
            role_id=1, staff_id=2, comments="test", creation_timestamp=1695174041)
        db.session.add(role_applicant1)
        db.session.add(role_applicant2)
        db.session.commit()

        response = self.client.get(
            '/roles/get_all_by_staff/1', content_type='application/json')

        self.assertEqual(response.json["data"]["roles"],
                         [
            {
                "applied": True,
                "count_applicant": 2,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                                    "role_id": 1,
                                    "role_name": "Software Engineer",
                                    "skills_required": [],
            },
            {
                "applied": False,
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "OT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 2,
                "location": "Singapore",
                "no_of_pax": 2,
                "role_description": "Maintain servers",
                                    "role_id": 2,
                                    "role_name": "Ops Engineer",
                                    "skills_required": [],
            },
            {
                "applied": False,
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 1,
                "role_description": "Develop software",
                                    "role_id": 3,
                                    "role_name": "Software Junior",
                                    "skills_required": [],
            },
            {
                "applied": False,
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "Sales",
                "expiry_date": "01-Dec-2023",
                "listed_by": 3,
                "location": "Singapore",
                "no_of_pax": 1,
                "role_description": "Manage sales",
                                    "role_id": 4,
                                    "role_name": "Sales manager",
                                    "skills_required": [],
            }
        ]
        )

    def test_get_all_role_listing_by_staff_empty(self):
        response = self.client.get(
            '/roles/get_all_by_staff/1', content_type='application/json')

        self.assertEqual(response.json["message"], 'There are no roles')

    def test_get_role_by_id(self):
        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        role3 = Role(role_name="Software Junior", role_description="Develop software", listed_by=1,
                     no_of_pax=1, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role4 = Role(role_name="Sales manager", role_description="Manage sales", listed_by=3,
                     no_of_pax=1, department="Sales", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.add(role4)
        db.session.commit()

        response = self.client.get(
            '/roles/1', content_type='application/json')

        self.assertEqual(response.json["data"], 
            {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                                    "role_id": 1,
                                    "role_name": "Software Engineer",
                                    "skills_required": []
            },
        )

    def test_get_role_by_id_empty(self):
        response = self.client.get(
            '/roles/1', content_type='application/json')

        self.assertEqual(response.json["message"], 'Role not found.')

class TestCreateRole(TestApp):
    # Testing for the endpoint /roles/create
    def test_create_role(self):
        requst_body = {
            'params': {
                'department': 'IT',
                'expiry_timestamp': "Mon Dec 01 2023 00:00:00 GMT+0000 (UTC)",
                'role_name': 'Software Engineer',
                'role_description': 'Develop software',
                'listed_by': 1,
                'no_of_pax': 3,
                'location': 'Singapore',
                'skills_required': []
            },
        }

        response = self.client.post(
            '/roles/create', data=json.dumps(requst_body), content_type='application/json')
        
        self.assertEqual(response.json['data'], {
                'department': 'IT',
                'expiry_date': 1701388800,
                'listed_by': 1,
                'location': 'Singapore',
                'no_of_pax': 3,
                'role_id': 1,
                'role_name': 'Software Engineer',
                'role_description': 'Develop software',
            })

    def test_create_role_error(self):
        # Catches error will include incomplete request body
        requst_body = {
            'params': {
                'department': 'IT',
                'expiry_timestamp': "Mon Dec 12 2023 00:00:00 GMT+0000 (UTC)",
                'role_name': 'Software Engineer',
                'role_description': 'Develop software',
                'listed_by': 1,
                'location': 'Singapore',
                'skills_required': []
            }
        }
        
        with self.assertRaises(Exception):
            self.client.post(
            '/roles/create', data=json.dumps(requst_body), content_type='application/json')

class TestGetSkills(TestApp):
    # Testing for the endpoint /skills/get_all
    def test_get_all_skills(self):
        skill1 = Skill(skill_id=1, skill_name="Python", skill_description="Programming language")
        skill2 = Skill(skill_id=2, skill_name="Java", skill_description="Programming language")
        skill3 = Skill(skill_id=3, skill_name="C++", skill_description="Programming language")

        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(skill3)
        db.session.commit()

        response = self.client.get(
            '/skills/get_all', content_type='application/json')
        
        self.assertEqual(response.json["data"]["skills"], [
            {
                "skill_description": "Programming language",
                "skill_id": 1,
                "skill_name": "Python"
            },
            {
                "skill_description": "Programming language",
                "skill_id": 2,
                "skill_name": "Java"
            },
            {
                "skill_description": "Programming language",
                "skill_id": 3,
                "skill_name": "C++"
            }
        ])

    def test_get_all_skills_empty(self):
        response = self.client.get(
            '/skills/get_all', content_type='application/json')

        self.assertEqual(response.json["message"], 'There are no skills')

    # Testing for the endpoint /skills/<int:skill_id>
    def test_get_specific_skill(self):
        skill1 = Skill(skill_id=1, skill_name="Python", skill_description="Programming language")
        skill2 = Skill(skill_id=2, skill_name="Java", skill_description="Programming language")
        skill3 = Skill(skill_id=3, skill_name="C++", skill_description="Programming language")

        db.session.add(skill1)
        db.session.add(skill2)
        db.session.add(skill3)
        db.session.commit()

        response = self.client.get(
            '/skills/1', content_type='application/json')
        
        self.assertEqual(response.json["data"], 
            {
                "skill_description": "Programming language",
                "skill_id": 1,
                "skill_name": "Python"
            },
        )

    def test_get_specific_skill_not_found(self):
        response = self.client.get(
            '/skills/1', content_type='application/json')
        
        self.assertEqual(response.json['message'], "Skill not found." )

class TestSearch(TestApp):
    # Testing for the endpoint /search      

    def test_search_single_word(self):
        request_body = {
            'params': {
                'search_query': ['Software']
            }
        }

        response = self.client.post(
            '/search/', data=json.dumps(request_body), content_type='application/json')
        
        self.assertEqual(response.json["data"], [ {
                        "count_applicant": 0,
                        "days_left": days_left_from_unix(1701388800),
                        "department": "IT",
                        "expiry_date": "01-Dec-2023",
                        "listed_by": 1,
                        "location": "Singapore",
                        "no_of_pax": 3,
                        "role_description": "Develop software",
                        "role_id": 1,
                        "role_name": "Software Engineer",
                        "skills_required": [
                        ]
                    }
            ])

    def test_search_no_result(self):
        request_body = {
            'params': {
                'search_query': ['qwertyuiop']
            }
        }
        response = self.client.post(
            '/search/', data=json.dumps(request_body), content_type='application/json')
        
        self.assertEqual(response.json['message'], "There are no results matching your query" )

    def test_search_multi_word(self):
        request_body = {
            'params': {
                'search_query': ['Software', 'Engineer']
            }
        }

        response = self.client.post(
            '/search/', data=json.dumps(request_body), content_type='application/json')

        self.assertEqual(response.json["data"], [ {
                        "count_applicant": 0,
                        "days_left": days_left_from_unix(1701388800),
                        "department": "IT",
                        "expiry_date": "01-Dec-2023",
                        "listed_by": 1,
                        "location": "Singapore",
                        "no_of_pax": 3,
                        "role_description": "Develop software",
                        "role_id": 1,
                        "role_name": "Software Engineer",
                        "skills_required": [
                        ]
                    }
            ])

    def test_search_multi_word_no_result(self):
        request_body = {
            'params': {
                'search_query': ['nowords1', 'nowords2']
            }
        }

        response = self.client.post(
            '/search/', data=json.dumps(request_body), content_type='application/json')
        
        self.assertEqual(len(response.json['data']), 0 )

class TestGetApplication(TestApp):
    # Testing /application/<int:role_id>_<int:staff_id>
    def testing_get_application(self):
        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.commit()

        role_applicant1 = Role_Applicant(
            role_id=1, staff_id=1, comments="test", creation_timestamp=1695174041)
        role_applicant2 = Role_Applicant(
            role_id=1, staff_id=2, comments="test", creation_timestamp=1695174041)
        db.session.add(role_applicant1)
        db.session.add(role_applicant2)
        db.session.commit()

        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        response = self.client.get(
            '/application/1_1', content_type='application/json')
        
        self.assertEqual(response.json['data'], {
            'application_data': {
                'comments': 'test',
                'creation_timestamp': 1695174041,
            },
            'role_data': {
                "count_applicant": 2,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                "role_id": 1,
                "role_name": "Software Engineer",
                "skills_required": [],
            },
            'staff_data': {
                "access_rights": 1,
                "current_role": "Software Engineer",
                "department": "IT",
                "email": "JohnTan@gmail.com",
                "first_name": "John",
                "last_name": "Tan",
                "staff_id": 1,
                "staff_skills": [

                ]
            },
        })

    def testing_get_application_empty_application(self):
        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.commit()

        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        response = self.client.get(
            '/application/1_1', content_type='application/json')
        
        self.assertEqual(response.json['message'], 'Application not found.' )

    def testing_get_application_no_role_found(self):
        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.commit()

        role_applicant1 = Role_Applicant(
            role_id=1, staff_id=1, comments="test", creation_timestamp=1695174041)
        role_applicant2 = Role_Applicant(
            role_id=1, staff_id=2, comments="test", creation_timestamp=1695174041)
        db.session.add(role_applicant1)
        db.session.add(role_applicant2)
        db.session.commit()

        response = self.client.get(
            '/application/1_1', content_type='application/json')
        
        self.assertEqual(response.json['message'], 'Role not found.' )

    def testing_get_application_no_staff_found(self):
        role_applicant1 = Role_Applicant(
            role_id=1, staff_id=1, comments="test", creation_timestamp=1695174041)
        role_applicant2 = Role_Applicant(
            role_id=1, staff_id=2, comments="test", creation_timestamp=1695174041)
        db.session.add(role_applicant1)
        db.session.add(role_applicant2)
        db.session.commit()

        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        response = self.client.get(
            '/application/1_1', content_type='application/json')

        self.assertEqual(response.json['message'], 'Staff not found.' )

class TestRole(TestApp):
    # Testing /roles/apply
    @patch('time.time', return_value=1701388795)
    def test_apply_role(self, mock_time):
        request_body = {
            'params': {
                'role_id': 1,
                'staff_id': 1,
                'comments': 'test'
            }
        }

        response = self.client.post(
            '/roles/apply', data=json.dumps(request_body), content_type='application/json')
        
        self.assertEqual(response.json['data'], {
            "comments": "test",
            "creation_timestamp": 1701388795,
            "role_id": 1,
            "staff_id": 1
        })

    def test_apply_role_error(self):
        request_body = {
            'params': {
                'role_id': 1,
                'comments': 'test'
            }
        }

        with self.assertRaises(Exception):
            self.client.post(
            '/roles/apply', data=json.dumps(request_body), content_type='application/json')

    # Testing /roles/update
    def test_update_role(self):
        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.commit()

        request_body = {
            'params': {
                'department': 'IT',
                'expiry_timestamp': 'Mon Dec 01 2023 00:00:00 GMT+0000 (UTC)',
                'listed_by': 1,
                'location': 'Singapore',
                'no_of_pax': 3,
                'role_id': 1,
                'role_name': 'Software Engineer',
                'role_description': 'Develop software',
                'skills_name': []
            }
        }

        response = self.client.put(
            '/roles/update', data=json.dumps(request_body), content_type='application/json')
        
        self.assertEqual(response.json['data'], {
                        "department": "IT",
                        "expiry_date": 1701388800,
                        "listed_by": 1,
                        "location": "Singapore",
                        "no_of_pax": 3,
                        "role_description": "Develop software",
                        "role_id": 1,
                        "role_name": "Software Engineer"
                    }
            )

    def test_update_role_error(self):
        request_body = {
            'params': {
                'department': 'IT',
                'expiry_timestamp': 'Mon Dec 12 2023 00:00:00 GMT+0000 (UTC)',
                'listed_by': 1,
                'location': 'Singapore',
                'no_of_pax': 3,
                'role_id': 1,
                'role_name': 'Software Engineer',
                'role_description': 'Develop software',
                'skills_name': []
            }
        }
        with self.assertRaises(Exception):
            self.client.put(
                '/roles/update', data=json.dumps(request_body), content_type='application/json')

class TestGetRoleApplicant(TestApp):
    # Testing /role_application/get_all/<int:role_id>
    def test_get_all_role_applicant(self):
        staff1 = Staff(staff_id=1, first_name="John", last_name="Tan",
                       email="JohnTan@gmail.com", department="IT", current_role="Software Engineer",
                       access_rights=1)
        staff2 = Staff(staff_id=2, first_name="Tony", last_name="Lim",
                       email="TonyLin@gmail.com", department="OT", current_role="Ops Engineer",
                       access_rights=2)
        db.session.add(staff1)
        db.session.add(staff2)
        db.session.commit()

        role_applicant1 = Role_Applicant(
            role_id=1, staff_id=1, comments="test", creation_timestamp=1695174041)
        role_applicant2 = Role_Applicant(
            role_id=1, staff_id=2, comments="test", creation_timestamp=1695174041)
        db.session.add(role_applicant1)
        db.session.add(role_applicant2)
        db.session.commit()

        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        response = self.client.get(
            '/role_application/get_all/1', content_type='application/json')

        self.assertEqual(response.json["data"], {
            'role_data': {
                "count_applicant": 2,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                "role_id": 1,
                "role_name": "Software Engineer",
                "skills_required": [],
            },
            'staff_data': [
                {
                    "access_rights": 1,
                    "current_role": "Software Engineer",
                    "department": "IT",
                    "email": "JohnTan@gmail.com",
                    "first_name": "John",
                    "last_name": "Tan",
                    "staff_id": 1,
                    "staff_skills": [

                    ]
                },
                {
                    "access_rights": 2,
                    "current_role": "Ops Engineer",
                    "department": "OT",
                    "email": "TonyLin@gmail.com",
                    "first_name": "Tony",
                    "last_name": "Lim",
                    "staff_id": 2,
                    "staff_skills": [

                    ]
                },
            ]
        })

    def test_get_all_role_applicant_empty(self):
        role1 = Role(role_name="Software Engineer", role_description="Develop software", listed_by=1,
                     no_of_pax=3, department="IT", location="Singapore", expiry_timestamp=1701388800)
        role2 = Role(role_name="Ops Engineer", role_description="Maintain servers", listed_by=2,
                     no_of_pax=2, department="OT", location="Singapore", expiry_timestamp=1701388800)
        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()
        response = self.client.get(
            '/role_application/get_all/1', content_type='application/json')

        self.assertEqual(response.json["data"], {
            'role_data': {
                "count_applicant": 0,
                "days_left": days_left_from_unix(1701388800),
                "department": "IT",
                "expiry_date": "01-Dec-2023",
                "listed_by": 1,
                "location": "Singapore",
                "no_of_pax": 3,
                "role_description": "Develop software",
                "role_id": 1,
                "role_name": "Software Engineer",
                "skills_required": [],
            },
            'staff_data': []
        })

if __name__ == '__main__':
    unittest.main()
