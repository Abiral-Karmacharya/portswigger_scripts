# Legal disclaimer and responsible use

**⚠️Important Disclaimer** \
This project is created solely for educational and ethical cybersecurity learning using PortSwigger’s intentionally vulnerable Web Security Academy labs.

**Do not use this tool on system other than:**

1. The portswigger authorized labs. i.e \*.web-security-academy.net
2. The system you own
3. The system you have permission on

**Unauthoized use of code may:**

1. Violet terms and conditions of portswigger
2. Computer misuse policy
3. Github's acceptable use policy

**You are responsible for how you use this code**:
This repository is published for learning, research, and demonstration purposes only.
I do not condone or support misuse, abuse, or unauthorized exploitation of real-world systems.

# 📌 About This Project

This script automates solving a small set of PortSwigger Web Security Academy labs that involve uploading files to achieve code execution.
These labs are intentionally insecure and provided specifically for practice.

**This repository does not:**

1. Target real-world applications
2. Encourage real-world exploitation
3. Provide attack payloads applicable outside the labs

**🛑 Usage Warning**\
Before running the script:

1. Verify that the target is a valid PortSwigger lab.
2. Do not run this against production systems or systems you do not own.
3. Respect all relevant laws and policies.

# How to use the app

My app is not that complicated. This app is just something I made out of interest. So just keep the points below in to consideration:

1. For file upload, you will need to make a .env file in /python_script directory. Then you have to add constants which are:
   1. FILE_TO_UPLOAD: The payload file. Just grab one from revshells.com ദ്ദി ˉ͈̀꒳ˉ͈́
   2. .HTACCESS: sounds tough but make a file named .htaccess then add 'AddType application/x-httpd-php .php2' in the file
   3. .MAGIC_BYTE_FILE: The payload file but just add GIF at the top of the file or GIF87a.
      side note: In all constant above you will have to add the location of the files are. For example, FILE_TO_UPLOAD should contains the location of payload file and same for others.
2. If you want to add proxies. You will need to add 'HTTP_PROXY' and your proxy ip:port for http and then 'HTTPS_PROXY' and your proxy ip:port for https.
3. ** If you don't like pain, then just use my config.py. Run that file and you are all set **

**Format of .env is:** \
export FILE_TO_UPLOAD="location_of_your_file" \
export HTACCESS_FILE="location_of_your_file" \
export MAGIC_BYTE_FILE="location_of_your_file" \
export PROXY_HTTP="ip:port" \
export PROXY_HTTPS="ip:port"
