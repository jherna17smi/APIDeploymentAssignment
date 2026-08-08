import unittest

from app import app


class TestMember(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_member(self):
        member_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "DOB": "1900-01-01",
            "password": "123",
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "John Doe")

    def test_invalid_creation(self):
        member_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123",
        }

        response = self.client.post('/members/', json=member_payload)
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertEqual(payload['message'], 'Validation failed')
        self.assertEqual(payload['errors']['email'], ['Missing data for required field.'])
        self.assertEqual(payload['errors']['DOB'], ['Missing data for required field.'])


if __name__ == '__main__':
    unittest.main()
