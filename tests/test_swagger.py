import unittest

from app import app


class TestSwaggerDocs(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_swagger_json_contains_routes(self):
        response = self.client.get('/swagger.json')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn('/sum', data['paths'])
        self.assertIn('/members/', data['paths'])
        self.assertIn('/mechanics/', data['paths'])
        self.assertIn('/mechanics/{mechanic_id}', data['paths'])
        self.assertIn('/customers/', data['paths'])
        self.assertIn('/customers/{customer_id}', data['paths'])
        self.assertIn('/service-tickets/', data['paths'])
        self.assertIn('/service-tickets/{ticket_id}', data['paths'])
        self.assertIn('/inventory/', data['paths'])
        self.assertIn('/inventory/{item_id}', data['paths'])
        self.assertIn('securityDefinitions', data)
        self.assertIn('ApiKeyAuth', data['securityDefinitions'])


if __name__ == '__main__':
    unittest.main()
