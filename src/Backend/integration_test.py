import flask_testing
import unittest
import json
from app import app, db, Access_Rights, Staff, Role, Skill, Role_Skill, Staff_Skill, Role_Applicant


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


class TestGetAllStaff(TestApp):
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

class TestGetSpecificStaff(TestApp):
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

if __name__ == '__main__':
    unittest.main()
