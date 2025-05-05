import shutil
import os
from PAS import shredder

# Use relative quarantine path
quarantine_dir = os.path.join("Quarantine")
os.makedirs(quarantine_dir, exist_ok=True)

def quarantine_file(file_path):
    """Move the infected file to the quarantine folder and store its original path in a .meta file."""
    if not os.path.exists(file_path):
        print(f"[PAS] ❌ File not found: {file_path}")
        return None

    try:
        filename = os.path.basename(file_path)
        quarantine_file_path = os.path.join(quarantine_dir, filename + "_quarantined")
        meta_file_path = quarantine_file_path + ".meta"

        # Overwrite if exists
        if os.path.exists(quarantine_file_path):
            os.remove(quarantine_file_path)
        if os.path.exists(meta_file_path):
            os.remove(meta_file_path)

        shutil.move(file_path, quarantine_file_path)
        with open(meta_file_path, "w", encoding="utf-8") as meta:
            meta.write(file_path)

        print(f"[PAS] ✅ Quarantined: {quarantine_file_path}")
        return quarantine_file_path
    except Exception as e:
        print(f"[PAS] ❌ Failed to quarantine {file_path}: {e}")
        return None

def get_original_path(quarantined_file):
    """Retrieve original path from the corresponding .meta file."""
    meta_path = quarantined_file + ".meta"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as meta:
            return meta.read().strip()
    return None