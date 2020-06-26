# bulk rename files
import os
search_str = input('Enter string to search for that is shared by all the files you want to change: ')
append_str = input('Enter string to add to end of name (example: "_FINAL"). leave blank for none: ')
prepend_str = input('Enter string to add to beginning of name (example: "BRKSEC-1234-"). leave blank for none: ')
for old_name in os.listdir(os.curdir):  # loop through all files in the current directory
    if search_str in old_name:  # only operate on files that contain the search string
        try:
            new_name = prepend_str + old_name[:-4] + append_str + old_name[-4:]
            os.rename(old_name, new_name)  # os.rename(old, new); f is the old filename
            print(f'Renamed {old_name}\nto {new_name}\n') # ouput to console
        except Exception as e:
            print(f'    there was was an error with {old_name}')
            print('   ', e)
input('Done')  # so the terminal doesn't close
