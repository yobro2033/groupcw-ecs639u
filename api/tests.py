from django.test import TestCase
import requests

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
# Create your tests here.

def create_hobbies():
    list_hobbies = [
        {'name': 'Writing', 'description': 'Writing books'},
        {'name': 'Coding', 'description': 'Coding books'},
        {'name': 'Swimming', 'description': 'Swimming books'},
        {'name': 'Running', 'description': 'Running books'},
        {'name': 'Cycling', 'description': 'Cycling books'},
        {'name': 'Walking', 'description': 'Walking books'},
        {'name': 'Playing', 'description': 'Playing books'},
        {'name': 'Singing', 'description': 'Singing books'},
        {'name': 'Dancing', 'description': 'Dancing books'},
    ]
    for each_hobby in list_hobbies:
        headers = {
            'Accept': '*/*',
            'Authorization': 'Token 34ae5acf5d284c562674d23c752bef2da229cb7a',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Connection': 'keep-alive',
            'Content-type': 'application/json',
            'Origin': 'http://localhost:5173',
            'Referer': 'http://localhost:5173/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        json_data = {
            'name': each_hobby['name'],
            'description': each_hobby['description']
        }

        response = requests.put('http://127.0.0.1:8000/api/hobbies/add/', headers=headers, json=json_data)
        print(response, response.text)

#create_hobbies()





class MySeleniumTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        
    
    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super().tearDownClass()


    #manually run test, python manage.py api.tests.MySeleniumTests.test_signup``
    def test_signup(self):
        self.selenium.get("http://localhost:8000")

        #accessing the sign up page
        signup = self.selenium.find_element(By.LINK_TEXT, "Sign Up")
        signup.click()

        firstname_input = self.selenium.find_element(By.ID, "firstNameInput")
        lastname_input = self.selenium.find_element(By.ID, "lastNameInput")
        email_input = self.selenium.find_element(By.ID, "emailInput")
        DOB_input = self.selenium.find_element(By.ID, "dobInput")
        password_input = self.selenium.find_element(By.ID, "passwordInput")
        confirmPassword_input = self.selenium.find_element(By.ID, "passwordInput2")
        
        firstname_input.send_keys("James")
        lastname_input.send_keys("Smith")
        email_input.send_keys("Jamessmith@test.com")
        DOB_input.send_keys("10-09-1987")
        password_input.send_keys("seleniumPassword")
        confirmPassword_input.send_keys("seleniumPassword")
        confirmPassword_input.submit()
   


    #manually run test, python manage.py api.tests.MySeleniumTests.test_login
    def test_login(self):
        self.selenium.get("http://localhost:8000")

        #accessing the login page
        login = self.selenium.find_element(By.LINK_TEXT, "Login")
        login.click()

        email_input = self.selenium.find_element(By.ID, "usernameInput")
        password_input = self.selenium.find_element(By.ID,"passwordInput")
       
        email_input.send_keys("Jamessmith@test.com")
        password_input.send_keys("seleniumPassword")
        password_input.submit()



    #manually run test, python manage.py api.tests.MySeleniumTests.test_editing_info
    def test_editing_info(self):
        self.test_login()

        firstnameChange = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[1]/input")
        lastnameChange = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[2]/input")
        emailChange = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[3]/input")
        DOBChange = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[4]/input")
        submit = self.selenium.find_element(By.CLASS_NAME, "btn-primary")

        firstnameChange.clear()
        firstnameChange.send_keys("newFirst")

        lastnameChange.clear()
        lastnameChange.send_keys("NewLast")

        emailChange.clear()
        emailChange.send_keys("ChangedEmail@test.com")

        DOBChange.clear()
        DOBChange.send_keys("17-02-2000")

        submit.click()

        #change password is not working yet, testing will be implemented when fixed 

    #manually run test, python manage.py api.tests.MySeleniumTests.test_filtering_age
    def test_filtering_age(self):
        self.test_login()

        search = self.selenium.find_element(By.LINK_TEXT, "Search")
        search.click()

        ageSliderLower = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[1]")
        ageSliderUpper = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[2]")

        for i in range(8):
            ageSliderLower.send_keys(Keys.RIGHT)
        
        for i in range(30):
            ageSliderUpper.send_keys(Keys.LEFT)



    #manually run test, python manage.py api.tests.MySeleniumTests.test_send_friend_request
    def test_send_friend_request(self):
        self.test_login()

        friendRequests = self.selenium.find_element(By.LINK_TEXT, "Search")
        friendRequests.click()

        sendRequest = self.selenium.find_element(By.CLASS_NAME, "btn-primary")
        sendRequest.click()



    #manually run test, python manage.py api.tests.MySeleniumTests.test_receive_friend_request
    def test_receive_friend_request(self):
        self.test_login()

        friendRequests = self.selenium.find_element(By.LINK_TEXT, "Search")
        friendRequests.click()

        sendRequest = self.selenium.find_element(By.CLASS_NAME, "btn-success")
        sendRequest.click()
