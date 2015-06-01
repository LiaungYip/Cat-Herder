"""
Li-aung "Lewis" Yip
minecraft@penwatch.net
"""

import urllib2
import re
import json
from atlauncher_import import atlauncher_to_catherder

def get_share_code_json (share_code):
    assert re.match("[A-Za-z0-9]{8}", share_code)
    url = "https://api.atlauncher.com/v1/share-codes/" + share_code
    try:
        d = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        if e.code == 404:
            print "ERROR - HTTP 404 while retrieving share code - {u}".format(u = url)
            raise

    j = d.read()
    d.close()
    return j

def process_share_code_json (json_string):
    # Returns a dict of 'pack', 'pack_version', and 'selected_mods'.
    # 'selected_mods' is a list of the optional mods to be installed.

    json_data = json.loads(json_string)

    assert json_data['error'] == False
    assert json_data['code'] == 200 # OK

    # Note that the /data/mods/ node of the json_data itself contains JSON.
    # It's JSON all the way down, man.
    json_mods_data = json.loads(json_data['data']['mods'])
    optional_mods = json_mods_data['optional']
    selected_mods = [m['name'] for m in optional_mods if m['selected'] == True]

    return dict (pack = json_data['data']['pack'],
                 pack_version = json_data['data']['version'],
                 selected_mods = selected_mods)

def get_mod_pack_with_share_code (share_code, download_cache_folder, install_folder):
    # Returns a Mod_Pack object.
    #
    # The pack name and pack version are implied by the share code, so these
    # don't have to be provided externally.
    #
    # The 'install_optional?' flag is set on each of the Mod_Pack's
    # optional mods, based on the 'selected' mods in the share code data.
    sc_json_str = get_share_code_json (share_code)
    r = process_share_code_json (sc_json_str)

    mp = atlauncher_to_catherder(pack_name = r['pack'],
                                 pack_version = r['pack_version'],
                                 download_cache_folder=download_cache_folder,
                                 install_folder=install_folder)

    for m in mp.mod_files:
        if m['optional?']:
            m['install_optional?'] = m['name'] in r['selected_mods']
    return mp