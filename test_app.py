import unittest

from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_sum(self):
        response = self.client.post('/sum', json={'num1': 2, 'num2': 3})
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['result'], 5)


if __name__ == '__main__':
    unittest.main()
