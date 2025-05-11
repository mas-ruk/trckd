from app import create_app, db
import unittest
from app.models import User

class BasicTests(unittest.TestCase):
    def SetUp(self):
        testApp = create_app('test')
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        # Add test data

    def TearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        return


