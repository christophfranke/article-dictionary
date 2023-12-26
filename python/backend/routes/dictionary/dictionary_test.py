import unittest
import logging
import json
from main import create_app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.app = create_app({
            'TESTING': True,
            'SECRET_KEY': 'test',
            'SESSION_COOKIE_SECURE': False
        }).test_client()

    def login(self, email, password):
        response = self.app.post('/api/auth/login', json=dict(
            email=email,
            password=password
        ), follow_redirects=True)
        return response

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_list_and_detail(self):
        # Perform login
        login_response = self.login('test@test.de', 'test')
        self.assertEqual(login_response.status_code, 200)

        # Test that the home page loads correctly after login
        response = self.app.get('/api/dictionary/')
        self.assertEqual(response.status_code, 200)

        # Parse response data to JSON
        data = json.loads(response.data.decode('utf-8'))
        
        # Ensure data is a list and not empty
        self.assertTrue(isinstance(data, list) and len(data) > 0)

        # Extract 'original' from the first item in the list
        original = data[0]['original']

        # Make a new request using 'original'
        new_response = self.app.get(f'/api/dictionary/{original}')
        self.assertEqual(new_response.status_code, 200)

        # Perform logout
        self.logout()

if __name__ == '__main__':
    unittest.main()
