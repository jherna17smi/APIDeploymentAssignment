import unittest

from app import app
from app.models import db


class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        self.auth_headers = {"X-API-Key": app.config["API_KEY"]}

    def test_list_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_mechanic(self):
        response = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], 'Ana')

    def test_create_mechanic_invalid_payload(self):
        response = self.client.post('/mechanics/', json={'name': 'Ana'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Validation failed')

    def test_get_mechanic_by_id(self):
        created = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        response = self.client.get(f"/mechanics/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['specialty'], 'Engine')

    def test_get_mechanic_not_found(self):
        response = self.client.get('/mechanics/999')
        self.assertEqual(response.status_code, 404)

    def test_update_mechanic_requires_auth(self):
        created = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        response = self.client.put(f"/mechanics/{created['id']}", json={'name': 'Ana B', 'specialty': 'Transmission'})
        self.assertEqual(response.status_code, 401)

    def test_update_mechanic(self):
        created = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        response = self.client.put(
            f"/mechanics/{created['id']}",
            json={'name': 'Ana B', 'specialty': 'Transmission'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['specialty'], 'Transmission')

    def test_patch_mechanic(self):
        created = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        response = self.client.patch(
            f"/mechanics/{created['id']}",
            json={'specialty': 'Brakes'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['specialty'], 'Brakes')

    def test_delete_mechanic(self):
        created = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        response = self.client.delete(f"/mechanics/{created['id']}", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Mechanic deleted')


if __name__ == '__main__':
    unittest.main()
