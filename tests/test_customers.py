import unittest

from app import app
from app.models import db


class TestCustomers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        self.auth_headers = {"X-API-Key": app.config["API_KEY"]}

    def test_list_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_customer(self):
        response = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Luis')

    def test_create_customer_invalid_payload(self):
        response = self.client.post('/customers/', json={'name': 'Luis'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Validation failed')

    def test_get_customer_by_id(self):
        created = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        response = self.client.get(f"/customers/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['phone'], '555-0101')

    def test_get_customer_not_found(self):
        response = self.client.get('/customers/999')
        self.assertEqual(response.status_code, 404)

    def test_update_customer_requires_auth(self):
        created = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        response = self.client.put(f"/customers/{created['id']}", json={'name': 'Luis A', 'phone': '555-0102'})
        self.assertEqual(response.status_code, 401)

    def test_update_customer(self):
        created = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        response = self.client.put(
            f"/customers/{created['id']}",
            json={'name': 'Luis A', 'phone': '555-0102'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Luis A')

    def test_patch_customer(self):
        created = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        response = self.client.patch(
            f"/customers/{created['id']}",
            json={'phone': '555-9999'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['phone'], '555-9999')

    def test_delete_customer(self):
        created = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        response = self.client.delete(f"/customers/{created['id']}", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Customer deleted')


if __name__ == '__main__':
    unittest.main()
