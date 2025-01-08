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



# def wait(f):

#     def slower_f(*args, **kwargs):
#         time.sleep(1)
#         f(*args, **kwargs)
#     return slower_f


class MySeleniumTests(StaticLiveServerTestCase):
    
    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     cls.selenium = WebDriver()
    #     cls.selenium.implicitly_wait(10)
        

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




    #manually run test, python manage.py api.tests.MySeleniumTests.test_login
    def login2(self):

        driver1 = WebDriver()
        driver1.implicitly_wait(10)
        driver1.get("http://localhost:8000")

        #accessing the login page
        login = driver1.find_element(By.LINK_TEXT, "Login")
        login.click()

        email_input = driver1.find_element(By.ID, "usernameInput")
        password_input = driver1.find_element(By.ID,"passwordInput")
       
        email_input.send_keys("Jamessmith@test.com")
        password_input.send_keys("seleniumPassword")
        password_input.submit()

        time.sleep(4)



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


    def test_receive_friend_request2(self):
        self.test_login()

        reqeustTab = self.selenium.find_element(By.XPATH, "html/body/div/main/div/div/nav/div/div/ul/li/div/button")
        reqeustTab.click()


    def test_hobbies(self):
        self.test_login()

        
        HobbyTest = self.selenium.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div")
        HobbyTest.send_keys("Test0\ue007")
    
        HobbyDescription = self.selenium.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/input[2]")
        HobbyDescription.send_keys("This is the description used in testing")

        hobbySubmit = self.selenium.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/button")
        hobbySubmit.click()
    

    def fullTesting1Driver(self):
        driver1 = WebDriver()
        driver1.implicitly_wait(10)
        driver1.get("http://localhost:8000")


        # #logging into browser 1
        # login = driver1.find_element(By.LINK_TEXT, "Login")
        # login.click()
        # email_input = driver1.find_element(By.ID, "usernameInput")
        # password_input = driver1.find_element(By.ID,"passwordInput")
        # email_input.send_keys("Jamessmith@test.com")
        # password_input.send_keys("seleniumPassword")
        # time.sleep(2)
        # password_input.submit()
        # time.sleep(2)


        #signing up - increase the number by 1 when testing   
        signup = driver1.find_element(By.LINK_TEXT, "Sign Up")
        signup.click()

        firstname_input = driver1.find_element(By.ID, "firstNameInput")
        lastname_input = driver1.find_element(By.ID, "lastNameInput")
        email_input = driver1.find_element(By.ID, "emailInput")
        DOB_input = driver1.find_element(By.ID, "dobInput")
        password_input = driver1.find_element(By.ID, "passwordInput")
        confirmPassword_input = driver1.find_element(By.ID, "passwordInput2")
        
        firstname_input.send_keys("Test")
        lastname_input.send_keys("version3")
        email_input.send_keys("testversion3@test.com")
        DOB_input.send_keys("10-09-1987")
        password_input.send_keys("seleniumPassword")
        confirmPassword_input.send_keys("seleniumPassword")
        confirmPassword_input.submit()
        

        #Changing the users details - increase number by 1 when testing 
        firstnameChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[1]/input")
        lastnameChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[2]/input")
        emailChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[3]/input")
        DOBChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[4]/input")
        HobbyTest = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div")
        submit = driver1.find_element(By.CLASS_NAME, "btn-primary")

        firstnameChange.clear()
        firstnameChange.send_keys("Changed")
        lastnameChange.clear()
        lastnameChange.send_keys("V3")
        emailChange.clear()
        emailChange.send_keys("ChangedV3@test.com")
        DOBChange.clear()
        DOBChange.send_keys("17-02-1984")
        HobbyTest.send_keys("testHobby3\ue007")
        HobbyDescription = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/input[2]")
        HobbyDescription.send_keys("This is the description used in testing")
        hobbySubmit = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/button")
        time.sleep(2)
        hobbySubmit.click()

        time.sleep(2)
        submit.click()
        time.sleep(2)


        #search and filetering by age
        search = driver1.find_element(By.LINK_TEXT, "Search")
        search.click()
        ageSliderLower = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[1]")
        ageSliderUpper = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[2]")
        for i in range(8):
            ageSliderLower.send_keys(Keys.RIGHT)
        for i in range(30):
            ageSliderUpper.send_keys(Keys.LEFT)
        time.sleep(2)


        #Sending a friend request
        sendRequest = driver1.find_element(By.CLASS_NAME, "btn-primary")
        sendRequest.click()
        time.sleep(2)


        #Logging out 
        logout = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[5]")
        logout.click()
        time.sleep(2)


        #Logging in to second account
        login = driver1.find_element(By.LINK_TEXT, "Login")
        login.click()
        email_input = driver1.find_element(By.ID, "usernameInput")
        password_input = driver1.find_element(By.ID,"passwordInput")
        email_input.send_keys("Testing2@test.com")
        password_input.send_keys("seleniumPassword")
        time.sleep(2)
        password_input.submit()
        time.sleep(2)


        #Accepting friend request
        friendRequests = driver1.find_element(By.LINK_TEXT, "Search")
        friendRequests.click()
        time.sleep(2)
        recievedRequest = driver1.find_element(By.CLASS_NAME, "btn-success")
        recievedRequest.click()
        time.sleep(2)

        
        #Show current friends
        currentFriends = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[2]/div/button")
        currentFriends.click()
        time.sleep(5)
   


    def fullTesting2Drivers(self):
        driver1 = WebDriver()
        driver1.implicitly_wait(10)
        driver1.get("http://localhost:8000")

        # #logging into browser 1
        # login = driver1.find_element(By.LINK_TEXT, "Login")
        # login.click()
        # email_input = driver1.find_element(By.ID, "usernameInput")
        # password_input = driver1.find_element(By.ID,"passwordInput")
        # email_input.send_keys("Jamessmith@test.com")
        # password_input.send_keys("seleniumPassword")
        # time.sleep(2)
        # password_input.submit()
        # time.sleep(2)


        #signing up - increase the number by 1 when testing   
        signup = driver1.find_element(By.LINK_TEXT, "Sign Up")
        signup.click()

        firstname_input = driver1.find_element(By.ID, "firstNameInput")
        lastname_input = driver1.find_element(By.ID, "lastNameInput")
        email_input = driver1.find_element(By.ID, "emailInput")
        DOB_input = driver1.find_element(By.ID, "dobInput")
        password_input = driver1.find_element(By.ID, "passwordInput")
        confirmPassword_input = driver1.find_element(By.ID, "passwordInput2")
        
        firstname_input.send_keys("Test")
        lastname_input.send_keys("version6")
        email_input.send_keys("testversion6@test.com")
        DOB_input.send_keys("10-09-1987")
        password_input.send_keys("seleniumPassword")
        confirmPassword_input.send_keys("seleniumPassword")
        confirmPassword_input.submit()
        

        #Changing the users details - increase number by 1 when testing 
        firstnameChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[1]/input")
        lastnameChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[2]/input")
        emailChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[3]/input")
        DOBChange = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/div[4]/input")
        HobbyTest = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div")
        submit = driver1.find_element(By.CLASS_NAME, "btn-primary")

        firstnameChange.clear()
        firstnameChange.send_keys("Changed")
        lastnameChange.clear()
        lastnameChange.send_keys("V6")
        emailChange.clear()
        emailChange.send_keys("ChangedV6@test.com")
        DOBChange.clear()
        DOBChange.send_keys("17-02-1984")
        HobbyTest.send_keys("testHobby6\ue007")
        HobbyDescription = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/input[2]")
        HobbyDescription.send_keys("This is the description used in testing")
        hobbySubmit = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/div[2]/button")
        time.sleep(2)
        hobbySubmit.click()

        time.sleep(2)
        submit.click()
        time.sleep(2)


        #search and filetering by age
        search = driver1.find_element(By.LINK_TEXT, "Search")
        search.click()
        ageSliderLower = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[1]")
        ageSliderUpper = driver1.find_element(By.XPATH, "html/body/div/main/div/div/div/div/input[2]")
        for i in range(8):
            ageSliderLower.send_keys(Keys.RIGHT)
        for i in range(30):
            ageSliderUpper.send_keys(Keys.LEFT)
        time.sleep(2)


        #Sending a friend request
        sendRequest = driver1.find_element(By.CLASS_NAME, "btn-primary")
        sendRequest.click()
        time.sleep(2)

 
        #Creating second browser
        driver2 = WebDriver()
        driver2.implicitly_wait(10)
        driver2.get("http://localhost:8000")


        #Logging in to second account
        login = driver2.find_element(By.LINK_TEXT, "Login")
        login.click()
        email_input = driver2.find_element(By.ID, "usernameInput")
        password_input = driver2.find_element(By.ID,"passwordInput")
        email_input.send_keys("Testing2@test.com")
        password_input.send_keys("seleniumPassword")
        time.sleep(2)
        password_input.submit()
        time.sleep(2)


        friendRequests = driver2.find_element(By.LINK_TEXT, "Search")
        friendRequests.click()
        time.sleep(2)
        recievedRequest = driver2.find_element(By.CLASS_NAME, "btn-success")
        recievedRequest.click()
        time.sleep(2)

        #Showing current friends
        currentFriends1 = driver1.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[2]/div/button")
        currentFriends1.click()
        currentFriends2 = driver2.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[2]/div/button")
        currentFriends2.click()
        time.sleep(5)