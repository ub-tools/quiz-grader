#!/usr/bin/python

from __future__ import print_function

import sys
import json

printscores = False
studentfile = 'quiz_results.json'

i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '-A':
        printscores = True
    elif arg == '-f':
        i += 1
        studentfile = sys.argv[i]
    else:
        print("usage: %s [-A] [-f inputfile]" % sys.argv[0], file=sys.stderr)
        sys.exit(-1)

    i += 1

with file('key.json', 'r') as f:
    key = json.load(f)

with file(studentfile, 'r') as f:
    results = json.load(f)


if not 'version' in results or results['version'] != key['version']:
    print('The submitted quiz results are from a different version of this quiz.')
    print('Please re-take the quiz following the link provided by your instructor!')
    if printscores:
        print('{"scores":{"Total":0}}')
    sys.exit(0)

key.pop('version')

total = 0
missed = []

def miss_str(v):
    return "q. %d: %s" % (v['question'], v['description'])

for k, v in iter(sorted(key.iteritems(), key=lambda x: x[1]['question'])):
    if not k in results:
        missed.append(miss_str(v))
        continue
    
    if isinstance(results[k], list):
        results[k].sort
        if results[k] != v['value']:
            missed.append(miss_str(v))
            continue
    elif isinstance(results[k], str) or isinstance(results[k], unicode):
        if results[k] != v['value']:
            missed.append(miss_str(v))
            continue
    else:
        missed.append(miss_str(v))
        continue

    total += 1

if len(missed) > 0:
    print("You missed some questions.  You may want to look at the following documentation:")
    print("")
    for str in missed:
        print(" * %s" % str)

if printscores:
    print("""{"scores":{"Total":%d}}""" % total)
    
