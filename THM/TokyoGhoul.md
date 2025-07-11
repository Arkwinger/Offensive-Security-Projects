# Tokyo Ghoul: Rize – TryHackMe CTF Walkthrough

 
## Introduction 
This challenge blends stylized horror themes with practical offensive techniques. Inspired by Tokyo Ghoul, the box pushes you to think like a creative attacker — combining web fuzzing, steganography, hash cracking, and sandbox escape. It's a study in exploiting misconfigurations, decoding hidden clues, and chaining vulnerabilities to root. I’ll walk through each phase in technical detail, highlighting why every step mattered and how it reflects real-world attack surfaces.

<img width="7000" height="5000" alt="Screenshot (45)" src="https://github.com/user-attachments/assets/c3c3873a-e4a0-450c-8f04-16e191c81b2c" />


## Task2 – Where am I?
As with any CTF or penetration test, the first step is understanding the attack surface. I kicked things off by running a full TCP port scan using nmap, one of the most widely used network discovery tools. This helps enumerate all available services, including those on non-standard ports, which might otherwise go unnoticed.

<img width="1474" height="636" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/6a2a35db-7c9c-45e5-9e27-66f7a0bf9a53" />


 Command Used
bash
<pre> ```bash nmap -p- -sC -sV -oN fullscan.txt 10.10.131.242 ``` </pre>
-p- → Scans all 65,535 ports, not just common ones.

-sC → Runs default scripts for basic vulnerability detection.

-sV → Attempts to identify service versions, useful for fingerprinting.

-oN fullscan.txt → Outputs results to a readable text file for later reference.

Scanning all ports gives visibility into potentially hidden services. The default scripts may reveal basic vulnerabilities, while version detection is key for identifying outdated or exploitable software.

📊 Scan Results
**Scan Results:**
- **Port 21 (FTP)** – vsftpd 3.0.3 — possible anonymous login or misconfigs
- **Port 22 (SSH)** – OpenSSH 8.2p1 — potential shell access
- **Port 80 (HTTP)** – Apache 2.4.41 — main web entry point


Based on version banners and service responses, the underlying operating system appears to be Ubuntu.

✅ How many ports are open? → 3 ✅ What is the OS used? → Ubuntu


## Task 3 – Planning to Escape
After initial enumeration, I started digging deeper into the web server. Normally, I always check the webpage. I did so by going there first. It brought me to a static page that included a link...


<img width="1427" height="879" alt="Screenshot (25)" src="https://github.com/user-attachments/assets/c4a95227-173b-4884-9180-a8ca4796ea4e" />


During directory fuzzing, I also discovered the endpoint for Jason's room.

http://10.10.131.242/jasonroom.html
The page itself was blank, but viewing the HTML source revealed a hidden comment left by the “other ghouls.” It referenced messages left behind, which indicated there were additional clues buried deeper in the system.

<img width="1594" height="522" alt="Screenshot (26)" src="https://github.com/user-attachments/assets/e9decdf8-d2c9-4e49-908a-940262deb812" />



✅ Did you find the note the other ghouls gave you? Yes — it was embedded in the source code of /jasonroom.html as an HTML comment.

After seeing the clue, I remembered from before, that there was anonymous login to the FTP server. I decided to check it out. 

<img width="1488" height="879" alt="Screenshot (27)" src="https://github.com/user-attachments/assets/9cb0db77-5125-4806-90f2-7f65c2a67eda" />

There were various files that we could extract using the GET (filename) command:

get rize_and_kaneki.jpg
get need_to_talk

I explored a folder named:

/Talk_with_me
Inside, I found two files:

rize_and_kaneki.jpg

need_to_talk

 Using rabin2 -z, I inspected the need_to_talk file — it was a cryptic note in plain text, hinting that something deeper was embedded in the image.

 
<img width="1492" height="878" alt="Screenshot (44)" src="https://github.com/user-attachments/assets/a480cd20-8f5d-43d5-ac18-300fc8a5934d" />


✅ What is the key for Rize executable? kamishiro

Next, it was important to look at the .jpeg file. This could have something hidden inside of it!
Extracting the Hidden File with Steghide


bash
steghide extract -sf rize_and_kaneki.jpg -p You_found_1t
-sf points to the source image

-p supplies the known passphrase: You_found_1t

 Recovered Payload: yougotme.txt
The command successfully extracted a file:

yougotme.txt
Opening it revealed lines of dot-dash sequences, like:

....- .-
....- -..
...-- ..---

Decoding Logic: Right away, I noticed that it was morse code. I decided to use - [CyberChef](https://gchq.github.io/CyberChef/) to decode. 

**CyberChef Flow:**
Morse → Hex → Base64 → `d1r3c70ry_center`


<img width="2000" height="1000" alt="Screenshot (30)" src="https://github.com/user-attachments/assets/c7ad2de3-e59e-4355-9137-e10d2bf1e01d" />
<img width="2000" height="1000" alt="Screenshot (31)" src="https://github.com/user-attachments/assets/2cff5754-0301-4b45-9ffe-03c73d90bade" />
<img width="2000" height="1000" alt="Screenshot (32)" src="https://github.com/user-attachments/assets/f8676008-8099-41fd-85aa-0f95f93e5b3b" />



## Task 4 – What Rize is trying to say?
I browsed to:

http://10.10.131.242/d1r3c70ry_center/
The page showed an eerie animated message: “Scan Me.” That was my cue to run another directory enumeration using - [Gobuster](https://github.com/OJ/gobuster):

<img width="1613" height="885" alt="Screenshot (33)" src="https://github.com/user-attachments/assets/3cd3fe3e-35bd-401b-8352-effa1fcba074" />



bash
gobuster dir -u http://10.10.131.242/d1r3c70ry_center/ -w /usr/share/wordlists/dirb/common.txt

Gobuster Results
/claim
Navigating to /claim brought me to a new interactive web application with YES/NO buttons and a view parameter — signaling the start of the next attack vector: Local File Inclusion (LFI).


<img width="1576" height="894" alt="Screenshot (34)" src="https://github.com/user-attachments/assets/3097494f-d7b3-44a9-a662-d2922862d47c" />


I found myself on a page that presented YES/NO buttons. These interacted with the backend using a view parameter:

index.php?view=flower.gif
This type of structure is often vulnerable to Local File Inclusion (LFI), where unsanitized file paths can be manipulated to access system files. I started by attempting a classic LFI path to read /etc/passwd:

bash
?view=../../../../etc/passwd
However, this request was blocked with a cheeky message:

“no no no silly don’t do that”

To bypass this superficial filter, I encoded the file path using URL-encoded characters:

bash
?view=%2F%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd
This successfully returned the contents of /etc/passwd.

<img width="1574" height="892" alt="Screenshot (35)" src="https://github.com/user-attachments/assets/5730bc79-3e3f-4125-8e69-37557a2014c9" />

<img width="1585" height="899" alt="Screenshot (36)" src="https://github.com/user-attachments/assets/72f523a6-87f3-4c40-9265-ffe83665b900" />

<img width="1582" height="893" alt="Screenshot (37)" src="https://github.com/user-attachments/assets/c79bf5a0-4ec9-4b6b-99e6-6e1d369e1e31" />


Extracted Information
From the dumped file, I found a valid user entry:

kamishiro:x:1001:1001:/home/kamishiro:/bin/bash
Alongside that, there was a SHA-512 password hash:

$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0

✅ What is rize username ? kamishiro 

<img width="1482" height="867" alt="Screenshot (39)" src="https://github.com/user-attachments/assets/d4bdb045-0701-4b01-9e6e-31a02b0b82f7" />

Saved the hash:
bash
echo '$6$Tb/euwmK$OXA.dwMeOAcopwBl68boTG5zi65wIHsc84OWAIye5VITLLtVlaXvRDJXET..it8r.jbrlpfZeMdwD3B0fGxJI0' > kamishiro.hash

Cracked with John:
bash
john --wordlist=/usr/share/wordlists/rockyou.txt --format=sha512crypt kamishiro.hash

> ✅ **Rize's Password:** `password123`

SSH'd in:
bash
ssh kamishiro@10.10.131.242

Found and grabbed user.txt:
e6215e25c0783eb4279693d9f073594a

## Task 5 - Fight Jason
After gaining SSH access as kamishiro, I was able to read the user flag located in the home directory:
bash
cat /home/kamishiro/user.txt

✅ user.txt: e6215e25c0783eb4279693d9f073594a
From there, I checked sudo permissions and discovered I could run a Python jail script as root:
bash
sudo /usr/bin/python3 /home/kamishiro/jail.py

<img width="1484" height="285" alt="Screenshot (42)" src="https://github.com/user-attachments/assets/62d7af95-6ce2-4c02-8449-001a701e22b3" />


After attempting several bypass methods, I used an evasion payload to bypass the keyword filter and execute:
python
__builtins__.__dict__['__IMPORT__'.lower()]('OS'.lower()).__dict__['SYSTEM'.lower()]('cat /root/root.txt')

<img width="1492" height="424" alt="Screenshot (44)" src="https://github.com/user-attachments/assets/b4663c2b-7b0f-4d09-a4b5-6e9fa2d0be92" />


✅ root.txt: 9d790bb87898ca66f724ab05a9e6000b

## In the real world 

To mitigate the vulnerabilities exposed in this box, several layers of defense must be considered. Steganographic techniques demonstrate the risk of allowing unchecked file uploads — images and media should be thoroughly inspected beyond just their extensions. Hidden directories were easily uncovered, reminding us that obscurity is not an effective form of access control; proper authentication and authorization must be enforced instead.

The Local File Inclusion flaw was bypassed with simple URL encoding, which reinforces the necessity of validating user input rigorously and using secure coding patterns that prevent file traversal. Even though the system used a strong hashing algorithm (SHA-512), the password itself was trivially weak. This illustrates the importance of enforcing strong credential policies and implementing mechanisms like multi-factor authentication and rate limiting.

Lastly, the Python jail relied on naive string filtering to block dangerous commands. Such an approach is fundamentally flawed. True sandboxing demands process-level isolation, containerization, or secure restricted environments — not just a blacklist of forbidden terms. Defense in depth isn't optional in systems exposed to adversarial behavior; it's the baseline.



Thanks for reading!




































