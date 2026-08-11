import unittest

from app import app


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)

    def test_create_customer(self):
        response = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Luis')


if __name__ == '__main__':
    unittest.main()
