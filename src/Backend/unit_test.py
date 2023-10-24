import unittest
from unittest.mock import patch
from app import days_left_from_unix, convert_to_unix_timestamp, convert_unix_to_custom_format, Access_Rights, Staff, Role, Skill, Role_Skill, Staff_Skill, Role_Applicant

class TestDaysLeftFromUnix(unittest.TestCase):

    @patch('time.time', return_value=1701388795)  # Thursday, November 30, 2023 11:59:55 PM
    def test_days_left_from_unix(self, _):

        # Define a sample unix timestamp
        unix_timestamp = 1701388800  # Friday, December 1, 2023 12:00:00 AM

        # Mock the current time to a known value
        result = days_left_from_unix(unix_timestamp)

        # Assert that the function returned the correct value
        self.assertEqual(result, 1)


class TestConvertToUnixTimestamp(unittest.TestCase):

    def test_convert_to_unix_timestamp(self):

        # Define a date object
        date_obj = "Fri Dec 01 2023 08:00:00 GMT+08:00 (UTC)"

        # Call the function
        result = convert_to_unix_timestamp(date_obj)

        # Assert that the function returned the correct value
        self.assertEqual(result, 1701417600)

class TestConvertUnixToCustomFormat(unittest.TestCase):

    def test_convert_unix_to_custom_format(self):

        # Define a sample unix timestamp
        unix_timestamp = 1701388800  # Friday, December 1, 2023 12:00:00 AM

        # Call the function
        result = convert_unix_to_custom_format(unix_timestamp)

        # Assert that the function returned the correct value
        self.assertEqual(result, '01-Dec-2023')
       
class TestAccessRights(unittest.TestCase):
        
        def setUp(self):
            self.acesss_one = Access_Rights(5, "Tester")
        
        def tearDown(self):
             self.access_one = None

        def test_json(self):
            self.assertDictEqual(self.acesss_one.json(), {"access_id": 5, "type": "Tester"})

class TestStaff(unittest.TestCase):
        
        def setUp(self):
            self.staff_tester = Staff(1, "John", "Doe", "IT", "Tester", "test@email.com", 3)

        def tearDown(self):
             self.staff_tester = None

        def test_json(self):
            self.assertDictEqual(self.staff_tester.json(), 
                {
                    "staff_id": 1, 
                    "first_name": 'John', 
                    "last_name": 'Doe',
                    "department": 'IT', 
                    "current_role": 'Tester', 
                    "email": 'test@email.com', 
                    "access_rights": 3
                })
            
class TestRole(unittest.TestCase):
    
        # Since database has no default value for role_id, we set it to None
        def setUp(self):
            self.role_tester = Role("Tester", "Test Software", 1, 1, "IT", "Singapore", 1701388800)

        def tearDown(self):
             self.role_tester = None

        def test_json(self):
            self.assertDictEqual(self.role_tester.json(), 
                {
                    "role_id": None,
                    "role_name": "Tester",
                    "role_description": "Test Software",
                    "listed_by": 1,
                    "no_of_pax": 1,
                    "department": "IT",
                    "location": "Singapore",
                    "expiry_date": 1701388800
                })
            
class TestSkill(unittest.TestCase):
    
        def setUp(self):
            self.skill_tester = Skill(1, 'Python', 'Programming Language')

        def tearDown(self):
             self.skill_tester = None

        def test_json(self):
            self.assertDictEqual(self.skill_tester.json(), 
                {
                    "skill_id": 1, 
                    "skill_name": 'Python', 
                    "skill_description": 'Programming Language'
                })
            
class TestRoleSkill(unittest.TestCase):
    
        def setUp(self):
            self.role_skill_tester = Role_Skill(1, 2)

        def tearDown(self):
             self.role_skill_tester = None

        def test_json(self):
            self.assertDictEqual(self.role_skill_tester.json(), 
                {
                    "role_id": 1, 
                    "skill_id": 2
                })
            
class TestStaffSkill(unittest.TestCase):
    
        def setUp(self):
            self.staff_skill_tester = Staff_Skill(1001, 2)

        def tearDown(self):
             self.staff_skill_tester = None

        def test_json(self):
            self.assertDictEqual(self.staff_skill_tester.json(), 
                {
                    "staff_id": 1001, 
                    "skill_id": 2
                })
            
class TestRoleApplicant(unittest.TestCase):
    
        def setUp(self):
            self.role_applicant_tester = Role_Applicant(1, 1001, 'Pending', 1701388800)

        def tearDown(self):
             self.role_applicant_tester = None

        def test_json(self):
            self.assertDictEqual(self.role_applicant_tester.json(), 
                {
                    "role_id": 1, 
                    "staff_id": 1001,
                    "comments": 'Pending',
                    "creation_timestamp": 1701388800,
                })


if __name__ == '__main__':
    unittest.main()