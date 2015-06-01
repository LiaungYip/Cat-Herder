# Cat-Herder

A command line tool for updating Minecraft servers based on ATLauncher modpacks.

Currently, `cat-herder` is able to install new servers using the `install` option. The `update` option is not implemented yet.

As of 2015-06-02, there is support for "Share Codes" via the `install-from-share-code` option.

Regardless, the tool is still useful for directly downloading an updated version of a modpack to a server, eliminating the pesky cycle of using the ATLauncher app to download a new server, zip the resulting installation, and upload the entire zip at painfully slow speeds.

## Disclaimer

The tool has been tested to install a Bevo's Tech Pack BTP-11-Full server, which works successfully on my machine.

However! This is alpha, un-tested software, so *back up your server before using this tool*.

## Feedback

Feedback is welcome - submit a GitHub issue, a pull request, or email minecraft@penwatch.net.

## Usage

It's a Python script. It uses Python 2.

Dependencies are `plac` and `unshortenit`.

Put the .py files somewhere and run `cat-herder.py` at the command line. `cat_herder.py -h` for usage instructions.

## License

This software is made available under the terms of the MIT License. Have fun.
