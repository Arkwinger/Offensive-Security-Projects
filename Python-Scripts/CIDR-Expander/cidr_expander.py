import ipaddress

print("CIDR Expander")
print("-------------")

network = input("Enter CIDR range: ")

try:
net = ipaddress.ip_network(network, strict=False)

```
print(f"\nHosts in {network}:\n")

for ip in net.hosts():
    print(ip)
```

except ValueError:
print("Invalid CIDR range.")
