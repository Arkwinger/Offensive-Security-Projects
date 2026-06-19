# Screenshot Archiver

A Python utility that captures screenshots of websites and saves them locally for review.

This tool is useful for quickly documenting web applications, reviewing discovered assets, and creating visual records during security assessments and lab environments.

## Features

* Capture screenshots from a list of URLs
* Automatically save images to a local directory
* Supports bulk website processing
* Useful for reconnaissance and documentation workflows

## How to Use

1. Install the required dependencies:

```bash
pip install playwright
playwright install
```

2. Add target URLs to `urls.txt`:

Example: 
```text
https://github.com
https://google.com
https://microsoft.com
```

3. Run the script:

```bash
python screenshot_archiver.py
```

4. View the captured screenshots in the `screenshots` directory.


## Disclaimer

This tool is intended for educational purposes, lab environments, and authorized security assessments only.
