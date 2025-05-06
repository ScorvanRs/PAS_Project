# PAS - Prototype Antivirus System

**PAS (Prototype Antivirus System)** is a lightweight antivirus MVP built in Python for educational purposes. It demonstrates core antivirus functions like hash-based detection, quarantine, and secure deletion using a simple and clean Streamlit interface.

---

## 🧩 Features

- **File Scanner (SHA-256-based):** Input the full path to a file. PAS will compute its SHA-256 hash and compare it to known malware signatures.
- **Folder Scanner:** Input a directory path to recursively scan all files using hash comparison.
- **Signature Loader:** Load a list of malware hashes from `signature.txt` (one SHA-256 hash per line).
- **Quarantine System:** Automatically isolates infected files in a quarantine folder.
- **Quarantine Manager (UI-based):** View and delete quarantined files directly in the app.
- **Shredder:** Securely and permanently delete any selected file.
- **Logs Viewer:** Displays logs for each scan session, automatically saved.

---

## 🔍 How Detection Works

PAS does **not analyze file behavior** — it uses **SHA-256 hash comparison** to detect known malware.

1. Files are scanned by calculating their SHA-256 hash.
2. These are compared to a list of known malicious hashes in `PAS/database/signature.txt`.
3. If a match is found, the file is flagged and moved to quarantine.

> ⚠️ **Note:** This is a conceptual prototype. It does not protect against zero-day or unknown threats.

---

## 🧪 Testing (Optional)

You can download a separate folder called `dummy_files/` which contains **harmless test files** with hashes already listed in the signature list.

Use it to test:
- File scanning
- Folder scanning
- Quarantine system
- Log creation

✅ These files are safe and meant only for demonstration.

---

## 🚀 Getting Started

### Requirements

- Python **3.11.9**
- Streamlit
- Dependencies listed in `requirements.txt`

### Installation

```bash
git clone https://github.com/ScorvanRs/PAS_Project.git
cd PAS_Project
pip install -r requirements.txt
```

## Run The App


```bash
streamlit run app.py
```




##📁 Project Structure

```css
PAS_Project/
├── app.py
├── PAS/
│   ├── database/
│   │   └── signature.txt
│   ├── main.py
│   ├── quarantine.py
│   ├── scanner.py
│   ├── shredder.py
│   └── ...
├── Quarantine/
├── temp/
├── requirements.txt
└── README.md
```


##🛡 Disclaimer
This project is for educational purposes only and is not a replacement for real antivirus software.
