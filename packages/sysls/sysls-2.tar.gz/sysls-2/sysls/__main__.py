#!/usr/bin/env python3
import glob
import os
import errno
import argparse


def list(path, prefix=None):
    q = os.path.join(path, '*')
    namelen = 0
    dirs = []
    files = []
    if prefix is None:
        prefix = ''
    for file in glob.glob(q):
        namelen = max(namelen, len(prefix + file.replace(path, '')))
        if os.path.isdir(file):
            dirs.append(file)
        else:
            files.append(file)

    for file in sorted(dirs) + sorted(files):
        if file.endswith('uevent'):
            continue

        name = prefix + file[len(path):]

        if not os.path.isfile(file):
            print(name)
            continue

        display = name.ljust(namelen + 2, '.')
        try:
            with open(file, 'r') as handle:
                data = handle.read().strip()
            print(display, data)
        except OSError as e:
            if e.errno in errno.errorcode:
                print(display, f'[-{errno.errorcode[e.errno]}]')
            else:
                print(display, e)
        except UnicodeDecodeError as e:
            print(display, "[ Unprintable data ]")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', help='Directory to open')
    parser.add_argument('--inline', '-i', action='store_true',
                        help='Display an inline prefix when using multiple paths')
    args = parser.parse_args()
    if len(args.path) == 0:
        list('.')
    elif len(args.path) == 1:
        list(args.path[0])
    else:
        if args.inline:
            prefix = os.path.commonprefix(args.path)
            for path in args.path:
                list(path, prefix=path[len(prefix):])
                print()
        else:
            for path in args.path:
                print(f'[{path}]')
                list(path)
                print()


if __name__ == '__main__':
    main()
