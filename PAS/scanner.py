import hashlib
import os

def calculate_hash(filepath, hash_type='sha256'):
    """Calculate the hash of a file (MD5, SHA-1, or SHA-256)"""
    try:
        hash_function = hashlib.new(hash_type)
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                hash_function.update(chunk)
        return hash_function.hexdigest().lower()
    except Exception as e:
        print(f"Error calculating hash for {filepath}: {e}")
        return None

def load_signatures():
    """Load all hashes from the signature file (MD5, SHA-1, SHA-256)"""
    signatures = set()

    # Path relative to scanner.py, inside PAS/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    signature_path = os.path.join(current_dir, "database", "signatures.txt")

    print(f"Looking for signatures in: {signature_path}")
    try:
        with open(signature_path, 'r', encoding="utf-8") as f:
            for line in f:
                signatures.add(line.strip())
    except FileNotFoundError:
        print(f"[ERROR] {signature_path} not found!")

    return signatures

def scan_directory(directory, signatures):
    """Scan a directory for infected files based on hash matching"""
    infected = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            sha256 = calculate_hash(path, 'sha256')
            md5 = calculate_hash(path, 'md5')
            sha1 = calculate_hash(path, 'sha1')

            print(f"Checking {file} → SHA256: {sha256} | MD5: {md5} | SHA1: {sha1}")

            if sha256 in signatures or md5 in signatures or sha1 in signatures:
                infected.append(path)

    return infected