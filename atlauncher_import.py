"""
Li-aung "Lewis" Yip
minecraft@penwatch.net
"""

import xml.etree.ElementTree as element_tree
import os

import unshortenit

from file_handling import fetch_url
from mod_file import Mod_File
from mod_pack import Mod_Pack
import re

URL_BASE = "http://download.nodecdn.net/containers/atl/"


def atlauncher_to_catherder(pack_name, pack_version, download_cache_folder,
                            install_folder):
    # Returns a Mod_Pack object describing the given ATLauncher mod pack.

    # This is exactly what is used in the ATlauncher code.
    # Note \W is shorter, but also includes the underscore. We are trying
    # to exactly match ATLauncher behaviour.
    # Note 2: ATLauncher calls this "getSafeName()".
    sn = re.sub("[^A-Za-z0-9]","",pack_name)
    if pack_name != sn:
        print "INFO - changing pack name {p1} to {p2}.".format(p1=pack_name,p2=sn)
        pack_name = sn

    os.chdir(download_cache_folder)
    config_xml_file_path = fetch_atlauncher_config_xml(pack_name, pack_version)

    # Process Configs.xml and pull out list of files to download.
    tree = element_tree.parse(config_xml_file_path)
    root = tree.getroot()
    mods = root.findall("./mods/mod")
    libs = root.findall("./libraries/library")

    # From config file, pull out minecraft version number (need this for
    # creating 'dependency' folder, i.e. ./mods/1.7.10/.
    minecraft_version = root.find("./pack/minecraft").text

    # Mod_Pack is a parent class which contains a list of Mod_Files.
    mp = Mod_Pack(pack_name, pack_version, download_cache_folder,
                  install_folder, minecraft_version)

    # Config zip is a special file, not included in the modpack's XML
    # description.
    mp.mod_files.append(atlauncher_config_zip(pack_name, pack_version))

    # Build list of mod files that need to be downloaded.
    for mod in mods:
        f = mod_handler(mod, minecraft_version)
        if f is not None:
            mp.mod_files.append(f)

    for lib in libs:
        f = lib_handler(lib)
        if f is not None:
            mp.mod_files.append(f)
    return mp


def mod_lib_handler(xml, mod_or_lib):
    assert mod_or_lib in ("mod", "lib")
    f = Mod_File()
    f['download_url_primary'] = expand_atlauncher_url(xml.attrib['url'],
                                                      xml.attrib['download'])
    f['download_md5'] = xml.attrib['md5']
    f['install_filename'] = xml.attrib['file']

    if mod_or_lib == 'mod':
        f['name'] = xml.attrib['name']
        f['description'] = xml.attrib['description']
    else:
        f['name'] = "A library."
        f['description'] = 'A library.'

    return f


def mod_handler(mod, minecraft_version):
    # See ATLauncher source - java\com\atlauncher\data\Mod.java
    f = mod_lib_handler(mod, 'mod')

    # 'server' attribute may be missing from XML. Default is 'yes'.
    f['required_on_server'] = not ('server' in mod.attrib.keys()
                                   and mod.attrib['server'] == 'no')

    f['required_on_client'] = not ('client' in mod.attrib.keys()
                                   and mod.attrib['client'] == 'no')

    if 'optional' in mod.attrib.keys() and mod.attrib['optional'] == 'yes':
        f['optional?'] = True
        f[
            'install_optional?'] = True  # TODO - replace with question prompt or share code support.
    else:
        f['optional?'] = False
        f[
            'install_optional?'] = True  # No effect, apart from satisfying validate() assert

    install_types_folders = {
        'mods': 'mods/',
        'forge': './',
        'dependency': 'mods/' + minecraft_version + "/",
        'ic2lib': 'mods/ic2/',
        'flan': 'mods/Flan/',  # not tested
        'denlib': 'mods/denlib/',  # not tested
        'plugins': 'plugins/',  # not tested
        'coremods': 'coremods/',  # not tested
        'jarmod': 'jarmods/',  # not tested
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
        if t in ['forge', 'mcpc']:
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
                "WARNING - didn't know what to do with file {f} of type {t} extractto type {e}.".format(
                    f=fn, t=t,
                    e=e))
    else:
        print (
            "WARNING - didn't know what to do with file {f} of type {t}.".format(
                f=fn, t=t))
        return None
    print ('Adding mod {m} to download list - {u}'.format(m=fn, u=url))
    return f


def lib_handler(lib):
    f = mod_lib_handler(lib, 'lib')
    f['optional?'] = False
    f['install_optional?'] = True
    f['install_method'] = 'copy'
    if 'server' in lib.attrib.keys():
        f['required_on_server'] = True
        [dir_path, filename] = os.path.split(
            'libraries/' + lib.attrib['server'])
        f['install_path'] = dir_path

        l = f['install_filename']
        u = f['download_url_primary']
        print (
            'Adding library {l} to download list - {u}'.format(l=l, u=u))
    else:
        f['required_on_server'] = False
    f['required_on_client'] = True
    return f


def fetch_atlauncher_config_xml(pack_name, pack_version):
    config_xml_url = "{u}packs/{pn}/versions/{pv}/Configs.xml".format(
        u=URL_BASE, pn=pack_name, pv=pack_version)
    config_xml_filename = "Configs_{pn}_{pv}.xml".format(pn=pack_name,
                                                         pv=pack_version)
    config_xml_file_path = fetch_url(config_xml_url, config_xml_filename, None)
    return config_xml_file_path


def atlauncher_config_zip(pack_name, pack_version):
    mf = Mod_File()
    mf[
        'download_url_primary'] = "{u}packs/{pn}/versions/{pv}/Configs.zip".format(
        u=URL_BASE, pn=pack_name,
        pv=pack_version)
    mf['install_filename'] = "Configs_{pn}_{pv}.zip".format(pn=pack_name,
                                                            pv=pack_version)
    mf['required_on_server'] = True
    mf['required_on_client'] = True
    mf['name'] = "Configs"
    mf['install_method'] = 'unzip'
    mf['install_path'] = './'
    mf['optional?'] = False
    mf['install_optional?'] = True
    return mf


def expand_atlauncher_url(original_url, download_type):
    if download_type == 'direct':
        return original_url

    elif download_type == 'server':
        # Note, pathname2url for applying percent encoding -
        # "Pams HarvestCraft 1.7.10c.jar" is an example of something that
        # needs percent-encoding.
        return URL_BASE + original_url.replace(' ', '%20')

    elif download_type == 'browser':
        if 'http://adf.ly' in original_url:
            status = unshortenit.unshorten(original_url)
            if status[1] == 200:  # 200 = HTTP OK
                print ('Unshortened {url1} to {url2}.'.format(url1=original_url,
                                                              url2=status[0]))
                return status[0]
            else:
                return 'INVALID ADFLY LINK OR OTHER HTTP ERROR'
        return 'Download file manually'


if __name__ == "__main__":
    atl_pack = atlauncher_to_catherder(pack_name="Bevo's Tech Pack",
                                       pack_version="BTP-11-Full",
                                       download_cache_folder="D:/mc_test/cache-btp",
                                       install_folder="D:/mc_test/install-btp")
    atl_pack.install_server()