# UltraTech Walkthrough (CTF)

---

## Enumeration

I began with a **staged Nmap approach**, starting with a fast and safe service discovery scan (`-sC -sV`) to identify active services and gather banners. I then ran a **full-port SYN scan** (`-p- -sS`) to detect any non-standard ports, followed by targeted script scans against interesting ports to extract metadata (HTTP titles, SSL certs, SMB info, etc.).  
This multi-stage method balanced **speed, noise, and information gain**.

<img width="1050" height="556" alt="nmap" src="https://github.com/user-attachments/assets/790cd51b-40b6-4f98-b0f9-80260a98cb40" />

---

### Questions Answered by Enumeration

| Question | Answer |
|-----------|--------|
| Which software is using port 8081? | **Node.js** |
| Which other non-standard port is used? | **31331** |
| Which software uses this port? | **Apache** |
| Which GNU/Linux distribution seems to be used? | **Ubuntu** |
| The software using port 8081 is a REST API — how many routes are used by the web app? | **2** |

---

## Exploitation

I discovered two primary web entry points:

- Apache web service on **port 31331**
- Node.js REST API on **port 8081**

Directory enumeration (`gobuster`) revealed a `partners.html` page. Viewing its HTML source showed that there was **no backend action** on the login form; instead, it referenced two JavaScript files:

```
js/app.min.js
js/api.js
```

This hinted that the **client-side handled all logic**, making it worthwhile to inspect the JavaScript for hidden routes or API endpoints.

---

### Analyzing `api.js`

Inspecting `api.js` showed a minimal API wrapper that passed user input directly into a **system-level ping command** — without sanitization. Essentially, the backend was running something like:

```javascript
system("ping " + user_input)
```

This exposed a **classic command injection** vulnerability.

To confirm this safely, I tested low-impact payloads against the `ip` parameter. Using a backtick-style payload triggered command execution:

```bash
http://<TARGET_IP>:8081/ping?ip=`ls`
```

The server output listed filenames from the working directory — including **`utech.db.sqlite`**, confirming **remote code execution (RCE)** in the web process.

---

### Database Discovery

After verifying RCE, I used the same injection vector to perform limited enumeration:

```bash
whoami
pwd
ls -la
```

Among the results, the SQLite database **`utech.db.sqlite`** stood out.

<img width="1049" height="521" alt="partners" src="https://github.com/user-attachments/assets/0885f8b3-f022-45ab-952c-aa851b1bd00c" />
<img width="1425" height="948" alt="login page" src="https://github.com/user-attachments/assets/4dd926b0-0a8b-4842-afbb-386fe20f6c9c" />
<img width="1416" height="1013" alt="pagesource" src="https://github.com/user-attachments/assets/ce4a0d9c-ca3e-4829-b668-9666c0da1a00" />
<img width="1417" height="878" alt="js" src="https://github.com/user-attachments/assets/80e71242-f8fc-4cce-a3bf-f6f7949cc859" />
<img width="1417" height="538" alt="ping" src="https://github.com/user-attachments/assets/7e9f4dc2-a0df-4467-9e1f-7311cdc2f6ce" />

---

### There is a database lying around — what is its filename?

`utech.db.sqlite`

<img width="1415" height="327" alt="cat" src="https://github.com/user-attachments/assets/dc7f3b52-b47e-42f8-83e1-89974a10235c" />

From that database, I extracted **two MD5 password hashes**.  
Using [hashes.com](https://hashes.com/en/decrypt/hash) to crack them revealed the following credentials.

| Question | Answer |
|-----------|--------|
| What is the first user's password hash? | `f357a0c52799563c7c7b76c1e7543a32` |
| What is the password associated with this hash? | `n100906` |

---

## Privilege Escalation

With valid credentials in hand, I authenticated and obtained a shell as **r00t (Docker container context)**.

Local enumeration revealed **Docker** was installed, and a **bash image** was available.  
Since I could execute Docker commands, I leveraged this to **escape to the host filesystem** using a bind mount and chroot technique:

```bash
docker run -v /:/mnt --rm -it bash chroot /mnt sh
```

Once chrooted into `/mnt`, I had full access to the host filesystem — including **/root/.ssh/id_rsa**.  
Copying the private key allowed SSH access as **root** on the host, completing full compromise.

---

### What are the first 9 characters of the root user's private SSH key?

`MIIEogIBA`

---

## Conclusion

This challenge showcased how a **client-side API call** (the `ping` endpoint) can lead to **full host compromise** through:

1. Client-side inspection revealing a vulnerable API  
2. Command injection through unsanitized input  
3. Discovery and exfiltration of sensitive database data  
4. Cracking credentials to gain shell access  
5. Docker misuse allowing **container escape**  
6. Extraction of the root SSH private key for full control

---

### Key Takeaways

- **Validate and sanitize all user input**, especially before passing data to shell commands.  
- **Never expose database files** or credentials via web-accessible paths.  
- **Restrict Docker usage** — only trusted administrators should run containers with host mounts.  
- **Apply least privilege** across all services to minimize blast radius.  
- **Monitor outbound connections** from web apps for unexpected command behavior.

---

### Tools Used

- `nmap`, `gobuster`, `curl`, `sqlite3`, `hashes.com`  
- `docker`, `chroot`, `bash`  
- `Burp Suite` for inspecting API requests/responses  

---

### Summary Table

| Stage | Description | Result |
|--------|-------------|--------|
| Recon | Nmap + Gobuster | Discovered ports 8081 & 31331 |
| Exploit | Command injection in ping API | Remote code execution |
| Loot | Extracted SQLite DB | Obtained user credentials |
| PrivEsc | Docker abuse (bind mount) | Root-level access |
| Flag | `/root/.ssh/id_rsa` | First 9 chars: `MIIEogIBA` |

---
