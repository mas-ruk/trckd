from app import create_app, db
import unittest
from selenium import webdriver
import multiprocessing
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

localHost = "http://localhost:5000/"

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.testApp = create_app('test')
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        new_user = User(email="test@gmail.com", username="test_user", password=generate_password_hash("password"))
        db.session.add(new_user)
        new_user = User(email="test2@gmail.com", username="test_user2", password=generate_password_hash("password2"))
        db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User.query.filter_by(email="test@gmail.com").first()
        self.assertTrue(check_password_hash(user.password, "password"))
        self.assertFalse(check_password_hash(user.password, "password2"))

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.testApp = create_app('test')
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        new_user = User(email="test@gmail.com", username="test_user", password=generate_password_hash("password"))
        db.session.add(new_user)
        new_user = User(email="test2@gmail.com", username="test_user2", password=generate_password_hash("password2"))
        db.session.add(new_user)
        db.session.commit()

        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_form(self):
        self.driver.get(localHost)
        


