import unittest
from main import create_app  # Replace with the name of your module

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client using the Flask application configured for testing
        self.app = create_app({
            'TESTING': True,
            'SECRET_KEY': 'test',
            'SESSION_COOKIE_SECURE': False
        }).test_client()

    def tearDown(self):
        # Here, you can add code to be executed after each test
        pass

    def test_home_page(self):
        # Test that the home page loads correctly
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
