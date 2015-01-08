"""
Li-aung "Lewis" Yip
minecraft@penwatch.net
"""

import xml.etree.ElementTree as ET
import os

import unshortenit

from file_handling import fetch_url
from mod_file import Mod_File
from mod_pack import Mod_Pack


URL_BASE = "http://download.nodecdn.net/containers/atl/"


def atlauncher_to_catherder(pack_name, pack_version, download_cache_folder, install_folder):
    os.chdir(download_cache_folder)
    config_xml_file_path = fetch_atlauncher_config_xml(pack_name, pack_version)

    # Process Configs.xml and pull out list of files to download.
    tree = ET.parse(config_xml_file_path)
    root = tree.getroot()
    mods = root.findall("./mods/mod")
    libs = root.findall("./libraries/library")

    # From config file, pull out minecraft version number (need this for creating 'dependency' folder, i.e. ./mods/1.7.10/.
    minecraft_version = root.find("./pack/minecraft").text

    mp = Mod_Pack(pack_name, pack_version, download_cache_folder, install_folder, minecraft_version)



    # Build list of mod files that need to be downloaded.
    for mod in mods:
        f = Mod_File()

        if 'server' in mod.attrib.keys() and mod.attrib['server'] == 'no':
            f['required_on_server'] = False
        else:
            f['required_on_server'] = True

        f['name'] = mod.attrib['name']
        f['download_url_primary'] = expand_atlauncher_url(mod.attrib['url'], mod.attrib['download'])
        f['download_md5'] = mod.attrib['md5']
        f['install_filename'] = mod.attrib['file']
        f['required_on_client'] = True
        f['description'] = mod.attrib['description']

        install_types_folders = {
            'mods': 'mods/',
            'forge': './',
            'dependency': 'mods/' + mp['minecraft_version'] + "/",
            'ic2lib': 'mods/ic2/',
            'flan': 'mods/Flan/',  # not tested
            'denlib': 'mods/denlib/',  # not tested
            'plugins': 'plugins/',  # not tested
            'coremods': 'coremods/',  # not tested
            'jarmod': 'jarmods/',  #not tested
            'disabled': 'disabledmods/',  #not tested
            'bin': 'bin/',  #not tested
            'natives': 'natives/'  #not tested
        }

        t = mod.attrib['type']
        fn = f['install_filename']
        url = f['download_url_primary']

        if t in install_types_folders.keys():
            f['install_method'] = 'copy'
            f['install_path'] = install_types_folders[t]
            if t in ['forge','mcpc']:
                f['special_actions'] = 'create_run_sh'
        elif t == 'extract':
            f['install_method'] = 'unzip'
            e = mod.attrib['extractto']
            if e == 'root':
                f['install_path'] = './'
            elif e == 'mods':
                f['install_path'] = 'mods/'
            else:
                print (
                    "WARNING - didn't know what to do with file {f} of type {t} extractto type {e}.".format(f=fn, t=t,
                                                                                                            e=e))
        else:
            print ("WARNING - didn't know what to do with file {f} of type {t}.".format(f=fn, t=t))
            continue
        print ('Adding mod {m} to download list - {u}'.format(m=fn, u=url))
        mp.mod_files.append(f)

    for lib in libs:
        # print lib.attrib

        f = Mod_File()

        # TODO - clean up common code with 'mod' loop above.
        f['download_url_primary'] = expand_atlauncher_url(lib.attrib['url'], lib.attrib['download'])

        f['download_md5'] = lib.attrib['md5']
        f['install_filename'] = lib.attrib['file']
        f['name'] = 'a library'
        f['install_method'] = 'copy'
        f['description'] = 'Library.'
        if 'server' in lib.attrib.keys():
            f['required_on_server'] = True
            # noinspection PyUnusedLocal
            [dir_path, filename] = os.path.split('libraries/' + lib.attrib['server'])
            f['install_path'] = dir_path
            print (
                'Adding library {l} to download list - {u}'.format(l=f['install_filename'],
                                                                   u=f['download_url_primary']))
        else:
            f['required_on_server'] = False
            print ("Library {l} had no 'server' attribute - assuming it's only required on clients - skipping.".format(
                l=f['install_filename']))
            continue
        f['required_on_client'] = True
        mp.mod_files.append(f)

    mp.mod_files.append(atlauncher_config_zip(pack_name, pack_version))

    return mp

def fetch_atlauncher_config_xml(pack_name, pack_version):
    config_xml_url = "{u}packs/{pn}/versions/{pv}/Configs.xml".format(u=URL_BASE, pn=pack_name, pv=pack_version)
    config_xml_filename = "Configs_{pn}_{pv}.xml".format(pn=pack_name, pv=pack_version)
    config_xml_file_path = fetch_url(config_xml_url, config_xml_filename, None)
    return config_xml_file_path


def atlauncher_config_zip(pack_name, pack_version):
    mf = Mod_File()
    mf['download_url_primary'] = "{u}packs/{pn}/versions/{pv}/Configs.zip".format(u=URL_BASE, pn=pack_name,
                                                                                  pv=pack_version)
    mf['install_filename'] = "Configs_{pn}_{pv}.zip".format(pn=pack_name, pv=pack_version)
    mf['required_on_server'] = True
    mf['required_on_client'] = True
    mf['name'] = "Configs"
    mf['install_method'] = 'unzip'
    mf['install_path'] = './'
    return mf


def expand_atlauncher_url(original_url, download_type):
    if download_type == 'direct':
        return original_url
    elif download_type == 'server':
        # Note, pathname2url for applying percent encoding - "Pams HarvestCraft 1.7.10c.jar" is an example of something that needs percent-encoding.
        # return URL_BASE + urllib.pathname2url(original_url)
        return URL_BASE + original_url.replace(' ', '%20')
    elif download_type == 'browser':
        if 'http://adf.ly' in original_url:
            status = unshortenit.unshorten(original_url)
            if status[1] == 200:  # 200 = HTTP OK
                print ('Unshortened {url1} to {url2}.'.format(url1=original_url, url2=status[0]))
                return status[0]
            else:
                return 'INVALID ADFLY LINK OR OTHER HTTP ERROR'
        return 'Download file manually'

if __name__ == "__main__":
    atl_pack = atlauncher_to_catherder(pack_name="BevosTechPack", pack_version="BTP-11-Full",
                                 download_cache_folder="D:/ATLauncher_Hacking/cache/",
                                 install_folder="D:/ATLauncher_Hacking/install/")
    atl_pack.install_server()