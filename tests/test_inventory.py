import unittest

from app import app
from app.models import db


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        self.auth_headers = {"X-API-Key": app.config["API_KEY"]}

    def test_list_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_inventory_item(self):
        response = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Brake Pad')

    def test_create_inventory_item_invalid_payload(self):
        response = self.client.post('/inventory/', json={'name': 'Brake Pad'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Validation failed')

    def test_get_inventory_item_by_id(self):
        created = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5}).get_json()
        response = self.client.get(f"/inventory/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['quantity'], 10)

    def test_get_inventory_item_not_found(self):
        response = self.client.get('/inventory/999')
        self.assertEqual(response.status_code, 404)

    def test_update_inventory_item_requires_auth(self):
        created = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5}).get_json()
        response = self.client.put(
            f"/inventory/{created['id']}",
            json={'name': 'Rotor', 'quantity': 4, 'price': 80.0},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_inventory_item(self):
        created = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5}).get_json()
        response = self.client.put(
            f"/inventory/{created['id']}",
            json={'name': 'Rotor', 'quantity': 4, 'price': 80.0},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Rotor')

    def test_patch_inventory_item(self):
        created = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5}).get_json()
        response = self.client.patch(
            f"/inventory/{created['id']}",
            json={'quantity': 12},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['quantity'], 12)

    def test_delete_inventory_item(self):
        created = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5}).get_json()
        response = self.client.delete(f"/inventory/{created['id']}", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Inventory item deleted')


if __name__ == '__main__':
    unittest.main()
