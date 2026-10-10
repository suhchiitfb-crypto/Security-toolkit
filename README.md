# Security Toolkit

A small Python toolkit for automated vulnerability testing, phishing detection, and Linux security auditing, built while learning penetration testing and defensive security fundamentals against OWASP Juice Shop (an intentionally vulnerable practice application) and a real Ubuntu Linux container.

## ⚠️ Legal & Ethical Use

This tool is for educational use against systems you own or have explicit permission to test — such as your own local instance of a deliberately vulnerable app like OWASP Juice Shop, or your own Linux systems/containers. Do not run the vulnerability checks against systems you do not own or have authorization to test. The phishing checker and SUID auditor are defensive tools, safe to use on any public domain or system you administer.

## Features

**`security_toolkit.py`** — offensive checks against a local test target:
- **SQL Injection check** — tests whether a login form is vulnerable to authentication bypass via a classic `' OR 1=1--` payload
- **IDOR (Insecure Direct Object Reference) checks** — probes multiple resource IDs to check whether access control properly restricts users to their own data, for both read access (baskets) and write access (reviews), with automatic restoration of modified data afterward

**`phishing_checker.py`** — interactive, defensive domain/URL analysis:
- Detects lookalike domains (character substitution like `1`→`l`, `rn`→`m`, brand names hidden in unrelated domains)
- Checks domain registration age via `whois`
- Flags commonly-abused top-level domains (`.tk`, `.xyz`, `.top`, etc.)
- Checks whether a domain supports HTTPS
- Detects classic URL obfuscation tricks: the `@` redirect trick and raw IP addresses in place of domain names
- Gives a combined red-flag count verdict per domain

**`suid_audit.py`** — defensive SUID baseline auditor (run on the target Linux system itself):
- Captures a trusted baseline of SUID binaries (`find / -perm -4000 -type f`)
- Compares future scans against that baseline using set operations
- Flags any new, unexpected SUID binaries — a real indicator of tampering or privilege-escalation backdoors
- Also reports binaries that lost SUID (useful for tracking legitimate patches/updates)

## How to run

1. Clone this repository
2. Set up a virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv

3. For `security_toolkit.py`, create a `.env` file with your own test target's auth token:

JUICE_SHOP_TOKEN=your_token_here

4. Run the tools:

python3 security_toolkit.py
python3 phishing_checker.py

5. For `suid_audit.py`, run directly on the Linux system being audited:

find / -perm -4000 -type f 2>/dev/null > /root/baseline_suid.txt
python3 suid_audit.py


## What I learned building this

- How SQL injection and IDOR vulnerabilities work (both read and write access), found and confirmed hands-on before automating them
- Automating manual security testing with Python and `requests` (GET, POST, and PATCH)
- Why secrets (tokens, credentials) should never be hardcoded — using `.env` files and `python-dotenv` instead
- How phishing domains are disguised (character substitution, hyphenated brand names, lookalike TLDs) and how to detect them programmatically
- Using `difflib` for string similarity and `re` (regular expressions) for pattern matching
- Running and capturing output from command-line tools (`whois`, `find`) via `subprocess`
- Linux SUID privilege escalation (a real GTFOBins-style technique, tested against `find` and `python3`) and how to build detection tooling using baseline comparison and Python set operations
- Writing reusable functions to structure small security tools, rather than one-off scripts