ERBAutocomplete
======================
The Package to help use erb template user that easy and quick to finish the erb tag.
***

How to install
-------------

<!-- With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run "Package Control: Install Package" command, find and install `ERBAutocomplete` package.
2. Restart your sublime text editor. -->


Manually:

1. Clone or [download](https://github.com/CasperLaiTW/ERBAutocomplete/archive/master.zip "download") git repo into your sublime text 3 packages folder.
2. Restart your sublime text editor.
***

Usage
-------------
You would set syntax to **ERB**.

And you can:

Manually:
1. Type erb keyword like **if**, **else** or nothing.
2. Press `ctrl` + `spcae`, will activate completion. ST would popup to tip you and select you want.

Automatic completion:
1. Open your user settings file.
2. Add `text.html.erb` to `auto_complete_selector`, you should according to your settings to set. this is an example.
    `"auto_complete_selector"` : `"source - comment, meta.tag - punctuation.definition.tag.begin, text.html.erb"`
3. Reset your sublime text editor.
4. And now you type **if**, **else**, the editor will automatic activate copmletion.
