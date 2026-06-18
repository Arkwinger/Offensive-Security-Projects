import base64
import json

print("JWT Decoder")
print("-----------")

token = input("Paste JWT: ")

try:
header, payload, signature = token.split(".")

```
def decode_part(part):
    padding = "=" * (-len(part) % 4)
    decoded = base64.urlsafe_b64decode(part + padding)
    return json.loads(decoded)

header_data = decode_part(header)
payload_data = decode_part(payload)

print("\nHeader:")
print(json.dumps(header_data, indent=4))

print("\nPayload:")
print(json.dumps(payload_data, indent=4))
```

except Exception as e:
print(f"\nError: {e}")
print("Invalid JWT format.")
