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
import re

import plac

from file_handling import mkdir, fetch_url
from atlauncher_import import atlauncher_to_catherder
from atlauncher_share_code import get_mod_pack_with_share_code

def safe_name (dirty):
    return re.sub('[^A-Za-z0-9]','',dirty)

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

def get_latest_pack_version(packs_json, pack_name):
    safe_pack_name = safe_name (pack_name)
    for pack in packs_json:
        if safe_name(pack['name']) == safe_pack_name:
            if pack['versions']:
                lv = pack['versions'][0]['version']
                return lv
            else:
                return None
    raise KeyError("Pack name {P} ({S}) not found in packs.json.").format(
        P = pack_name, S = safe_name )


@plac.annotations(
    operation=("Operation to perform", "positional", None, str, ['install', 'update', 'list_packs', 'install-from-share-code']),
    pack_name=("Name of pack, i.e. 'BevosTechPack' - try 'list_packs' for list of pack names", 'option', 'p'),
    pack_version=("Version of pack, i.e. 'BTP-11-Full' - defaults to latest available version", 'option', 'v'),
    install_folder=("Folder where server will be installed - defaults to './install/$pack_name/$pack_version'", 'option', 'i'),
    cache_folder=("Folder where downloaded files will be cached - defaults to './cache'", 'option', 'c'),
    share_code=("Share code - required for 'install-from-share-code'.", 'option', 's'),
    dry_run=("Perform a dry run. Lists what would be downloaded and installed, but doesn't actually download or install anything.", 'flag', 'd')
)
def main(operation, pack_name, pack_version, install_folder, cache_folder, share_code, dry_run):
    """A tool for installing and updating Minecraft servers based on ATLauncher mod packs.
    Example invocations:

    cat_herder.py list_packs

    Installing with share code:
    cat_herder.py install-from-share-code -s QtDNnlfZ

    As above, but manually specifying the download cache and server install folders:
    cat_herder.py install-from-share-code -s QtDNnlfZ -c /home/mc/cache -i /home/mc/install/

    Installing with manually specified pack name and pack version:
    cat_herder.py install -p BevosTechPack -v BTP-11-Full -c /home/mc/cache -i /home/mc/install/
    """

    if install_folder:
        install_folder = os.path.realpath(install_folder)
    else:
        install_folder = os.path.realpath('./install/{pn}/{pv}'.format(pn=pack_name,pv=pack_version))

    if cache_folder:
        cache_folder = os.path.realpath(cache_folder)
    else:
        cache_folder = os.path.realpath('./cache/')

    mkdir (cache_folder)
    os.chdir(cache_folder)
    packs_json = get_pack_json()

    pack_names = [p['name'] for p in packs_json]

    if operation == 'list_packs':
        list_packs(packs_json)

    if operation == 'update':
        print "Update not implemented yet."

    if operation == 'install':
        if not pack_version:
            pack_version = get_latest_pack_version (packs_json, pack_name)

        mp = atlauncher_to_catherder(pack_name, pack_version, cache_folder, install_folder)
        if dry_run:
            mp.print_mod_files_list()
        else:
            mp.install_server()

    if operation == 'install-from-share-code':
        if not share_code:
            print ("install-from-share-code option requires a share code to be specified using the -s option.")
        if not re.match("[A-Za-z0-9]{8}",share_code):
            print ("install-from-share-code requires an 8-character alphanumeric share code.")

        mp = get_mod_pack_with_share_code(share_code, cache_folder, install_folder)
        if dry_run:
            mp.print_mod_files_list()
        else:
            mp.install_server()

if __name__ == '__main__':
    plac.call(main)
