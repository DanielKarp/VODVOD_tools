# bulk rename files
__author__ = 'Daniel Karpelevitch (dkarpele)'
__version__ = '0.1'

import argparse
import os

import cutie


def main():
    args = get_args()
    search_str, append_str, prepend_str = args.file_name, args.append, args.prepend
    interactive, verbose, summary, simulate = args.interactive, args.verbose, args.summary, args.simulate
    if not (prepend_str and append_str) and not interactive:
        print('You have not selected text to prepend nor append. use -i or --interactive to be prompted for input')
        return None
    search_str = search_str or input('Enter string to search for that is shared by all the files you want to change: ')
    if not append_str and interactive:
        append_str = input('Enter string to add to end of name (example: "_FINAL"). leave blank for none: ')
    if not prepend_str and interactive:
        prepend_str = input('Enter string to add to start of name (example: "BRKSEC-1234-"). leave blank for none: ')
    if not verbose and interactive:
        verbose = cutie.prompt_yes_or_no('Enable verbose output?')
    if not summary and interactive:
        summary = cutie.prompt_yes_or_no('Enable summary output?')
    if not simulate and interactive:
        simulate = cutie.prompt_yes_or_no('Enable simulated mode? (no changes will be made)')
    result = []
    files = [file for file in os.listdir(os.curdir) if search_str in file]
    if verbose:
        verbose_intro(files)
    for old_name in files:  # loop through all files in the current directory
        if search_str in old_name:  # only operate on files that contain the search string
            try:
                new_name = prepend_str + old_name[:-4] + append_str + old_name[-4:]
                if not simulate:
                    os.rename(old_name, new_name)  # os.rename(old, new)
                if verbose:
                    print(f'* renamed {old_name} to {new_name}')  # output to console
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
    parser.add_argument('-i', '--interactive', action='store_true', dest='interactive',
                        help='Run the program interactively (ask for the file name and text to be added one by one)')
    parser.add_argument('-f', '--file_name', dest='file_name',
                        help='The [partial] file name of the video[s] you want to rename')
    parser.add_argument('-p', '--prepend', dest='prepend',
                        help='The text to be concatenated to the start of matching files (optional)')
    parser.add_argument('-a', '--append', dest='append',
                        help='The text to be concatenated to the end of matching files (optional)')
    return parser.parse_args()


def print_summary(result, sim):
    res_str = f'{"SIMULATED b" if sim else "B"}atch operation completed. \
{len(result)} files {"would" if sim else "should"} have been renamed:'
    separator = '*' * len(res_str)
    print(separator, res_str, separator, sep='\n')
    for file in result:
        print(file.strip('"'))
    print(separator)


def verbose_intro(files):
    print('* found files:')
    for file in files:
        print('*', file)
    print()


if __name__ == '__main__':
    main()
