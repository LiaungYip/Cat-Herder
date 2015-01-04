# -*- coding: utf-8 -*-
"""
Li-aung "Lewis" Yip
minecraft@penwatch.net

Requires:
    plac (command line argument parsing)
"""

STARTUP_SCRIPT_TEMPLATE = """#!/bin/bash
java -Xmx2G -XX:MaxPermSize=256M -jar {fn} nogui"""


def main(arg1):
    print arg1

# Command line argument parsing by 'plac'
if __name__ == '__main__':
    import plac

    plac.call(main)
