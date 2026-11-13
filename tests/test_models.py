import unittest
from app import app, db
from models import GameVault  # Clase modelo de tu proyecto

class TestGameVaultModels(unittest.TestCase):
    
    def setUp(self):
        """Configura una base de datos en memoria para pruebas aisladas."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Limpia la base de datos y el contexto al terminar cada prueba."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_gamevault_record(self):
        """Verifica que se pueda instanciar y guardar un registro en GameVault."""
        item = GameVault(title="Elden Ring", category="RPG", price=59.99)
        db.session.add(item)
        db.session.commit()
        
        saved_item = GameVault.query.filter_by(title="Elden Ring").first()
        self.assertIsNotNone(saved_item)
        self.assertEqual(saved_item.category, "RPG")
        self.assertEqual(saved_item.price, 59.99)

if __name__ == '__main__':
    unittest.main()
