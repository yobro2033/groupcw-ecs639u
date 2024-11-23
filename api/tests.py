from django.test import TestCase
import requests, time

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

create_hobbies()