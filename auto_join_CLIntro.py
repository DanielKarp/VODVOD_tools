import os
import sys

CL_INTRO = 'CL-Intro.mp4'
LISTFILE = 'concat_list.txt'

def main():
    result = []
    if len(sys.argv) > 1:
        searchstr = sys.argv[1]
        vids = [file for file in os.listdir(os.curdir) if searchstr in file]

        for vid in vids:
            with open(LISTFILE, mode='w') as f:
                print('file', CL_INTRO, file=f)
                print('file', f"'{vid}'", file=f)
            output = f'"{os.path.splitext(vid)[0] + "_FINAL" + os.path.splitext(vid)[1]}"'
            command = f'ffmpeg -f concat -safe 0 -i {LISTFILE} -c copy {output}'
            print(f'\n****{command}\n')
            result.append(output)
            os.system(command)
    else:
        print(
            'Enter a file name or substring of a file name in the current directory. All files that match will have CL-Intro prepended. _FINAL will be appended to the file name.')
    if os.path.exists(LISTFILE):
        os.remove(LISTFILE)
    res_str = f'Batch operation completed. {len(result)} files created:'
    print('*' * len(res_str))
    print(res_str)
    for file in result:
        print(file)


if __name__ == '__main__':
    main()
