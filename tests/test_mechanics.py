import unittest

from app import app


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)

    def test_create_mechanic(self):
        response = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Ana')


if __name__ == '__main__':
    unittest.main()
