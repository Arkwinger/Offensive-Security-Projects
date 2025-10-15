# UltraTech Walkthrough

<img width="579" height="571" alt="image" src="https://github.com/user-attachments/assets/38ff2086-c2a6-4c3c-80d4-6df7836deda7" />



## Enumeration

We used a staged Nmap approach: start with a fast, safe service discovery (-sC -sV) to learn which services are present and gather banners; then run a full-port SYN scan (-p- -sS) to discover any non-standard services; finally run targeted service/script scans against ports of interest to extract useful metadata (HTTP titles, SSL certs, SMB info, etc.). This ordering balances speed, noise, and information value.


<img width="1050" height="556" alt="nmap" src="https://github.com/user-attachments/assets/790cd51b-40b6-4f98-b0f9-80260a98cb40" />
_________________________________________________________________________________________________________________


For this box, this scan was able to asnwer the following questions:


### Which software is using the port 8081?

`Node.js`


### Which other non-standard port is used?

`31331`


### Which software using this port?

`Apache`


### Which GNU/Linux distribution seems to be used?

`Ubuntu`


### The software using the port 8081 is a REST api, how many of its routes are used by the web application?

`2`

______________________________________________________________________________________________________________

## Exploit

I began with standard reconnaissance against the host and discovered two web entry points: an Apache-served site on :31331 and a Node API on :8081. Directory enumeration with gobuster revealed a partner login page at /partners.html. The HTML for that page contained no server-side action attribute on the form; instead it referenced two JavaScript assets (js/app.min.js and js/api.js). That was a clear signal: the login flow and other logic were handled client-side, so the next step was to fetch and inspect those scripts.

Pulling js/api.js revealed a small API wrapper that called a simple “ping” endpoint. The code took user-supplied input (an ip or host parameter) and used it as the argument to a ping command on the server. In other words, the server was running something equivalent to system("ping " + user_input) rather than safely validating/whitelisting the input. This pattern is a classic command-injection anti-pattern: passing unsanitized input into a shell command.

To confirm this without being destructive I exercised low-impact probes. Submitting backtick-style payloads in the ip parameter produced immediate evidence of code execution. For example, issuing:

`http://10.201.123.134:8081/ping?ip=`ls``

This caused the server to attempt to resolve a host named after the output of ls, and the resulting page reflected that output (the web response included the filename utech.db.sqlite). From there I ran small, safe enumeration commands through the same vector: whoami, pwd, and ls -la. Each returned content that showed I could execute arbitrary commands in the context of the web process. The application therefore had an exploitable command injection vulnerability via the ping API.

Having confirmed code execution, I enumerated the application directory and discovered a SQLite database file utech.db.sqlite. Using command injection to read small chunks of the file, I extracted two MD5 password hashes contained in the database.

<img width="1049" height="521" alt="partners" src="https://github.com/user-attachments/assets/0885f8b3-f022-45ab-952c-aa851b1bd00c" />


<img width="1425" height="948" alt="login page" src="https://github.com/user-attachments/assets/4dd926b0-0a8b-4842-afbb-386fe20f6c9c" />

<img width="1416" height="1013" alt="pagesource" src="https://github.com/user-attachments/assets/ce4a0d9c-ca3e-4829-b668-9666c0da1a00" />

<img width="1421" height="878" alt="js" src="https://github.com/user-attachments/assets/80e71242-f8fc-4cce-a3bf-f6f7949cc859" />

<img width="1417" height="538" alt="ping" src="https://github.com/user-attachments/assets/7e9f4dc2-a0df-4467-9e1f-7311cdc2f6ce" />


###There is a database lying around, what is its filename?
`utech.db.sqlite`

<img width="1415" height="327" alt="cat" src="https://github.com/user-attachments/assets/dc7f3b52-b47e-42f8-83e1-89974a10235c" />

We find two password hashes: use 

https://hashes.com/en/decrypt/hash


### What is the first user's password hash?

`f357a0c52799563c7c7b76c1e7543a32`


### What is the password associated with this hash?

`n100906`


With valid credentials in hand I authenticated where appropriate and obtained a shell as r00t on the box. Local enumeration showed Docker was available and that a tiny bash image existed on the system. The presence of Docker and the ability to run containers allowed an escalation path even without sudo: I launched a container that bind-mounted the host filesystem and chrooted into it, for example:

`docker run -v /:/mnt --rm -it bash chroot /mnt sh`

From that chrooted root context I could access host files directly and read /root/.ssh/id_rsa. Copying that private key out of the host filesystem (securely) allowed me to authenticate as root where the key was authorized, completing host compromise.

The vulnerability chain is straightforward but severe: an unauthenticated or low-privileged web action allowed command injection; that led to disclosure of database-stored credentials and ultimately to host-level access via Docker/chroot. Confidential data (the SQLite DB, password hashes, and host private key) were exposed, and the service could be fully compromised.

<img width="1048" height="599" alt="image" src="https://github.com/user-attachments/assets/29ba0a0f-ec9c-4d41-9435-08f902fdb730" />


<img width="1571" height="589" alt="image" src="https://github.com/user-attachments/assets/bac2a799-b5d7-4543-9542-f83e656e61a6" />

### What are the first 9 characters of the root user's private SSH key?

`MIIEogIBA`

### Conclusion


This engagement demonstrates how a small client-side API call (the ping endpoint) can lead to full compromise when combined with unsafe server-side command execution. The exploitation path was: identify client-side logic → find server-side ping wrapper → confirm command injection → extract database → crack credentials → use Docker to chroot into host FS → obtain host id_rsa → authenticate as root. The fix is immediate: stop shelling out with untrusted input and follow least-privilege deployment and secrets management practices.



















