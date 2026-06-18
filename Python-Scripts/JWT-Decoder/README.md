# JWT Decoder

A simple Python utility that decodes JSON Web Tokens (JWTs) and displays the token header and payload in a readable format.

## Features

* Decodes JWT headers
* Decodes JWT payloads
* Pretty-prints JSON output
* Simple command-line interface
* No external dependencies required

## Usage

Run the script:

```bash
python jwt_decoder.py
```

Paste a JWT when prompted:

```text
Paste JWT:
```

The script will decode and display the header and payload.

## Example Output

```json
Header:
{
    "alg": "HS256",
    "typ": "JWT"
}

Payload:
{
    "sub": "1234567890",
    "name": "John"
}
```

## Disclaimer

This utility is intended for educational purposes, lab environments, and authorized security assessments only.
