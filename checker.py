import hashlib, os, json

def generate_hash(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def load_hashes():
    if os.path.exists('hash_records.json'):
        with open('hash_records.json', 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open('hash_records.json', 'w') as f:
        json.dump(hashes, f, indent=4)

def check_files(directory):
    old = load_hashes()
    new = {}
    changes = []

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            file_hash = generate_hash(path)
            new[path] = file_hash

            if path not in old:
                changes.append(f"[+] New file: {path}")
            elif old[path] != file_hash:
                changes.append(f"[!] Modified file: {path}")

    for path in old:
        if path not in new:
            changes.append(f"[-] Deleted file: {path}")

    save_hashes(new)
    return changes

if __name__ == "__main__":
    folder = input("Enter folder path to monitor: ")
    changes = check_files(folder)
    if changes:
        for c in changes:
            print(c)
    else:
        print("No changes detected.")
