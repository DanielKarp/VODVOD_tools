import argparse
import os

CL_INTRO = 'CL-Intro.mp4'
LISTFILE = 'concat_list.txt'


def main():
    result = []
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name',
                        help='The [partial] file name of the video[s] you want to edit')
    parser.add_argument('-n', '--no-summary',
                        action='store_false',
                        dest='summary',
                        help="Don't print a summary after completion")
    parser.add_argument('-s', '--simulate',
                        action='store_true',
                        dest='simulate',
                        help="Simulate calls to ffmpeg (useful for testing or seeing which files would be affected)")
    args = parser.parse_args()

    vids = [file for file in os.listdir(os.curdir) if args.file_name in file]

    for vid in vids:
        with open(LISTFILE, mode='w') as f:
            print('file', CL_INTRO, file=f)
            print('file', f"'{vid}'", file=f)
        output = f'"{os.path.splitext(vid)[0] + "_FINAL" + os.path.splitext(vid)[1]}"'
        command = f'ffmpeg -f concat -safe 0 -i {LISTFILE} -c copy {output}'
        print(f'\n**** {command}')
        result.append(output)
        if args.simulate:
            print('* some ffmpeg output *\n'*5)
        else:
            os.system(command)

    if os.path.exists(LISTFILE):
        os.remove(LISTFILE)
    if args.summary:
        print_summary(result, args.simulate)


def print_summary(result, sim):
    res_str = f'{"SIMULATED " if sim else ""}Batch operation completed. \
{len(result)} files {"would have been " if sim else ""}created:'
    sep = '*' * len(res_str)
    print(sep)
    print(res_str)
    print(sep)
    for file in result:
        print(file.strip('"'))
    print(sep)


if __name__ == '__main__':
    main()
