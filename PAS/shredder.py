import os
import random

def shred_file(file_path, passes=3):
    
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False
        
        # Get the file size
        file_size = os.path.getsize(file_path)
        
        # Open the file in write mode (this will overwrite the file)
        with open(file_path, 'r+b') as f:
            for _ in range(passes):
                # Overwrite the file with random data
                f.seek(0)
                f.write(bytearray(random.getrandbits(8) for _ in range(file_size)))
        
        # Now, delete the file
        os.remove(file_path)
        print(f"File shredded and deleted: {file_path}")
        return True
    except Exception as e:
        print(f"Error shredding file {file_path}: {e}")
        return False
