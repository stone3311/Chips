"""
Using instructions and simulation profiles, generate reports and statistics.
"""

__author__ = "Jon Dawson"
__copyright__ = "Copyright (C) 2015, Jonathan P Dawson"
__version__ = "0.1"

import operator


def code_lines(filename, instructions):

    codelines = []
    for instruction in instructions:
        trace = instruction["trace"]
        if trace.filename == filename:
            codelines.append(trace.lineno)
    return list(set(codelines))


def code_files(instructions):

    return set([i["trace"].filename for i in instructions])


def report_coverage(files, instructions):

    print("filename".ljust(100), end=' ')
    print("code".center(10), end=' ')
    print("executed".center(10), end=' ')
    print("percent".center(10))
    print(''.join(["=" for i in range(100)]), end=' ')
    print(''.join(["=" for i in range(10)]), end=' ')
    print(''.join(["=" for i in range(10)]), end=' ')
    print(''.join(["=" for i in range(10)]))

    for filename in sorted(code_files(instructions)):
        lines = files.get(filename, {})
        included = len(code_lines(filename, instructions))
        executed = len(lines)

        print(filename.ljust(100), end=' ')
        print(str(included).center(10), end=' ')
        print(str(executed).center(10), end=' ')
        print(100.0 * float(executed) / float(included))


def report_profile(files, instructions):

    print("filename".ljust(100), end=' ')
    print("line".center(10), end=' ')
    print("percent".center(10))
    print(''.join(["=" for i in range(100)]), end=' ')
    print(''.join(["=" for i in range(10)]), end=' ')
    print(''.join(["=" for i in range(10)]))

    total = 0
    for filename in sorted(code_files(instructions)):
        lines = files.get(filename, {})
        for lines, count in lines.items():
            total += count

    for filename in sorted(code_files(instructions)):
        lines = files.get(filename, {})
        for line, count in sorted(
            list(lines.items()), key=operator.itemgetter(1), reverse=True
        ):
            print(filename.ljust(100), end=' ')
            print(str(line).center(10), end=' ')
            print(100.0 * float(count) / float(total))


def annotate_coverage(filename, files, instructions):
    lines = files.get(filename, {})
    source = open(filename)
    included = code_lines(filename, instructions)

    print(filename, ":\n")
    for lineno, line in enumerate(source):
        print(lineno, end=' ')
        if lineno + 1 in lines:
            print(">", end=' ')
        else:
            if lineno + 1 in included:
                print("!", end=' ')
            else:
                print("-", end=' ')
        print(line.rstrip())

    source.close()
