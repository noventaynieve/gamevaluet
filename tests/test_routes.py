import unittest
from app import app, db

class TestGameVaultRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False 
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_gamevault_home(self):
        """Verifica que la página principal de GameVault responda con éxito (200)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_gamevault_protected_route(self):
        """Verifica el acceso o redirección en las rutas de GameVault."""
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])

if __name__ == '__main__':
    unittest.main()
