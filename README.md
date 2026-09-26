# Security Toolkit

A small Python toolkit for automated vulnerability testing, built while learning penetration testing fundamentals against OWASP Juice Shop (an intentionally vulnerable practice application).

## ⚠️ Legal & Ethical Use

This tool is for educational use against systems you own or have explicit permission to test — such as your own local instance of a deliberately vulnerable app like OWASP Juice Shop. Do not run this against systems you do not own or have authorization to test.

## Features

- **SQL Injection check** — tests whether a login form is vulnerable to authentication bypass via a classic `' OR 1=1--` payload
- **IDOR (Insecure Direct Object Reference) check** — automatically probes multiple resource IDs to check whether access control properly restricts users to their own data

## How to run

1. Clone this repository
2. Set up a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
3. Create a `.env` file with your own test target's auth token:
JUICE_SHOP_TOKEN=your_token_here
4. Run the toolkit:
python3 security_toolkit.py


## What I learned building this

- How SQL injection and IDOR vulnerabilities work, found and confirmed hands-on before automating them
- Automating manual security testing with Python and `requests` (GET and POST)
- Why secrets (tokens, credentials) should never be hardcoded — using `.env` files and `python-dotenv` instead
- Writing reusable functions to structure a small security tool, rather than one-off scripts