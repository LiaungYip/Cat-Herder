from zipfile import ZipFile
import shutil
import os.path

from file_handling import fetch_url, mkdir

STARTUP_SCRIPT_TEMPLATE = """#!/bin/bash
java -Xmx2G -XX:MaxPermSize=256M -jar {fn} nogui"""

class Mod_File(dict):
    attribs = sorted(('name',
                      'description',
                      'required_on_server',
                      'required_on_client',
                      'download_url_primary',
                      'download_url_secondary',
                      'download_md5',
                      'install_method',
                      'install_path',
                      'install_filename',
                      'special_actions',
                      'comments',
                      'optional?',
                      'install_optional?'))

    def __init__(self, **kwargs):
        super(Mod_File, self).__init__(**kwargs)
        for a in self.attribs:
            self[a] = None



    def download(self, server_or_client):
        assert server_or_client in ("server","client")
        if not self.selected_for_install(server_or_client):
            print "Skipping {f} (optional or not required on {sc}).".format(f=self['install_filename'], sc=server_or_client)
            return

        if self['download_url_primary'] == "Download file manually":
            print "Not installing {f} automatically. Download it manually if you need it.".format(f=self['install_filename'])
            return
        self.validate_attributes()
        print ("Downloading {f} from {u}".format(f=self['install_filename'], u=self['download_url_primary']))
        fetch_url(self['download_url_primary'], self['install_filename'], self['download_md5'])



    def install(self, mod_pack, server_or_client):
        assert server_or_client in ("server","client")
        if not self.selected_for_install(server_or_client):
            print "Skipping {f} (optional or not required on {sc}).".format(f=self['install_filename'], sc=server_or_client)
            return

        if self['download_url_primary'] == "Download file manually":
            print "Not installing {f} automatically. Download it manually if you need it.".format(f=self['install_filename'])
            return
        self.validate_attributes()
        inst_path = os.path.join(mod_pack['install_folder'], self['install_path'])
        src_path = os.path.join(mod_pack['download_cache_folder'], self['install_filename'])
        mkdir(inst_path)
        if self['install_method'] == 'copy':
            print ("Installing {f} by copying to {d}".format(f=src_path, d=inst_path))
            shutil.copy(src_path, inst_path)
        elif self['install_method'] == 'unzip':
            with ZipFile(src_path, 'r') as z:
                print ("Installing {f} by unzipping to {d}".format(f=src_path, d=inst_path))
                z.extractall(inst_path)

        if self['special_actions'] == 'create_run_sh':
            if 'forge' in self['install_filename']:
                script_name = 'start_forge_server.sh'
            elif 'cauldron' in self['install_filename']:
                script_name = 'start_cauldron_server.sh'
            else:
                raise ValueError
            script = STARTUP_SCRIPT_TEMPLATE.format(fn=self['install_filename'])
            script_path = os.path.join(mod_pack['install_folder'],script_name)
            with open(script_path, 'w') as fh:
                fh.write(script)

    def selected_for_install (self, server_or_client = "server"):
        # Returns true if the file should be downloaded and installed.
        assert server_or_client in ("server","client")
        self.validate_attributes()
        if server_or_client == "server" and not (self['required_on_server']):
            return False

        if server_or_client == "client" and not (self['required_on_client']):
            return False

        if self['install_optional?']:
            return True

        return False

    def validate_attributes(self):
        assert sorted(self.keys()) == self.attribs  # Check no extra attributes added
        assert self['name'] is not None
        assert self['download_url_primary'] is not None
        assert self['required_on_server'] in (True, False)
        assert self['required_on_client'] in (True, False)
        assert self['install_method'] in ('copy', 'unzip')
        assert self['install_path'] is not None
        assert self['install_filename'] is not None
        assert self['special_actions'] in (None, 'create_run_sh')
        assert self['optional?'] in (True, False)
        assert self['install_optional?'] in (True, False)



