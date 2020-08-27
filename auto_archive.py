import os

ALLOWED_FILE_EXTENSIONS = ['.mp4', '.mov']
IGNORE_LIST = ['CL_Intro']
ARCHIVE_FOLDER = 'archive'


def archive():
    result = []
    files = (file for file in os.listdir(os.curdir)
             if any(ext in file for ext in ALLOWED_FILE_EXTENSIONS)
             and not any(ign in file for ign in IGNORE_LIST))
    if ARCHIVE_FOLDER not in os.listdir(os.curdir):
        os.mkdir(ARCHIVE_FOLDER)
        print(f'{ARCHIVE_FOLDER} did not exist and has been created.')
    for file in files:
        try:
            os.rename(file, f'{ARCHIVE_FOLDER}/{file}')
        except Exception as e:
            result.append(f'***{file} was not moved due to an error:\n\t{e}')
        else:
            result.append(f'{file} was moved')

    print('Allowed file extensions:', *ALLOWED_FILE_EXTENSIONS)
    print('Ignored files:', *IGNORE_LIST)
    print(f'Archive folder: /{ARCHIVE_FOLDER}')
    print(f'{len(result)} files found.\n')
    for file in result:
        print(file.strip('"'))


if __name__ == '__main__':
    archive()
    input('\nDone, Press Enter to exit.')
