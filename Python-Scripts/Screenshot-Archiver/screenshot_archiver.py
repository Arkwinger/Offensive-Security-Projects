from playwright.sync_api import sync_playwright
from pathlib import Path

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)

with open("urls.txt", "r") as file:
    urls = [line.strip() for line in file if line.strip()]

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    for url in urls:

        try:

            print(f"Capturing: {url}")

            page.goto(
                url,
                wait_until="networkidle",
                timeout=15000
            )

            filename = (
                url.replace("https://", "")
                   .replace("http://", "")
                   .replace("/", "_")
            )

            page.screenshot(
                path=f"screenshots/{filename}.png",
                full_page=True
            )

            print(
                f"[+] Saved: screenshots/{filename}.png"
            )

        except Exception as e:

            print(
                f"[-] Failed: {url}"
            )

            print(
                f"    {e}"
            )

    browser.close()

print("\nDone.")
