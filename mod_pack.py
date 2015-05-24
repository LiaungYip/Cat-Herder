import os

from file_handling import mkdir
from mod_file import Mod_File


class Mod_Pack(dict):
    attribs = sorted(('pack_name',
                      'pack_version',
                      'download_cache_folder',
                      'install_folder',
                      'minecraft_version'))

    def __init__(self, pack_name, pack_version, download_cache_folder, install_folder, minecraft_version):
        for a in self.attribs:
            self[a] = None
        self.mod_files = list()
        self['pack_name'] = pack_name
        self['pack_version'] = pack_version
        self['download_cache_folder'] = download_cache_folder
        self['install_folder'] = install_folder
        self['minecraft_version'] = minecraft_version

    def install_server(self):
        self.mod_files.append(self.minecraft_server_jar())

        for f in self.mod_files:
            if not f['required_on_server']:
                # pass
                continue

            try:
                f.validate_attributes()
            except AssertionError:
                print ("INSTALLATION FAILED - MOD FILE DEFINITION INVALID.")
                import pprint

                pprint.pprint(f)
                return 'FAILURE'

            print ('-')
            mkdir(self['download_cache_folder'])
            os.chdir(self['download_cache_folder'])
            f.download("server")
            mkdir(self['install_folder'])
            os.chdir(self['install_folder'])
            f.install(self, "server")

        print ('-\r\nWriting eula.txt')
        os.chdir(self['install_folder'])
        with open('eula.txt', 'w') as eula:
            eula.write("eula=true")


    def minecraft_server_jar(self):
        ver = self['minecraft_version']
        mf = Mod_File()
        mf[
            'download_url_primary'] = "http://s3.amazonaws.com/Minecraft.Download/versions/{v}/minecraft_server.{v}.jar".format(
            v=ver)
        mf['install_filename'] = 'minecraft_server.{v}.jar'.format(v=ver)
        mf['required_on_server'] = True
        mf['required_on_client'] = False
        mf['name'] = "Minecraft Server Jar"
        mf['install_method'] = 'copy'
        mf['install_path'] = './'
        mf['optional?'] = False
        mf['install_optional?'] = True
        return mf