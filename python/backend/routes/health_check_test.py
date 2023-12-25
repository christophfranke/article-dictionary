import unittest
from main import create_app  # Replace with the name of your module

class HealthCheckTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SECRET_KEY': 'test',
            'SESSION_COOKIE_SECURE': False
        }).test_client()

    def test_health_check(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

if __name__ == '__main__':
    unittest.main()
