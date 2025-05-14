# Import all packages you need here
from app import create_app, db
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

# Setting the web address of our app
localHost = "http://localhost:5000/"

# Define all the basic unit tests to be run
class BasicTests(unittest.TestCase):
    # Function for setting up the app and testing database - ADD YOUR TESTING DATA IN HERE
    def setUp(self):
        self.testApp = create_app('test')
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        with self.app_context:
            db.create_all()
        
        new_user = User(email="test@gmail.com", username="test_user", password=generate_password_hash("password"))
        db.session.add(new_user)
        # ADD OTHER TESTING DATA HERE
            # Create new data object (e.g. Card)
            # Add it to the session

        db.session.commit()

    # Function to remove testing data after the tests are complete
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test to ensure password hashing works
    def test_password_hashing(self):
        user = User.query.filter_by(email="test@gmail.com").first()
        self.assertTrue(check_password_hash(user.password, "password"))
        self.assertFalse(check_password_hash(user.password, "password2"))

    # ADD YOUR UNIT TESTS HERE - all test functions must be defined like 'test_...(self):'

# Define all the Selenium (system) tests to be run
class SeleniumTests(unittest.TestCase):
    # Function for setting up the app and testing database - ADD YOUR TESTING DATA IN HERE
    def setUp(self):
        self.testApp = create_app('test')
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        new_user = User(email="test@gmail.com", username="test_user", password=generate_password_hash("password"))
        db.session.add(new_user)
        # ADD OTHER TESTING DATA HERE
            # Create new data object (e.g. Card)
            # Add it to the session
        
        db.session.commit()

        def run_app(app):
            app.run(port=5000, debug=True, use_reloader=False)

        self.server_thread = Thread(target=run_app, args=(self.testApp,))
        self.server_thread.daemon = True
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new") # Comment this out if you want to see your webpage pop up and run the tests
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    # Function to remove testing data after the tests are complete
    def tearDown(self):
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test the login form works (users are logged in correctly)
    def test_login_form(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "login_link").click()

        self.driver.find_element(By.ID, "login_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("password")
        self.driver.find_element(By.ID, "submit").click()

        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element(By.ID, "current_username").text, "test_user")
    
    # Test the register form works (user logged in correctly, user added to the database)
    def test_register_form(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "register_email").send_keys("test2@gmail.com")
        self.driver.find_element(By.ID, "username").send_keys("test_user2")
        self.driver.find_element(By.ID, "register_password").send_keys("password2")
        self.driver.find_element(By.ID, "password_confirm").send_keys("password2")
        self.driver.find_element(By.ID, "register_submit").click()

        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element(By.ID, "current_username").text, "test_user2")
        user = User.query.filter_by(email="test2@gmail.com").first()
        self.assertIsNotNone(user)

    # ADD YOUR SELENIUM TESTS HERE - all test functions must be defined like 'test_...(self):'
        


