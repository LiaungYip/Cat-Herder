# Cat-Herder

A command line tool for updating Minecraft servers based on ATLauncher modpacks.

Currently, `cat-herder` is able to install new servers using the `install` option. The `update` option is not implemented yet.

As of 2015-06-02, there is support for "Share Codes" via the `install-from-share-code` option.

The tool is still useful for directly downloading an updated version of a modpack to a server, eliminating the pesky cycle of using the ATLauncher app to download a new server, zip the resulting installation, and upload the entire zip at painfully slow speeds.

Ryan of the ATLauncher has been contacted by email, is aware this project exists, and has no objections to it.

## Disclaimer

This tool is not very thoroughly tested and may do surprising things. It is recommended to have a backup of your server before you use this.

Do not point at people's faces. See your doctor if pain persists.

## Feedback

Feedback is welcome - submit a GitHub issue, a pull request, or email minecraft@penwatch.net.

## Installation.

It's a Python script. It uses Python 2.

Put it somewhere and run it from the command line.

Dependencies are `plac` and `unshortenit`.

## Usage

    usage: cat_herder.py [-h] [-p PACK_NAME] [-v PACK_VERSION] [-i INSTALL_FOLDER]
                         [-c CACHE_FOLDER] [-s SHARE_CODE] [-d]
                         {install,update,list_packs,install-from-share-code}
    
    A tool for installing and updating Minecraft servers based on ATLauncher mod packs.
        Example invocations:
    
        cat_herder.py list_packs
    
        Installing with share code:
        cat_herder.py install-from-share-code QtDNnlfZ
    
        As above, but manually specifying the download cache and server install folders:
        cat_herder.py install-from-share-code QtDNnlfZ -c /home/mc/cache -i /home/mc/install/
    
        Installing with manually specified pack name and pack version:
        cat_herder.py install -p BevosTechPack -v BTP-11-Full -c /home/mc/cache -i /home/mc/install/
        
    
    positional arguments:
      {install,update,list_packs,install-from-share-code}
                            Operation to perform
    
    optional arguments:
      -h, --help            show this help message and exit
      -p PACK_NAME, --pack-name PACK_NAME
                            Name of pack, i.e. 'BevosTechPack' - try 'list_packs'
                            for list of pack names
      -v PACK_VERSION, --pack-version PACK_VERSION
                            Version of pack, i.e. 'BTP-11-Full' - defaults to
                            latest available version
      -i INSTALL_FOLDER, --install-folder INSTALL_FOLDER
                            Folder where server will be installed - defaults to
                            './install/$pack_name/$pack_version'
      -c CACHE_FOLDER, --cache-folder CACHE_FOLDER
                            Folder where downloaded files will be cached -
                            defaults to './cache'
      -s SHARE_CODE, --share-code SHARE_CODE
                            Share code - required for 'install-from-share-code'.
      -d, --dry-run         Perform a dry run. Lists what would be downloaded and
                            installed, but doesn't actually download or install
                            anything.

## License

This software is made available under the terms of the MIT License. Have fun.
