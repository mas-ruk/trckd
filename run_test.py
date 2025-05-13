from app import create_app, db
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
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
        db.session.commit()

        def run_app(app):
            app.run(port=5000)

        self.server_thread = Thread(target=run_app, args=(self.testApp,))
        self.server_thread.daemon = True
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_form(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "login_link").click()

        self.driver.find_element(By.ID, "login_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("password")
        self.driver.find_element(By.ID, "submit").click()

        self.assertEqual(self.driver.current_url, "http://localhost:5000/collection")
        # self.assertEqual(current_user.username, "test_user") Replace w/ check of sidebar username

    def test_register_form(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "register_email").send_keys("test2@gmail.com")
        self.driver.find_element(By.ID, "username").send_keys("test_user2")
        self.driver.find_element(By.ID, "register_password").send_keys("password2")
        self.driver.find_element(By.ID, "password_confirm").send_keys("password2")
        self.driver.find_element(By.ID, "register_submit").click()

        # self.assertEqual(self.driver.current_url, "http://localhost:5000/collection")
        # self.assertEqual(current_user.username, "test_user2") Replace w/ check of sidebar username
        # user = User.query.filter_by(email="test2@gmail.com").first()
        # self.assertIsNotNone(user)
        


