import requests
import subprocess
import difflib
import re

known_brands = ["paypal.com", "amazon.com", "google.com", "apple.com", "microsoft.com", "bankofamerica.com"]
suspicious_tlds = [".tk", ".xyz", ".top", ".click", ".loan", ".win"]


def check_lookalike(domain):
    domain_name = domain.split(".")[0]
    normalized = domain_name.replace("1", "l").replace("0", "o").replace("rn", "m")
    parts = normalized.split("-")

    for brand in known_brands:
        brand_name = brand.split(".")[0]
        for part in parts:
            if part == brand_name and domain != brand:
                print("[SUSPICIOUS] '" + domain + "' contains brand name '" + brand_name + "' as part of a longer, unrelated domain")
                return True
            similarity = difflib.SequenceMatcher(None, part, brand_name).ratio()
            if similarity > 0.85 and part != brand_name:
                print("[SUSPICIOUS] '" + domain + "' contains a close misspelling of '" + brand_name + "' (part: '" + part + "', similarity: " + str(round(similarity, 2)) + ")")
                return True

    print("[OK] No close lookalike match found for '" + domain + "'")
    return False

def check_domain_age(domain):
    result = subprocess.run(["whois", domain], capture_output=True, text=True)
    output = result.stdout

    creation_lines = [line.strip() for line in output.splitlines() if "creation date" in line.lower()]
    if creation_lines:
        print("[INFO] " + creation_lines[-1])
        return False
    else:
        print("[INFO] Could not find a specific creation date for '" + domain + "'")
        return True

def check_suspicious_tld(domain):
    for tld in suspicious_tlds:
        if domain.endswith(tld):
            print("[SUSPICIOUS] '" + domain + "' uses a commonly-abused TLD (" + tld + ")")
            return True
    print("[OK] TLD looks unremarkable")
    return False

def check_https(domain):
    try:
        response = requests.get("https://" + domain, timeout=5)
        print("[OK] HTTPS is supported")
        return False
    except requests.exceptions.RequestException:
        print("[SUSPICIOUS] Could not connect via HTTPS (may not be supported, or domain doesn't resolve)")
        return True
def check_url_tricks(url):
    if "@" in url:
        print("[SUSPICIOUS] URL contains '@' - browsers ignore everything before it, a classic redirect trick")
        return True

    ip_pattern = r"://(\d{1,3}\.){3}\d{1,3}"
    if re.search(ip_pattern, url):
        print("[SUSPICIOUS] URL uses a raw IP address instead of a domain name")
        return True

    print("[OK] No obvious URL structure tricks found")
    return False

def analyze_domain(domain):
    print("\n=== Analyzing: " + domain + " ===")
    red_flags = 0

    if check_lookalike(domain):
        red_flags += 1
    if check_domain_age(domain):
        red_flags += 1
    if check_suspicious_tld(domain):
        red_flags += 1
    if check_https(domain):
        red_flags += 1

    print("--- Verdict: " + str(red_flags) + " red flag(s) found ---")

while True:
    user_input = input("\nEnter a domain or URL to analyze (or 'quit' to exit): ")
    if user_input.lower() == "quit":
        break

    domain = user_input.replace("https://", "").replace("http://", "").split("/")[0]

    analyze_domain(domain)
    check_url_tricks(user_input)