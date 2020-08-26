import os


ALLOWED_FILE_EXTENSIONS = ['.mp4', '.mov']
IGNORE_LIST = ['CL_Intro']
ARCHIVE_FOLDER = 'archive'

files = (file for file in os.listdir(os.curdir)
         if any(ext in file for ext in ALLOWED_FILE_EXTENSIONS)
         and not any(ign in file for ign in IGNORE_LIST))

for file in files:
    print(file)
    os.rename(file, f'{ARCHIVE_FOLDER}/{file}')
