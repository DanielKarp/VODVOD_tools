__author__ = 'Daniel Karpelevitch (dkarpele)'
__version__ = '0.1'

import argparse
import os


def finalize():
    args = get_args()
    search_str, ignore_str, append_str, prepend_str = args.search, args.ignore, args.append, args.prepend
    verbose, summary, simulate = args.verbose, args.summary, args.simulate
    result = []
    files = [file for file in os.listdir(os.curdir) if search_str in file and ignore_str not in file]
    if not files:
        print('no files found')
        return
    if verbose:
        verbose_intro(files)
    for old_name in files:  # loop through all files in the current directory
        try:
            old_base, ext = os.path.splitext(old_name)
            new_name = prepend_str + old_base + append_str + ext
            if not simulate:
                os.replace(old_name, new_name)  # os.finalize(old, new)
            if verbose:
                print(f'renamed {old_name} to {new_name}')  # output to console
        except Exception as e:
            if verbose:
                print(f'*    there was was an error renaming {old_name}')
                print('*   ', e)
            result.append(f'{old_name} was not renamed due to an error')
        else:
            result.append(new_name)
    if summary:
        print_summary(result, simulate)


def get_args():
    parser = argparse.ArgumentParser(description='A tool to automate renaming files. ' +
                                                 'Append or prepend text to all matching files.' +
                                                 'Only works on files in the current directory.',
                                     epilog=f'Written by {__author__}')
    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s ({__version__})")
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                        help='Enable verbose output')
    parser.add_argument('-s', '--summary', action='store_true', dest='summary',
                        help="Print a summary after completion")
    parser.add_argument('-S', '--simulate', action='store_true', dest='simulate',
                        help="Simulate renaming (useful for testing or seeing which files would be affected)")
    parser.add_argument('search',
                        help='The search string that files will be compared against (default is ".mp4")',
                        nargs='?', default='.mp4')
    parser.add_argument('-i', '--ignore', dest='ignore',
                        help='Files that match this string will be ignored\n'
                             '(optional, default is "_FINAL", use -i with no argument to not ignore any matched files)',
                        nargs='?', const='', default='_FINAL')
    parser.add_argument('-p', '--prepend', dest='prepend',
                        help='The text to be concatenated to the start of matching files (optional)',
                        nargs='?', const='', default='')
    parser.add_argument('-a', '--append', dest='append',
                        help='The text to be concatenated to the end of matching files\n'
                             '(optional, default is "_FINAL")',
                        nargs='?', const='', default='_FINAL')
    return parser.parse_args()


def print_summary(result, sim):
    res_str = f'{"SIMULATED b" if sim else "B"}atch operation completed. \
{len(result)} files {"would" if sim else "should"} have been renamed:'
    separator = '*' * len(res_str)
    print(separator, res_str, separator, sep='\n')
    for file in result:
        print(file)
    print(separator)


def verbose_intro(files):
    print('* found files:')
    for file in files:
        print(file)
    print('* starting...')


if __name__ == '__main__':
    finalize()
