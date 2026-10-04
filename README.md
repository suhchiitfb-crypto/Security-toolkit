# Security Toolkit

A small Python toolkit for automated vulnerability testing and phishing detection, built while learning penetration testing and defensive security fundamentals against OWASP Juice Shop (an intentionally vulnerable practice application).

## ⚠️ Legal & Ethical Use

This tool is for educational use against systems you own or have explicit permission to test — such as your own local instance of a deliberately vulnerable app like OWASP Juice Shop. Do not run the vulnerability checks against systems you do not own or have authorization to test. The phishing checker is a defensive tool and safe to use against any public domain.

## Features

**`security_toolkit.py`** — offensive checks against a local test target:
- **SQL Injection check** — tests whether a login form is vulnerable to authentication bypass via a classic `' OR 1=1--` payload
- **IDOR (Insecure Direct Object Reference) check** — automatically probes multiple resource IDs to check whether access control properly restricts users to their own data

**`phishing_checker.py`** — interactive, defensive domain/URL analysis:
- Detects lookalike domains (character substitution like `1`→`l`, `rn`→`m`, brand names hidden in unrelated domains)
- Checks domain registration age via `whois`
- Flags commonly-abused top-level domains (`.tk`, `.xyz`, `.top`, etc.)
- Checks whether a domain supports HTTPS
- Detects classic URL obfuscation tricks: the `@` redirect trick and raw IP addresses in place of domain names
- Gives a combined red-flag count verdict per domain

## How to run

1. Clone this repository
2. Set up a virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv

3. For `security_toolkit.py`, create a `.env` file with your own test target's auth token:

JUICE_SHOP_TOKEN=your_token_here

4. Run either tool:

python3 security_toolkit.py
python3 phishing_checker.py