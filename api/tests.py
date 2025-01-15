import time

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
    fixtures=['api/fixtures/test_data.json']
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver1 = WebDriver()
        cls.driver1.implicitly_wait(10)
        
        cls.driver2 = WebDriver()
        cls.driver2.implicitly_wait(10)
        

    @classmethod
    def tearDownClass(cls):
        cls.driver1.quit()
        cls.driver2.quit()
        super().tearDownClass()


    #manually run test, python manage.py api.tests.MySeleniumTests.test_signup``
    def _signup(self, firstname, lastname, email, DOB, password, driver):
        # driver.get("http://localhost:8000")

        #accessing the sign up page
        signup = driver.find_element(By.LINK_TEXT, "Sign Up")
        signup.click()

        firstname_input = driver.find_element(By.ID, "firstNameInput")
        lastname_input = driver.find_element(By.ID, "lastNameInput")
        email_input = driver.find_element(By.ID, "emailInput")
        DOB_input = driver.find_element(By.ID, "dobInput")
        password_input = driver.find_element(By.ID, "passwordInput")
        confirmPassword_input = driver.find_element(By.ID, "passwordInput2")
        
        firstname_input.send_keys(firstname)
        lastname_input.send_keys(lastname)
        email_input.send_keys(email)
        DOB_input.send_keys(DOB)
        password_input.send_keys(password)
        confirmPassword_input.send_keys(password)
        confirmPassword_input.submit()
        time.sleep(4)
        

    #manually run test, python manage.py api.tests.MySeleniumTests.test_login
    def _login(self, username, password, driver):
        # driver.get(f"{self.live_server_url}")

        #accessing the login page
        login = driver.find_element(By.LINK_TEXT, "Login")
        login.click()

        email_input = driver.find_element(By.ID, "usernameInput")
        password_input = driver.find_element(By.ID,"passwordInput")
       
        email_input.send_keys(username)
        password_input.send_keys(password)
        password_input.submit()
        time.sleep(4)


    def _logout(self, driver):
        logout = driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[5]")
        logout.click()


    #manually run test, python manage.py api.tests.MySeleniumTests.test_editing_info
    def _editing_info(self, first, last, email, DOB, hobby, driver):
        # self.test_login()

        firstnameChange = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[1]/input")
        lastnameChange = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[2]/input")
        emailChange = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[3]/input")
        DOBChange = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[4]/input")
        HobbyTest = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div")
        submit = driver.find_element(By.CLASS_NAME, "btn-primary")

        firstnameChange.clear()
        firstnameChange.send_keys(first)
        lastnameChange.clear()
        lastnameChange.send_keys(last)
        emailChange.clear()
        emailChange.send_keys(email)
        DOBChange.clear()
        DOBChange.send_keys(DOB)
        HobbyTest.send_keys(f"{hobby}\ue007")
        HobbyDescription = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/input[2]")
        HobbyDescription.send_keys(f"This is the activity of {hobby}")
        hobbySubmit = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/button")
        time.sleep(2)
        hobbySubmit.click()


        time.sleep(2)
        submit.click()

        #change password is not working yet, testing will be implemented when fixed 

    #manually run test, python manage.py api.tests.MySeleniumTests.test_filtering_age
    def _filtering_age(self, driver):
        search = driver.find_element(By.LINK_TEXT, "Search")
        search.click()

        ageSliderLower = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[1]")
        ageSliderUpper = driver.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[2]")

        for i in range(8):
            ageSliderLower.send_keys(Keys.RIGHT)
        
        for i in range(30):
            ageSliderUpper.send_keys(Keys.LEFT)



    #manually run test, python manage.py api.tests.MySeleniumTests.test_send_friend_request
    def _send_friend_request(self, driver):
        sendRequest = driver.find_element(By.CLASS_NAME, "btn-primary")
        sendRequest.click()



    #manually run test, python manage.py api.tests.MySeleniumTests.test_receive_friend_request
    def _receive_friend_request(self, driver):

        sendRequest = driver.find_element(By.CLASS_NAME, "btn-success")
        sendRequest.click()


    def _show_friends(self, driver):
        currentFriends = driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[2]/div/button")
        currentFriends.click()


    
    def test_liveserver(self):
        self.driver1.get(f"{self.live_server_url}")
        time.sleep(3)

        #Creating an account
        self._signup("James", "Smith", "Jamessmith@test.com", "10-09-1987", "seleniumPassword", self.driver1)
        time.sleep(3)


        #Logging out of the account just created
        self._logout(self.driver1)
        time.sleep(3)


        #Logging back in to the account just created
        self._login("Jamessmith@test.com", "seleniumPassword", self.driver1)
        time.sleep(2)


        #Changing the users details 
        self._editing_info("Josh", "Brown", "ChangedEmail@test.com", "17-02-1984", "Running", self.driver1)
        time.sleep(2)


        #search and filetering by age
        self._filtering_age(self.driver1)
        time.sleep(2)

        #Sending a friend request
        self._send_friend_request(self.driver1)
        time.sleep(2)


        #Creating second browser
        self.driver2.get(f"{self.live_server_url}")
        time.sleep(4)

        #Logging in to second account
        self._login("Tomstar@testmail.com", "passwordTesting", self.driver2)

        #accessing search 
        friendRequests = self.driver2.find_element(By.LINK_TEXT, "Search")
        friendRequests.click()
        time.sleep(2)
                
        #accepting friend request
        self._receive_friend_request(self.driver2)
        time.sleep(2)

        #Showing current friends
        self._show_friends(self.driver1)
        self._show_friends(self.driver2)
        time.sleep(5)