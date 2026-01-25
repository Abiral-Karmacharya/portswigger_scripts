from file_upload_labs.auto import FileUpload
from lfi_labs.auto import LocalFile
from sqli_labs.auto import Sqli

if __name__ == "__main__":
    url = input("Enter the link to exploit: ")
    vulnerabilities = [FileUpload, LocalFile, Sqli]
    for vulnerability in vulnerabilities:
        if vulnerability(url).main():
            break
        else: 
            continue
    
