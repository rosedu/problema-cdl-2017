#!/bin/python3

import os
import shutil
from subprocess import call


def print_test_line(test, score, line_width=50):
    dots = '.' * (line_width - 2 - len(test) - len(str(score)))

    line = '[{test}]{dots}{score}'.format(test=test,
                                          dots=dots,
                                          score=score)

    print(line)


executable_name = './log_stats'

tests = [
    ('tests/test0.log',),
    ('tests/test1.log',),
    ('tests/test2.log',),
    ('tests/test3.log',),
    ('tests/test4.log', '--interval', '2'),
    ('tests/test5.log', '--interval', '5'),
    ('tests/test6.log', '--interval', '60'),
    ('tests/test7.log', '--interval', '2', '--start', '2016-01-18T12:23'),
    ('tests/test8.log', '--interval', '5', '--end', '2016-11-21T04:52'),
    ('tests/test9.log', '--interval', '60', '--start', '2016-04-11T08:37', '--end', '2017-03-14T14:06'),
    ('tests/test10.log', '--interval', '30', '--success', '20x,3xx,404'),
]


for directory in ('output', 'diffs'):
    if os.path.exists(directory):
        shutil.rmtree(directory)

    os.mkdir(directory)


if not os.path.exists('reference'):
    print('ERROR: Reference directory does not exist')
    exit(-1)


total_score = 0

for test in tests:
    out_file = (test[0].replace('tests', 'output')
                       .replace('log', 'out'))

    with open(out_file, 'w') as f:
        call(['gtimeout', '30', executable_name] + list(test),
             stdout=f)

    ref_file = (test[0].replace('tests', 'reference')
                       .replace('log', 'ref'))

    diff_file = (test[0].replace('tests', 'diffs')
                        .replace('log', 'diff'))

    with open(diff_file, 'w') as f:
        call(['diff', out_file, ref_file], stdout=f)

    with open(diff_file, 'r') as f:
        score = 10 if not f.read() else 0

        total_score += score

        print_test_line(test[0], score)


print_test_line('TOTAL', str(total_score) +'/110')
