
import zipfile
import os

def create_zip():
    # Name of the output zip file
    zip_filename = 'invitation_web_project_final.zip'
    
    # Directories/Files to exclude
    EXCLUDE_DIRS = {'venv', '__pycache__', '.git', '.idea', '.vscode'}
    EXCLUDE_EXTENSIONS = {'.pyc', '.pyo', '.pyd'}
    EXCLUDE_FILES = {zip_filename, 'debug_login.zip', 'repair_db.zip'}

    print(f"Creating {zip_filename}...")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk('.'):
                # Modify dirs in-place to skip excluded directories
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                
                for file in files:
                    if file in EXCLUDE_FILES:
                        continue
                        
                    _, ext = os.path.splitext(file)
                    if ext in EXCLUDE_EXTENSIONS:
                        continue
                        
                    file_path = os.path.join(root, file)
                    # Add file to zip with relative path
                    arcname = os.path.relpath(file_path, '.')
                    print(f"Adding: {arcname}")
                    zipf.write(file_path, arcname)
                    
        print(f"\n[SUCCESS] Successfully created {zip_filename}")
        
    except PermissionError as e:
        print(f"\n[ERROR] Permission denied: {e}")
        print("Please ensure no files are open or locked by other programs.")
    except Exception as e:
        print(f"\n[ERROR] Failed to create zip: {e}")

if __name__ == "__main__":
    create_zip()
