#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Li-aung "Lewis" Yip
minecraft@penwatch.net

Requires:
    plac (command line argument parsing)
    unshortenit (adf.ly resolving)
"""

STARTUP_SCRIPT_TEMPLATE = """#!/bin/bash
java -Xmx2G -XX:MaxPermSize=256M -jar {fn} nogui"""

import os
import json
from operator import itemgetter

import plac

from file_handling import mkdir, fetch_url
from atlauncher_import import atlauncher_to_catherder


def get_pack_json():
    url = "http://download.nodecdn.net/containers/atl/launcher/json/packs.json"
    print ("Grabbing new copy of packs.json from {u}".format(u=url))
    fetch_url(url,'packs.json',None)
    with open('packs.json', 'r') as f:
        packs_json = json.load(f)
    return packs_json

def list_packs(packs_json):
    packs_json.sort(key=itemgetter('position'))
    print(u"{:^38}| {:^19}| {:^19}\r\n{:-<80}".format('Pack Name', 'Latest Version', 'Latest Dev Version', ''))
    for pack in packs_json:
        n = pack['name']
        lv = ''
        if pack['versions']:
            lv = pack['versions'][0]['version']
        ldv = ''
        if pack['devVersions']:
            ldv = pack['devVersions'][0]['version']
        print(u"{name:<38}| {latest_version:<19}| {latest_dev_version:<19}".format(name=n, latest_version=lv,
                                                                                   latest_dev_version=ldv))


@plac.annotations(
    operation=("Operation to perform", "positional", None, str, ['install', 'update', 'list_packs']),
    pack_name=("Name of pack, i.e. 'BevosTechPack' - try 'list_packs' for list of pack names", 'option', 'p'),
    pack_version=("Version of pack, i.e. 'BTP-11-Full' - defaults to latest available version", 'option', 'v'),
    install_folder=(
    "Folder where server will be installed - defaults to './install/$pack_name/$pack_version'", 'option', 'i'),
    cache_folder=("Folder where downloaded files will be cached - defaults to './cache'", 'option', 'c'),
    dry_run=("Perform a dry run (don't download any mod files or install anything)", 'flag', 'd')
)
def main(operation, pack_name, pack_version, install_folder, cache_folder, dry_run):
    """A tool for installing and updating Minecraft servers based on ATLauncher mod packs.
    Example invocation:

    cat_herder.py install -p BevosTechPack -v BTP-11-Full -c /home/mc/cache -i /home/mc/install/"""

    if install_folder:
        install_folder = os.path.realpath(install_folder)
    else:
        install_folder = os.path.realpath('./install/{pn}/{pv}'.format(pn=pack_name,pv=pack_version))

    if cache_folder:
        cache_folder = os.path.realpath(cache_folder)
    else:
        cache_folder = os.path.realpath('./cache/')

    os.chdir(cache_folder)
    packs_json = get_pack_json()

    pack_names = [p['name'] for p in packs_json]

    # import pprint; pprint.pprint(packs_json)

    if operation == 'list_packs':
        list_packs(packs_json)

    if operation == 'update':
        print "Update not implemented yet."

    if operation == 'install':
        mp = atlauncher_to_catherder(pack_name, pack_version, cache_folder, install_folder)
        if dry_run:
            pass
        else:
            mp.install_server()

if __name__ == '__main__':
    plac.call(main)
