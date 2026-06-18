# Hash Identifier

A simple Bash script that attempts to identify common hash types based on hash length.

## Features

* Detects common hash formats
* Supports:

  * MD5
  * SHA1
  * SHA224
  * SHA256
  * SHA384
  * SHA512
* Lightweight and easy to use

## Usage

Make the script executable:

```bash
chmod +x hashid.sh
```

Run the script:

```bash
./hashid.sh <hash>
```

Example:

```bash
./hashid.sh 5f4dcc3b5aa765d61d8327deb882cf99
```

## Example Output

```text
Hash Length: 32
Possible: MD5
```

## Disclaimer

This script is intended for educational purposes, lab environments, and authorized security assessments only.
