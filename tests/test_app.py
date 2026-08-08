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

    def test_sum_missing_value(self):
        response = self.client.post('/sum', json={'num1': 2})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['message'], 'Missing properties num1 and/or num2')


if __name__ == '__main__':
    unittest.main()
