import sys
import time
import pyshorteners
from urllib.parse import urlparse
import re
import qrcode
import json
import os
import random
                                                                                                                                             # PH Flag Colors - High Contrast
B = '\033[1;94m'  # Blue
W = '\033[1;97m'  # White
R = '\033[1;31m'  # Red
Y = '\033[1;93m'  # Yellow
G = '\033[1;32m'  # Green
C = '\033[1;36m'  # Cyan
X = '\033[0m'     # Reset

TOOL_NAME = "SAD-MASK"
VERSION = "v2.5"
AUTHOR = "SadFriends"

SAYINGS = [
    "Buti pa yung link na-mask, yung feelings mo hindi.",
    "URL Masking: Parang make-up, tinatago ang katotohanan.",
    "Huwag kang mafall sa link, parang sa kanya—scam lang 'yan.",
    "Hindi lahat ng link totoo, parang yung 'I love you' niya."
]

def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    # SOLID MABAGA BANNER
    print(f"""{B}  ██████  █████  ██████       ███    ███  █████  ███████ ██   ██
{B} ██      ██   ██ ██   ██      ████  ████ ██   ██ ██      ██  ██
{Y}  █████  ███████ ██   ██ ████ ██ ████ ██ ███████ ███████ █████
{R}      ██ ██   ██ ██   ██      ██  ██  ██ ██   ██      ██ ██  ██
{R} ██████  ██   ██ ██████       ██      ██ ██   ██ ███████ ██   ██ {X}""")
    print(f"{W} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{B}  [#] {W}Created by: {Y}{AUTHOR:<12} {R}The Final Boss of Masking{X}")
    print(f"{W} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  {C}Hugot: {W}\"{random.choice(SAYINGS)}\"{X}\n")

def loading_animation(service_name):
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(10):
        for symbol in spinner:
            sys.stdout.write(f"\r  {C}[{Y}{symbol}{C}] {W}Masking via {service_name}...{X}")
            sys.stdout.flush()
            time.sleep(0.02)
    print("\r\033[K", end='')

def mask_url(domain, keyword, target_url):
    # Nililinis ang domain para siguradong walang http/https sa gitna
    clean_domain = domain.replace("https://", "").replace("http://", "").rstrip('/')
    parsed = urlparse(target_url)
    return f"{parsed.scheme}://{clean_domain}-{keyword}@{parsed.netloc}{parsed.path}"

def generate_qr_code(link, filename="sadmask_qr.png"):
    try:
        qrcode.make(link).save(filename)
        print(f"  {G}✓ QR code saved as {Y}{filename}{X}")
    except:
        print(f"  {R}✗ Failed to save QR code.{X}")

def save_to_file(data, filename="sadmask_links.json"):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"  {Y}✓ Links saved to {filename}{X}")
    except:
        print(f"  {R}✗ Failed to save history.{X}")

def main():
    print_banner()

    # Input Validation (Tulad ng MaskGod)
    while True:
        original_url = input(f"  {G}Enter target URL (e.g. https://site.com): {W}").strip()
        if original_url.startswith("http"): break
        print(f"  {R}✗ Invalid URL. Dapat may http:// o https://{X}")

    domain = input(f"  {Y}Enter fake domain (e.g. google.com): {W}").strip()
    keyword = input(f"  {C}Enter keyword (e.g. claim-now): {W}").strip().replace(" ", "-")

    print("\n")

    # Pyshorteners Setup
    s = pyshorteners.Shortener()
    shorteners = [
        ("TinyURL", s.tinyurl),
        ("Is.gd", s.isgd),
        ("Da.gd", s.dagd),
        ("Clck.ru", s.clckru)
    ]

    results = []
    print(f"  {W}━━━━━━━ {Y}GENERATING MASKED LINKS {W}━━━━━━━{X}\n")

    for name, service in shorteners:
        try:
            loading_animation(name)
            short_url = service.short(original_url)
            masked = mask_url(domain, keyword, short_url)
            print(f"  {G}[✓] {name: <8}: {W}{masked}{X}")
            results.append({"shortener": name, "masked_url": masked})
        except:
            print(f"  {R}[✗] {name: <8}: Service Error/Timeout{X}")

    if results:
        print(f"\n  {W}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        generate_qr_code(results[0]["masked_url"])
        save_to_file(results)
        print(f"  {Y}Mission Accomplished, {AUTHOR}!{X}")
    else:
        print(f"\n  {R}[!] All services failed. Check internet connection.{X}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {R}[!] System Aborted. Stay sad but masked!{X}")
        sys.exit()
