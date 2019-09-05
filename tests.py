from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask tests"""

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage page (also the login page)"""

        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1>Login</h1>', result.data)

    def test_register(self):
        """Test register page"""

        result = self.client.get('/register')
        self.assertIn(b'<h1>Register</h1>', result.data)


class FlaskTestDataBase(TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        """Stuff to do before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Stuff to do after every test"""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_registered_user(self):
        """Test registered user in login page"""

        result = self.client.post('/login',
                                  data={'username': 'mlion', 'password': '111111'},
                                  follow_redirects=True)
        self.assertIn(b"Welcome to Instapic", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged into session"""

    def setUp(self):
        """stuff to do before every test"""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'abc'
        self.client = app.test_client()
        connect_to_db(app)

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

    def test_photos_list(self):
        """Test photo list page"""

        result = self.client.get('/photos')
        self.assertIn(b'Logout', result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user logged into session"""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_upload_page(self):
        """Test that user can't see upload page when logged out."""

        result = self.client.get("/upload", follow_redirects=True)
        self.assertNotIn(b"Welcome to Instapic", result.data)
        self.assertIn(b"Login", result.data)


################################################################################


if __name__ == "__main__":
    import unittest

    unittest.main()

