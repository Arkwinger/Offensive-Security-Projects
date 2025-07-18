# ReconCreep

Simulated Recon Tool for Pentesting

ReconCreep mimics basic information gathering techniques used during early stages of penetration testing. It performs banner grabbing on common open ports and simulates service fingerprinting

##  Features
- Fake banner grabbing over sockets
- Targets common ports (21, 22, 80, 443, 8080)
- Stylized output with simulated service responses

##  Usage

```bash
python3 reconcreep.py <target-ip>
```

## Requirements 
```
pip install requests python-whois dnspython

```

