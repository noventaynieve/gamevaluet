import unittest
import json
from app import app, db
from models import GameVault

class TestGameVaultAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_api_get_gamevault(self):
        """Verifica que el endpoint GET devuelva una lista JSON válida en GameVault."""
        response = self.client.get('/api/gamevault')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_api_post_gamevault(self):
        """Verifica la inserción de registros a través del endpoint POST de la API."""
        payload = {
            "title": "Hades II",
            "category": "Roguelike",
            "price": 29.99
        }
        response = self.client.post(
            '/api/gamevault',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 201])
        
        item = GameVault.query.filter_by(title="Hades II").first()
        self.assertIsNotNone(item)

if __name__ == '__main__':
    unittest.main()
