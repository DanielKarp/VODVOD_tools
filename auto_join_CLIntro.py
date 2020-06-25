__author__ = 'Daniel Karpelevitch (dkarpele)'
__version__ = '0.1'
import argparse
import os
CL_INTRO = 'CL-Intro.mp4'
LISTFILE = 'concat_list.txt'


def main():
    result = []
    args = setup_parser()
    vids = [file for file in os.listdir(os.curdir) if args.file_name in file]
    if args.verbose:
        verbose_intro(vids)
    for vid in vids:
        with open(LISTFILE, mode='w') as f:
            print('file', CL_INTRO, file=f)
            print('file', f"'{vid}'", file=f)
        output_filename, command = make_command(vid)
        if args.verbose:
            verbose_list(vid, command)
        result.append(output_filename)
        if args.simulate:
            if args.verbose:
                print('- some ffmpeg output -\n' * 4)
        else:
            os.system(command)
    if os.path.exists(LISTFILE):
        os.remove(LISTFILE)
        if args.verbose:
            verbose_delete_list()
    if args.summary:
        print_summary(result, args.simulate)


def setup_parser():
    parser = argparse.ArgumentParser(description='A tool to automate joining CL-Intro.mp4 to a clip or clips.',
                                     epilog=f'Written by {__author__}')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s ({__version__})")
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Enable verbose output')
    parser.add_argument('-s', '--summary', action='store_true', dest='summary',
                        help="Print a summary after completion")
    parser.add_argument('-S', '--simulate', action='store_true', dest='simulate',
                        help="Simulate calls to ffmpeg (useful for testing or seeing which files would be affected)")
    parser.add_argument('file_name', help='The [partial] file name of the video[s] you want to edit')
    return parser.parse_args()


def make_command(vid):
    output_filename = f'"{os.path.splitext(vid)[0] + "_FINAL" + os.path.splitext(vid)[1]}"'
    command = f'ffmpeg -f concat -safe 0 -i {LISTFILE} -c copy {output_filename}'
    return output_filename, command


def print_summary(result, sim):
    res_str = f'{"SIMULATED b" if sim else "B"}atch operation completed. \
{len(result)} files {"would" if sim else "should"} have been created:'
    separator = '*' * len(res_str)
    print(separator, res_str, separator, sep='\n')
    for file in result:
        print(file.strip('"'))
    print(separator)


def verbose_intro(vids):
    print('* found files:')
    for vid in vids:
        print('*', vid)
    print()


def verbose_list(vid, command):
    print(f'* overwriting {LISTFILE} with the following:')
    print('** file', CL_INTRO)
    print('** file', f"'{vid}'")
    print(f'* executing: {command}')


def verbose_delete_list():
    print(f'* deleting {LISTFILE}')


if __name__ == '__main__':
    main()
