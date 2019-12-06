#!/usr/bin/env python3

import sys
import pwresource

def check():
    print (pwresource.PWResource(sys.stdin.read()).cmd_check())

def input():
    print (pwresource.PWResource(sys.stdin.read()).cmd_in(sys.argv[1]))

def output():
    print("TODO: implement out", file=sys.stderr)


