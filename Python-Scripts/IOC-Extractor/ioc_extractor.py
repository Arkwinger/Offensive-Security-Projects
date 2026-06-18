import re

print("IOC Extractor")
print("-------------")

filename = input("Enter filename: ")

try:

```
with open(filename, "r", encoding="utf-8") as file:
    content = file.read()

ips = set(
    re.findall(
        r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        content
    )
)

domains = set(
    re.findall(
        r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b',
        content
    )
)

urls = set(
    re.findall(
        r'https?://[^\s]+',
        content
    )
)

md5_hashes = set(
    re.findall(
        r'\b[a-fA-F0-9]{32}\b',
        content
    )
)

print("\nIP Addresses:")
for ip in sorted(ips):
    print(ip)

print("\nDomains:")
for domain in sorted(domains):
    print(domain)

print("\nURLs:")
for url in sorted(urls):
    print(url)

print("\nMD5 Hashes:")
for md5 in sorted(md5_hashes):
    print(md5)
```

except Exception as e:

```
print(f"Error: {e}")
```
