Recon

```
gobuster dir -u http://10.201.87.191 -w /usr/share/wordlists/dirbuster/directory-list-1.0.txt 
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.201.87.191
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-1.0.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/phpmyadmin           (Status: 301) [Size: 319] [--> http://10.201.87.191/phpmyadmin/]
/flags                (Status: 301) [Size: 314] [--> http://10.201.87.191/flags/]
/css                  (Status: 301) [Size: 312] [--> http://10.201.87.191/css/]
/js                   (Status: 301) [Size: 311] [--> http://10.201.87.191/js/]
/vendor               (Status: 301) [Size: 315] [--> http://10.201.87.191/vendor/]
Progress: 141708 / 141709 (100.00%)
```

mail.log 

```
From: dev@injectics.thm
To: superadmin@injectics.thm
Subject: Update before holidays

Hey,

Before heading off on holidays, I wanted to update you on the latest changes to the website. I have implemented several enhancements and enabled a special service called Injectics. This service continuously monitors the database to ensure it remains in a stable state.

To add an extra layer of safety, I have configured the service to automatically insert default credentials into the `users` table if it is ever deleted or becomes corrupted. This ensures that we always have a way to access the system and perform necessary maintenance. I have scheduled the service to run every minute.

Here are the default credentials that will be added:

| Email                     | Password 	              |
|---------------------------|-------------------------|
| superadmin@injectics.thm  | superSecurePasswd101    |
| dev@injectics.thm         | devPasswd123            |

Please let me know if there are any further updates or changes needed.

Best regards,
Dev Team

dev@injectics.thm
```
