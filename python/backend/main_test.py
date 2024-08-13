import unittest
from main import create_app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def tearDown(self):
        # Here, you can add code to be executed after each test
        pass

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
