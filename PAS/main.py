import os
import scanner
import quarantine 
import shredder
from datetime import datetime

# Use relative paths for portability
LOG_FILE = os.path.join("logs", "scan_log.txt")
QUARANTINE_FOLDER = os.path.join("Quarantine")

# Ensure the quarantine folder exists
os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

def log_results(infected, quarantined=None, deleted=None):
    """Log the results of the scan, quarantine actions, and file deletions to a log file"""
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as log:
            log.write(f"=== Scan at {datetime.now()} ===\n")

            if infected:
                for f in infected:
                    log.write(f"[INFECTED] {f}\n")
            else:
                log.write("No infected files found.\n")

            if quarantined:
                for f in quarantined:
                    log.write(f"[QUARANTINED] {f}\n")

            if deleted:
                for f in deleted:
                    log.write(f"[DELETED] {f}\n")

            log.write("\n")

    except Exception as e:
        print(f"Error writing to log file: {e}")

def write_meta_file(quarantined_path, original_path):
    try:
        with open(quarantined_path + ".meta", "w", encoding="utf-8") as meta:
            meta.write(original_path)
    except Exception as e:
        print(f"[PAS] ❌ Failed to write .meta for {quarantined_path}: {e}")

def main():
    """Main function to execute the file scan"""
    target = input("Enter folder path to scan: ")
    if not os.path.exists(target):
        print("Path does not exist.")
        return

    print("\nLoading signatures...")
    signatures = scanner.load_signatures()
    print(f"Loaded {len(signatures)} signatures.")

    print("\nScanning...")
    infected_files = scanner.scan_directory(target, signatures)

    quarantined_files = []
    deleted_files = []

    existing_quarantined_files = [os.path.join(QUARANTINE_FOLDER, f) for f in os.listdir(QUARANTINE_FOLDER) if f.endswith("_quarantined")]

    if infected_files:
        print("\nInfected files found:")
        for infected_file in infected_files:
            print(f"- {infected_file}")
            quarantine_path = quarantine.quarantine_file(infected_file)
            if quarantine_path:
                write_meta_file(quarantine_path, infected_file)
                quarantined_files.append(quarantine_path)
                print(f"File quarantined: {quarantine_path}")

        all_quarantined_files = existing_quarantined_files + quarantined_files

        print("\nThe following files have been quarantined (new + existing):")
        for i, quarantined_file in enumerate(all_quarantined_files, 1):
            print(f"{i}. {quarantined_file}")

    else:
        print("\nNo infected files found.")
        if existing_quarantined_files:
            print("\nExisting quarantined files:")
            for i, quarantined_file in enumerate(existing_quarantined_files, 1):
                print(f"{i}. {quarantined_file}")
        all_quarantined_files = existing_quarantined_files

    delete_choice = input("\nDo you want to delete all quarantined files or choose specific ones? (all/choose): ").lower()

    if delete_choice == 'all':
        for quarantined_file in all_quarantined_files:
            shredded = shredder.shred_file(quarantined_file)
            if shredded:
                deleted_files.append(quarantined_file)
                print(f"File {quarantined_file} has been permanently deleted.")
                meta_file = quarantined_file + ".meta"
                if os.path.exists(meta_file):
                    os.remove(meta_file)
            else:
                print(f"Failed to delete {quarantined_file}.")
    elif delete_choice == 'choose':
        delete_choice = input("\nEnter the numbers of the files to delete (comma separated): ").lower()
        try:
            indices = [int(x.strip()) - 1 for x in delete_choice.split(',')]
            for index in indices:
                if 0 <= index < len(all_quarantined_files):
                    quarantined_file = all_quarantined_files[index]
                    shredded = shredder.shred_file(quarantined_file)
                    if shredded:
                        deleted_files.append(quarantined_file)
                        print(f"File {quarantined_file} has been permanently deleted.")
                        meta_file = quarantined_file + ".meta"
                        if os.path.exists(meta_file):
                            os.remove(meta_file)
                    else:
                        print(f"Failed to delete {quarantined_file}.")
                else:
                    print(f"Invalid index: {index + 1}")
        except ValueError:
            print("Invalid input! Please enter valid numbers separated by commas.")

    log_results(infected_files, quarantined_files, deleted_files)

if __name__ == "__main__":
    main()