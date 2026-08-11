import unittest

from app import app


class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_list_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)

    def test_create_service_ticket(self):
        response = self.client.post('/service-tickets/', json={'customer_id': 1, 'mechanic_id': 1, 'issue': 'Brake noise'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['issue'], 'Brake noise')


if __name__ == '__main__':
    unittest.main()
