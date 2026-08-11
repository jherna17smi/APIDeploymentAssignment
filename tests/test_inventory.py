import unittest

from app import app


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)

    def test_create_inventory_item(self):
        response = self.client.post('/inventory/', json={'name': 'Brake Pad', 'quantity': 10, 'price': 25.5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Brake Pad')


if __name__ == '__main__':
    unittest.main()
