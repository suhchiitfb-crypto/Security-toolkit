import subprocess

def get_current_suid():
    result = subprocess.run(
        ["find", "/", "-perm", "-4000", "-type", "f"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )
    return set(result.stdout.strip().splitlines())

def load_baseline(path="/root/baseline_suid.txt"):
    with open(path) as f:
        return set(line.strip() for line in f if line.strip())

def audit():
    baseline = load_baseline()
    current = get_current_suid()

    new_suid = current - baseline
    missing_suid = baseline - current

    print("=== SUID Audit Report ===")
    print("Baseline count: " + str(len(baseline)))
    print("Current count: " + str(len(current)))

    if new_suid:
        print("\n[ALERT] New SUID binaries NOT in baseline:")
        for f in sorted(new_suid):
            print("  + " + f)
    else:
        print("\n[OK] No new SUID binaries found.")

    if missing_suid:
        print("\n[INFO] Baseline binaries no longer SUID (could be a legitimate patch/update):")
        for f in sorted(missing_suid):
            print("  - " + f)

    if not new_suid and not missing_suid:
        print("\nSystem matches baseline exactly. No changes detected.")

audit()
