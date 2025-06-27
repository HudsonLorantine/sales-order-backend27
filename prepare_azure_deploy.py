import os
import zipfile

# Create a deployment zip file
def create_zip():
    # Files to include in the zip
    files_to_zip = [
        'azure_app.py',
        'azure_requirements.txt',
        'startup.sh'
    ]
    
    # Create the zip file
    with zipfile.ZipFile('azure_deploy.zip', 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file)
    
    print(f"Created azure_deploy.zip with {len(files_to_zip)} files")
    print(f"Zip file path: {os.path.abspath('azure_deploy.zip')}")

if __name__ == "__main__":
    create_zip()
