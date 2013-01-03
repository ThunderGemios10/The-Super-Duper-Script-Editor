# The Super Duper Script Editor

A (mostly) fully featured script editor for _Danganronpa: Hope's Academy and Despair's Students_, released under the GNU GPL, Version 3.

## Dependencies

### Primary dependencies

* Python 2.7
    * <http://www.python.org/download/>
* PyQt4
    * <http://www.riverbankcomputing.co.uk/software/pyqt/download>
* PyEnchant
    * <http://packages.python.org/pyenchant/download.html>
* MeCab
    * <http://mecab.sourceforge.net/#download>
    * Must use UTF-8 dictionaries.
* Sony ATRAC3 Codec
    * <http://www.codecs.com/Sony_ATRAC3_Audio_Codec_download.htm>
    * Required to play voices.
* Java
    * <http://www.java.com>
    * Must be available on PATH on Windows

### Other dependencies

* mkisofs
    * Used to build the completed ISO.
    * A Windows binary is included in `tools`.
* pngquant
    * <http://pngquant.org/>
    * Used to quantize PNGs before converting them to GIM files. (Not actually used by anything available through the editor right now, but the WIP model importation script **does** make use of it.)
    * A Windows binary is included in `tools`.

## Features

### Extraction and building

The SDSE is capable of extracting all the game's files and packing them back up in a way the game understands, and it does everything all in one place. When you run the editor for the first time, it'll prompt you to set up your workspace, which includes extracting the game's archives. When you're ready to try your changes out, just click the Build button on the top right and it'll spit out an ISO that's ready to drop onto your PSP.

### Real-time previews

See how every line is going to look in-game, so you don't have to waste time guessing how much space you have available, wondering who said a line, or what sprite is being shown at any given time. The SDSE can even play back voice clips from the game and display CG. It also supports all the game's text formatting codes, and it has special previews for text that appears in different contexts.

### Comments

If you're not sure how you want to word a line, or you just want to leave a note about a reference or something, leave a comment.

#### References

The SDSE also has special syntax for references in comments. Type `{e00_001_000.lin/0000.txt}` into the comments, and it'll turn blue and be added to the References tab on the right side of the editor. From there, you can see the line in question without having to open the folder.

You can also make in-folder references, so if you're in `e00_001_000.lin`, you can just type `{0000.txt}` and it'll be interpreted as `{e00_001_000.lin/0000.txt}`. Do be aware, though, that if you do this on a line that has duplicates in other folders, those other references are likely to be incorrect, so it's better to use the full format instead.

### Duplicate and similar line tracking

The SDSE keeps track of lines that are identical to one another and propogates changes to all of those lines. But not only that, it also keeps track of lines that are similar, but not necessarily identical. This way, you can see lines that have been subtly changed so you can keep your translation consistent while still reflecting the difference.

Since, in certain cases, identical lines don't need to be translated identically, you can tell the editor that one line isn't a duplicate of another line by right-clicking on it in the Duplicates tab and selecting `remove duplicate`. You can also break up an entire duplicate group by selecting `remove all duplicates`.

To remove the current line from a duplicate group and leave the rest of the group in tact, right-click on the line in the main window, under `script files`, and select `remove from duplicate group`.

You can also add duplicates, either from similarities or references.

**NOTE**: It can take some time to read all the similarities from the database, which can cause lines to appear slowly. This should only happen the first time you look at a line, and usually only if you're moving through the folder pretty quickly. If you're reading or translating each line, you're not likely to notice any slowdown.

### Terminology highlighting

Create and categorize your own list of important terminology--words or phrases that need to be translated consistently. The editor will highlight any matches for you, and you can see the translation just by hovering over the highlighted text. It even works for overlapping terms, so you can set 苗木, 誠, and 苗木誠 as separate terms, and it'll show you all the possible meanings.

Terminology can also be expressed as a regular expression (such as `うぷ+`) to catch slight variations.

### Spell-checking

Typos are inevitable, and spellcheck can be an invaluable tool for keeping errors to a minimum. The SDSE uses PyEnchant (listed under the dependencies) to handle spellchecking.

PyEnchant comes with a few dictionaries by default, but if you want to install a dictionary for another language, check [here](http://packages.python.org/pyenchant/tutorial.html#adding-language-dictionaries) for information on how to do it.

### Font generation

The font that comes with _Danganronpa_ pretty much only supports Japanese and English, and the non-Japanese characters have some weird alignment issues, so the SDSE comes with a font generator that will allow you to create your own font, to your own specifications, with any glyphs needed by the language you're translating into

You can even create fonts for the game using glyphs from more than one font on your system, so if you don't line how a certain glyph looks, just use a different font for it. (Both of the fonts Project Zetsubou uses, which are available on the downloads page, are blends.)

### And much, much more

Explore, click on things, right-click on things, push buttons, play around. I've done so much work on things thing, I honestly don't remember everything it can do.

## Some handy shortcuts

* `Page Up` = Go to previous line
* `Page Down` = Go to next line
* `Ctrl` + `Page Up` = Go to first line
* `Ctrl` + `Page Down` = Go to last line
* `F5` = Replay voice
* `F6` = Stop voice
* `Ctrl` + `O` = Open
* `Ctrl` + `S` = Save
* `Ctrl` + `F` = Find
* `Ctrl` + `T` = Terminology editor
* `Ctrl` + `B` = Build ISO