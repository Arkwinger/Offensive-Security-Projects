import re

print("Nmap Parser")
print("-----------")

filename = input("Enter Nmap output file: ")

try:

```
with open(filename, "r") as file:
    content = file.readlines()

ports = []

for line in content:

    match = re.search(
        r"(\d+/tcp)\s+open\s+(\S+)",
        line
    )

    if match:

        port = match.group(1)
        service = match.group(2)

        ports.append(
            (port, service)
        )

print("\nOpen Ports Found:\n")

for port, service in ports:

    print(f"{port} - {service}")

print(
    f"\nTotal Open Ports: {len(ports)}"
)
```

except Exception as e:

```
print(f"Error: {e}")
```
