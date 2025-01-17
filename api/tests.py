import time

from django.test import TestCase
import requests, names, random

#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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