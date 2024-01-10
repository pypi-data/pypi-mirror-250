import os
import tarfile
import zipfile
def unzip_data(zipfile_path, unzipfile_path):
    try:
        if zipfile_path.endswith(".tar.gz"):
            with tarfile.open(zipfile_path, 'r:gz') as tar:
                tar.extractall(unzipfile_path)
            print(f'✅ Successfully extracted {zipfile_path} to {unzipfile_path}')
        elif zipfile_path.endswith(".zip"):
            with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
                zip_ref.extractall(unzipfile_path)
            print(f'✅ Successfully extracted {zipfile_path} to {unzipfile_path}')
        else:
            print(f'❌ The dataset is not in tar.gz or zip format!')
    except Exception as e:
        print(f'❌ Extraction failed for {zipfile_path}: {str(e)}')
    finally:
        try:
            os.remove(zipfile_path)
            print(f'✅ Successfully Deleted {zipfile_path}')
        except Exception as e:
            print(f'Deletion failed for {zipfile_path}: {str(e)},but this does not affect the operation of the program,so you can ignore')

def is_directory_empty(path):
    if len(os.listdir(path)) == 0:
        return True
    else:
        return False