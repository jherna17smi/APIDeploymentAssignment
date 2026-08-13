import unittest

from app import app
from app.models import db


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.drop_all()
        self.auth_headers = {"X-API-Key": app.config["API_KEY"]}

    def _seed_dependencies(self):
        customer = self.client.post('/customers/', json={'name': 'Luis', 'phone': '555-0101'}).get_json()
        mechanic = self.client.post('/mechanics/', json={'name': 'Ana', 'specialty': 'Engine'}).get_json()
        return customer['id'], mechanic['id']

    def test_list_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_service_ticket(self):
        customer_id, mechanic_id = self._seed_dependencies()
        response = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['issue'], 'Brake noise')

    def test_create_service_ticket_invalid_payload(self):
        response = self.client.post('/service-tickets/', json={'issue': 'Brake noise'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Validation failed')

    def test_create_service_ticket_unknown_dependencies(self):
        response = self.client.post('/service-tickets/', json={'customer_id': 55, 'mechanic_id': 44, 'issue': 'Brake noise'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Validation failed')

    def test_get_service_ticket_by_id(self):
        customer_id, mechanic_id = self._seed_dependencies()
        created = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'}).get_json()
        response = self.client.get(f"/service-tickets/{created['id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], created['id'])

    def test_get_service_ticket_not_found(self):
        response = self.client.get('/service-tickets/999')
        self.assertEqual(response.status_code, 404)

    def test_update_service_ticket_requires_auth(self):
        customer_id, mechanic_id = self._seed_dependencies()
        created = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'}).get_json()
        response = self.client.put(
            f"/service-tickets/{created['id']}",
            json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Updated issue', 'status': 'in_progress'},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_service_ticket(self):
        customer_id, mechanic_id = self._seed_dependencies()
        created = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'}).get_json()
        response = self.client.put(
            f"/service-tickets/{created['id']}",
            json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Updated issue', 'status': 'in_progress'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'in_progress')

    def test_patch_service_ticket(self):
        customer_id, mechanic_id = self._seed_dependencies()
        created = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'}).get_json()
        response = self.client.patch(
            f"/service-tickets/{created['id']}",
            json={'status': 'closed'},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['status'], 'closed')

    def test_delete_service_ticket(self):
        customer_id, mechanic_id = self._seed_dependencies()
        created = self.client.post('/service-tickets/', json={'customer_id': customer_id, 'mechanic_id': mechanic_id, 'issue': 'Brake noise'}).get_json()
        response = self.client.delete(f"/service-tickets/{created['id']}", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Service ticket deleted')


if __name__ == '__main__':
    unittest.main()
