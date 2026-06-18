# WebRecon

WebRecon is a Python-based web reconnaissance tool designed to automate common web application discovery tasks.

## Current Features

* Technology detection through HTTP headers
* Server fingerprinting
* Directory enumeration using custom wordlists
* Page title extraction
* Modular Python architecture

## Example Output

```text
Target URL: https://github.com

Results
-------
server: github.com

Directories Found
-----------------
https://github.com/login (200) - Sign in to GitHub
https://github.com/uploads (200) - uploads
```

## Planned Features

* HTML report generation
* Subdomain enumeration
* Multi-threaded scanning
* Screenshot capture
* AI-assisted recon analysis

## Technologies Used

* Python
* Requests
* BeautifulSoup
