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

## Usage

It's a Python script. It uses Python 2.

Dependencies are `plac` and `unshortenit`.

Put the .py files somewhere and run `cat-herder.py` at the command line. `cat_herder.py -h` for usage instructions.

## License

This software is made available under the terms of the MIT License. Have fun.
