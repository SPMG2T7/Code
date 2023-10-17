import unittest
from unittest.mock import MagicMock
from datetime import datetime
from app import days_left_from_unix, convert_to_unix_timestamp, convert_unix_to_custom_format, Access_Rights, Staff, Role, Skill, Role_Skill, Staff_Skill, Role_Applicant

class TestDaysLeftFromUnix(unittest.TestCase):

    def test_days_left_from_unix(self):

        # Define a sample unix timestamp
        unix_timestamp = 1701388800  # Friday, December 1, 2023 12:00:00 AM

        # Mock the current time to a known value
        current_mock_time = MagicMock(return_value=1701388795)  # Thursday, November 30, 2023 11:59:55 PM
        with unittest.mock.patch('time.time', current_mock_time):
            result = days_left_from_unix(unix_timestamp)

        # Assert that the function returned the correct value
        self.assertEqual(result, 0)


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

        def test_json(self):
            self.assertDictEqual(self.acesss_one.json(), {"access_id": 5, "type": "Tester"})

class TestStaff(unittest.TestCase):
        
        def setUp(self):
            self.staff_tester = Staff(1, "John", "Doe", "IT", "Tester", "test@email.com", 3)

        def test_json(self):
            self.assertDictEqual(self.staff_tester.json(), 
                {"staff_id": 1, 
                "first_name": 'John', 
                "last_name": 'Doe',
                "department": 'IT', 
                "current_role": 'Tester', 
                "email": 'test@email.com', 
                "access_rights": 3
                })
            
class TestRole(unittest.TestCase):
        
        def setUp(self):
            self.role_tester = Role("Tester", "Test Software", 1, 1, "IT", "Singapore", 1701388800)

        # def test_json(self):
        #     self.assertDictEqual(self.role_tester.json(), 
        #         {"role_id": 1,
        #         "role_name": 'Tester',
        #         "role_description": 'Test Software',
        #         "listed_by": 1,
        #         "no_of_pax": 1,
        #         "department": "IT",
        #         "location": "Singapore",
        #         "expiry_date": 1701388800
        #         })

if __name__ == '__main__':
    unittest.main()