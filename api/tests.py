import time

from django.test import TestCase
import requests, names, random

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
            'Authorization': 'Token 6c8fa3e3172169d2b7dbd27d299bc305575c20a7',
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

def create_account():
    for i in range(15):
        cookies = {
            'csrftoken': 'CGCHmVLRRBLjUcaaTzaNjqrkTWLL3Wp7',
        }

        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = first_name.lower() + last_name.lower() + str(random.randint(1, 1000)) + '@gmail.com'
        date_of_birth = f'{random.randint(1990, 2000)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}'
        list_hobbies = [
                {
                    'id': 1,
                    'name': 'Writing',
                },
                {
                    'id': 2,
                    'name': 'Coding',
                },
                {
                    'id': 3,
                    'name': 'Swimming',
                },
                {
                    'id': 4,
                    'name': 'Running',
                },
                {
                    'id': 5,
                    'name': 'Cycling',
                },
                {
                    'id': 6,
                    'name': 'Walking',
                },
                {
                    'id': 7,
                    'name': 'Playing',
                },
                {
                    'id': 8,
                    'name': 'Singing',
                },
                {
                    'id': 9,
                    'name': 'Dancing',
                }
            ]

        selected_hobbies = random.sample(list_hobbies, random.randint(1, 5))

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            # 'Cookie': 'csrftoken=CGCHmVLRRBLjUcaaTzaNjqrkTWLL3Wp7',
            'Origin': 'http://127.0.0.1:8000',
            'Pragma': 'no-cache',
            'Referer': 'http://127.0.0.1:8000/Signup',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-CSRFToken': 'gUUggQl8MwLLbKJo37TXXWhf1Mer5GTfIqmNsBWPtXmUVMJoMwTA6cypKyP2Ys8c',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        json_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'date_of_birth': date_of_birth,
            'password': 'Abcd2003!',
            'password1': 'Abcd2003!',
            'password2': 'Abcd2003!',
            'hobbies': selected_hobbies,
        }

        response = requests.post('http://127.0.0.1:8000/api/register/', cookies=cookies, headers=headers, json=json_data)
        print(response.text, email)

def seach_users():
    cookies = {
        'csrftoken': 'CGCHmVLRRBLjUcaaTzaNjqrkTWLL3Wp7',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi-VN,vi;q=0.9',
        'Authorization': 'Token ec5c4108747524106f685776f68820492147623b',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': 'csrftoken=CGCHmVLRRBLjUcaaTzaNjqrkTWLL3Wp7',
        'Pragma': 'no-cache',
        'Referer': 'http://127.0.0.1:8000/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'search': '',
        'l_age': '12',
        'u_age': '60',
        'page': '2',
    }

    response = requests.get('http://127.0.0.1:8000/api/users/', params=params, cookies=cookies, headers=headers)
    print(response.text)

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


    # Performs the sign up process
    def _signup(self, firstname, lastname, email, DOB, password, driver):

        # Accessing the sign up page
        signup = driver.find_element(By.LINK_TEXT, "Sign Up")
        signup.click()

        firstname_input = driver.find_element(By.ID, "id_first_name")
        lastname_input = driver.find_element(By.ID, "id_last_name")
        email_input = driver.find_element(By.ID, "id_email")
        DOB_input = driver.find_element(By.ID, "id_date_of_birth")
        password_input = driver.find_element(By.ID, "id_password1")
        confirmPassword_input = driver.find_element(By.ID, "id_password2")
        
        firstname_input.send_keys(firstname)
        time.sleep(0.5)
        lastname_input.send_keys(lastname)
        time.sleep(0.5)
        email_input.send_keys(email)
        time.sleep(0.5)
        DOB_input.send_keys(DOB)
        time.sleep(0.5)
        password_input.send_keys(password)  
        time.sleep(0.5)
        confirmPassword_input.send_keys(password)
        time.sleep(0.5)
        confirmPassword_input.submit()
        


    # Performs the login process
    def _login(self, username, password, driver):

        #accessing the login page
        login = driver.find_element(By.LINK_TEXT, "Login")
        login.click()
        time.sleep(1)

        email_input = driver.find_element(By.ID, "id_username")
        password_input = driver.find_element(By.ID,"id_password")
       
        email_input.send_keys(username)
        time.sleep(0.5)
        password_input.send_keys(password)
        time.sleep(0.5)
        password_input.submit()

    # Performs the logout process
    def _logout(self, driver):
        logout = driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[5]")
        logout.click()


    # Performs the editing of user information
    def _editing_info(self, first, last, email, DOB, hobby, driver):

        firstnameChange = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[2]/input")
        lastnameChange = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[3]/input")
        emailChange = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[4]/input")
        DOBChange = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[5]/input")
        HobbyTest = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[6]/div")
        submit = driver.find_element(By.CLASS_NAME, "btn-primary")

        firstnameChange.clear()
        firstnameChange.send_keys(first)
        time.sleep(0.5)
        lastnameChange.clear()
        lastnameChange.send_keys(last)
        time.sleep(0.5)
        emailChange.clear()
        emailChange.send_keys(email)
        time.sleep(0.5)
        DOBChange.clear()
        DOBChange.send_keys(DOB)
        time.sleep(0.5)
        HobbyTest.send_keys(f"{hobby}\ue007")
        time.sleep(0.5)
        HobbyDescription = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[6]/div[2]/input[2]")
        HobbyDescription.send_keys(f"This is the activity of {hobby}")
        time.sleep(0.5)
        hobbySubmit = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div[6]/div[2]/button")
        time.sleep(2)
        hobbySubmit.click()


        time.sleep(2)
        submit.click()
 

    # Performs the changing of password
    def _changing_password(self, oldPass, newPass, driver):
        changePassword = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[2]/button")
        changePassword.click()
        time.sleep(1)

        currentPassword = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[3]/div/div/div[2]/div[1]/input")
        newPassword = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[3]/div/div/div[2]/div[2]/input")
        confirmPassword = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[3]/div/div/div[2]/div[3]/input")
        submit = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[3]/div/div/div[3]/button[1]")

        currentPassword.send_keys(oldPass)
        time.sleep(0.5)
        newPassword.send_keys(newPass)
        time.sleep(0.5)
        confirmPassword.send_keys(newPass)
        time.sleep(0.5)
        submit.click()
        time.sleep(2)


    # Performs the filtering of users by age
    def _filtering_age(self, driver):
        search = driver.find_element(By.LINK_TEXT, "Search")
        search.click()
        time.sleep(1)

        ageSliderLower = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div/input[1]")
        ageSliderUpper = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div/div/input[2]")

        for i in range(8):
            ageSliderLower.send_keys(Keys.RIGHT)
        
        for i in range(30):
            ageSliderUpper.send_keys(Keys.LEFT)



    # Performs the sending of a friend request
    def _send_friend_request(self, driver):
        sendRequest = driver.find_element(By.CLASS_NAME, "btn-primary")
        sendRequest.click()

   
    # Performs the receiving of a friend request
    def _receive_friend_request(self, driver):
        requests = driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[1]/div/button")
        requests.click()
        time.sleep(1)

        receiveRequest = driver.find_element(By.CLASS_NAME, "btn-success")
        receiveRequest.click()
        time.sleep(1)


    # Performs the showing of current friends
    def _show_friends(self, driver):
        currentFriends = driver.find_element(By.XPATH, "/html/body/div/main/div/div[1]/nav/div/div/ul/li[2]/div/button")
        currentFriends.click()


    # Performs the live testing of the application using selenium
    def test_liveserver(self):
        self.driver1.get(f"{self.live_server_url}")
        time.sleep(2)

        # Creating an account
        self._signup("James", "Smith", "Jamessmith@test.com", "10-09-1987", "seleniumPassword", self.driver1)
        time.sleep(2)

        # Changing the user's details 
        self.driver1.find_element(By.LINK_TEXT, "Profile Page").click()
        self._editing_info("Josh", "Brown", "ChangedEmail@test.com", "17-02-1984", "Running", self.driver1)
        time.sleep(2)

        # Changing the password
        self._changing_password("seleniumPassword", "passwordSelenium", self.driver1)
        time.sleep(2)

        # Logging out of the account just created
        self._logout(self.driver1)
        time.sleep(2)

        # Logging back in to the account 
        self._login("ChangedEmail@test.com", "passwordSelenium", self.driver1)
        time.sleep(2)

        # Search and filetering by age
        self._filtering_age(self.driver1)
        time.sleep(2)

        # Sending a friend request
        self._send_friend_request(self.driver1)
        time.sleep(2)
        
        # Returning to the home page
        self.driver1.find_element(By.LINK_TEXT, "Home").click()

        # Creating second browser
        self.driver2.get(f"{self.live_server_url}")
        time.sleep(2)

        # Logging in to second account
        self._login("Tomstar@testmail.com", "passwordTesting", self.driver2)
        time.sleep(2)

        # Accepting friend request
        self._receive_friend_request(self.driver2)
        time.sleep(2)

        # Showing current friends
        self._show_friends(self.driver1)
        self._show_friends(self.driver2)
        time.sleep(3)