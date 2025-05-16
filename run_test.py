# Import all packages you need here
from app import create_app, db
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            db.session.remove()
            db.drop_all()
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
        self.wait = WebDriverWait(self.driver, 10)

    # Function to remove testing data after the tests are complete
    def tearDown(self):
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test the login form works (users are logged in correctly)
    def test_login_form_success(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "login_link").click()

        self.driver.find_element(By.ID, "login_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("password")
        self.driver.find_element(By.ID, "submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "current_username")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element(By.ID, "current_username").text, "test_user")

    # Test the login form works (users cannot login with an unregistered email)
    def test_login_form_bad_email(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "login_link").click()

        self.driver.find_element(By.ID, "login_email").send_keys("wrongemail@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("123456")
        self.driver.find_element(By.ID, "submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_email_error")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/")
        self.assertEqual(self.driver.find_element(By.ID, "login_email_error").text, "[No user registered to that email address.]")

    # Test the login form works (users cannot login with an unregistered email)
    def test_login_form_bad_password(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "login_link").click()

        self.driver.find_element(By.ID, "login_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("123456")
        self.driver.find_element(By.ID, "submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "login_password_error")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/")
        self.assertEqual(self.driver.find_element(By.ID, "login_password_error").text, "[Incorrect password.]")
    
    # Test the register form works (user logged in correctly, user added to the database)
    def test_register_form_success(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "register_email").send_keys("test2@gmail.com")
        self.driver.find_element(By.ID, "username").send_keys("test_user2")
        self.driver.find_element(By.ID, "register_password").send_keys("password2")
        self.driver.find_element(By.ID, "password_confirm").send_keys("password2")
        self.driver.find_element(By.ID, "register_submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "current_username")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/home")
        self.assertEqual(self.driver.find_element(By.ID, "current_username").text, "test_user2")
        user = User.query.filter_by(email="test2@gmail.com").first()
        self.assertIsNotNone(user)

    # Test the register form works (user tries to register with taken email and username)
    def test_register_form_taken_email_and_username(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "register_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "username").send_keys("test_user")
        self.driver.find_element(By.ID, "register_password").send_keys("password2")
        self.driver.find_element(By.ID, "password_confirm").send_keys("password2")
        self.driver.find_element(By.ID, "register_submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "register_email_error")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/")
        self.assertEqual(self.driver.find_element(By.ID, "register_email_error").text, "[Email already in use. Choose a different email.]")
        self.assertEqual(self.driver.find_element(By.ID, "register_username_error").text, "[Username already in use. Choose a different username.]")
        users = User.query.all()
        self.assertEqual(len(users), 1)

    # Test the register form works (user tries to register with different passwords in the 'password' and 'confirm password' fields)
    def test_register_form_different_passwords(self):
        self.driver.get(localHost)
        self.driver.find_element(By.ID, "register_link").click()

        self.driver.find_element(By.ID, "register_email").send_keys("test2@gmail.com")
        self.driver.find_element(By.ID, "username").send_keys("test_user2")
        self.driver.find_element(By.ID, "register_password").send_keys("password2")
        self.driver.find_element(By.ID, "password_confirm").send_keys("password3")
        self.driver.find_element(By.ID, "register_submit").click()

        # Ensures all required page elements are loaded
        self.wait.until(EC.visibility_of_element_located((By.ID, "register_password_error")))

        self.assertEqual(self.driver.current_url, "http://localhost:5000/")
        self.assertEqual(self.driver.find_element(By.ID, "register_password_error").text, "[Passwords must match.]")
        users = User.query.all()
        self.assertEqual(len(users), 1)

    # ADD YOUR SELENIUM TESTS HERE - all test functions must be defined like 'test_...(self):'
    
    # Testing search bar and filter buttons respond
    def test_search_various_inputs(self):
        # travel to homepage
        self.driver.get(localHost)
        
        # log in to page using known credentials
        self.driver.find_element(By.ID, "login_link").click()
        self.driver.find_element(By.ID, "login_email").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "login_password").send_keys("password")
        self.driver.find_element(By.ID, "submit").click()

        # allow time for website to respond
        wait = WebDriverWait(self.driver, 10)

        # test normal search
        self.driver.get(localHost + "search")
        search_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "add-cards-search")))

        # test-case insensitivity
        search_input.clear()
        search_input.send_keys("liliana")
        search_input.send_keys(Keys.ENTER)
        cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card")))
        self.assertTrue(len(cards) > 0, "Expected cards for 'liliana' search")

        # test search with special characters
        search_input.clear()
        search_input.send_keys("!@#$%^&*()")
        search_input.send_keys(Keys.ENTER)

        try:
            error_msg = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p.text-danger")))
            self.assertTrue(error_msg.is_displayed())
            self.assertIn("Error loading cards", error_msg.text)
        except TimeoutException:
            # If error message not shown, check that no cards are present
            cards = self.driver.find_elements(By.CLASS_NAME, "card")
            self.assertEqual(len(cards), 0, "Expected no cards and no error message")

if __name__ == "__main__":
    unittest.main()