import base64
import hashlib
import urllib.parse
import codecs
import json

def jwt_decode(token):

    try:

        header, payload, signature = token.split(".")

        def decode_part(part):

            padding = "=" * (-len(part) % 4)

            return json.loads(
                base64.urlsafe_b64decode(
                    part + padding
                )
            )

        print("\nHeader:")
        print(
            json.dumps(
                decode_part(header),
                indent=4
            )
        )

        print("\nPayload:")
        print(
            json.dumps(
                decode_part(payload),
                indent=4
            )
        )

    except Exception:

        print("Invalid JWT")


while True:

    print("\nCyberChef CLI")
    print("-------------")

    print("1. Base64 Encode")
    print("2. Base64 Decode")
    print("3. URL Encode")
    print("4. URL Decode")
    print("5. Hex Encode")
    print("6. Hex Decode")
    print("7. MD5 Hash")
    print("8. SHA1 Hash")
    print("9. SHA256 Hash")
    print("10. ROT13")
    print("11. JWT Decode")
    print("0. Exit")

    choice = input("\nChoice: ")

    if choice == "0":
        break

    data = input("Input: ")

    try:

        if choice == "1":

            print(
                base64.b64encode(
                    data.encode()
                ).decode()
            )

        elif choice == "2":

            print(
                base64.b64decode(
                    data
                ).decode()
            )

        elif choice == "3":

            print(
                urllib.parse.quote(
                    data
                )
            )

        elif choice == "4":

            print(
                urllib.parse.unquote(
                    data
                )
            )

        elif choice == "5":

            print(
                data.encode().hex()
            )

        elif choice == "6":

            print(
                bytes.fromhex(
                    data
                ).decode()
            )

        elif choice == "7":

            print(
                hashlib.md5(
                    data.encode()
                ).hexdigest()
            )

        elif choice == "8":

            print(
                hashlib.sha1(
                    data.encode()
                ).hexdigest()
            )

        elif choice == "9":

            print(
                hashlib.sha256(
                    data.encode()
                ).hexdigest()
            )

        elif choice == "10":

            print(
                codecs.encode(
                    data,
                    "rot_13"
                )
            )

        elif choice == "11":

            jwt_decode(data)

        else:

            print("Invalid option")

    except Exception as e:

        print(f"Error: {e}")
