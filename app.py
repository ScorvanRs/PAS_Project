import streamlit as st
import os
import shutil
from datetime import datetime
from PAS.scanner import calculate_hash, load_signatures, scan_directory
from PAS.quarantine import quarantine_file, get_original_path
from PAS.shredder import shred_file


# Ensure required folders exist
os.makedirs("temp", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("Quarantine", exist_ok=True)  # For portability

QUARANTINE_PATH = os.path.abspath("Quarantine")
LOG_PATH = os.path.join("logs", "scan_log.txt")

st.set_page_config(page_title="🔹 PAS Antivirus", layout="centered")
st.title("🔹 PAS - Prototype Antivirus System")

# Load signatures once
signatures = load_signatures()

# UI Tabs
tab1, tab2, tab3 = st.tabs(["🧪 File/Folder Scanner", "📜 View Logs", "💃 Quarantine Manager"])

# ------------------ TAB 1: File/Folder Scanner ------------------
with tab1:
    st.header("🧪 File/Folder Scanner")
    path = st.text_input("Enter the full path to a file or folder to scan")

    if path:
        if os.path.isfile(path):
            if st.button("🔍 Scan File"):
                sha256 = calculate_hash(path, "sha256")
                md5 = calculate_hash(path, "md5")
                sha1 = calculate_hash(path, "sha1")

                match = None
                if sha256 in signatures:
                    match = ("SHA256", sha256)
                elif md5 in signatures:
                    match = ("MD5", md5)
                elif sha1 in signatures:
                    match = ("SHA1", sha1)

                if match:
                    st.error(f"⚠️ INFECTED FILE DETECTED\nMatch found in {match[0]}:\n{match[1]}")
                    log_entry = f"[{datetime.now()}] INFECTED: {path} ({match[0]}: {match[1]})"
                    with open(LOG_PATH, "a", encoding="utf-8") as log:
                        log.write(log_entry + "\n")
                    st.code(log_entry)

                    quarantine_result = quarantine_file(path)
                    if quarantine_result:
                        st.success("🚫 File quarantined automatically.")
                    else:
                        st.error("❌ Failed to quarantine file.")
                else:
                    st.success("✅ File is clean.")
                    with open(LOG_PATH, "a", encoding="utf-8") as log:
                        log.write(f"[{datetime.now()}] CLEAN: {path}\n")

        elif os.path.isdir(path):
            if st.button("🔍 Scan Folder"):
                with st.spinner("Scanning directory..."):
                    infected_files = scan_directory(path, signatures)

                if infected_files:
                    st.error(f"⚠️ {len(infected_files)} infected file(s) found:")
                    for f in infected_files:
                        st.code(f)
                        with open(LOG_PATH, "a", encoding="utf-8") as log:
                            log.write(f"[{datetime.now()}] INFECTED: {f}\n")

                    for f in infected_files:
                        quarantine_file(f)

                    st.success(f"🚫 {len(infected_files)} file(s) quarantined.")
                else:
                    st.success("✅ No infected files found.")
                    with open(LOG_PATH, "a", encoding="utf-8") as log:
                        log.write(f"[{datetime.now()}] Folder '{path}' scanned: no infections.\n")
        else:
            st.warning("Invalid file or folder path.")

# ------------------ TAB 2: Logs Viewer ------------------
with tab2:
    st.header("🌛 View Logs")
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as log:
            content = log.read()
        if content:
            st.text_area("Log Contents", content, height=300)
        else:
            st.info("Log file is empty.")
    else:
        st.warning("No log file found yet.")

# ------------------ TAB 3: Quarantine Manager ------------------
with tab3:
    st.header("💃 Quarantine Manager")

    if os.path.exists(QUARANTINE_PATH):
        files = [f for f in os.listdir(QUARANTINE_PATH) if not f.endswith(".meta")]
        if files:
            st.markdown("### Select files to restore or shred:")
            if "selected_files" not in st.session_state:
                st.session_state.selected_files = set()

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✅ Select All"):
                    st.session_state.selected_files = set(files)
            with col2:
                if st.button("❌ Deselect All"):
                    st.session_state.selected_files = set()

            selected_files = set()
            for file in files:
                checked = st.checkbox(file, value=file in st.session_state.selected_files)
                if checked:
                    selected_files.add(file)

            st.session_state.selected_files = selected_files

            if st.button("🔄 Restore Selected"):
                for selected_file in selected_files:
                    quarantined_path = os.path.join(QUARANTINE_PATH, selected_file)
                    original_path = get_original_path(quarantined_path)
                    if original_path:
                        try:
                            os.makedirs(os.path.dirname(original_path), exist_ok=True)
                            shutil.move(quarantined_path, original_path)
                            os.remove(quarantined_path + ".meta")
                            st.success(f"Restored to: {original_path}")
                        except Exception as e:
                            st.error(f"Failed to restore '{selected_file}': {e}")
                    else:
                        st.error(f"Original path not found for: {selected_file}")

            if st.button("💣 Shred Selected"):
                for selected_file in selected_files:
                    file_to_delete = os.path.join(QUARANTINE_PATH, selected_file)
                    success = shred_file(file_to_delete)
                    if success:
                        meta_file = file_to_delete + ".meta"
                        if os.path.exists(meta_file):
                            os.remove(meta_file)
                        with open(LOG_PATH, "a", encoding="utf-8") as log:
                            log.write(f"[{datetime.now()}] SHREDDED from quarantine: {selected_file}\n")
                        st.warning(f"File '{selected_file}' permanently deleted.")
                    else:
                        st.error(f"⚠️ Failed to delete '{selected_file}'.")
        else:
            st.info("No files in quarantine.")
    else:
        st.warning("No quarantine folder found.")