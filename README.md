## makeNovel

**Note:** This tool is under development.

This is a simple Python3 module that will compiles individual scene files and a master file into a
single file document.

### Background

There are many ways to write a novel from the technical side of things. I prefer to work on my
projects by writing each scene as an individual file. However, having a folder with loads of smaller
text documents can become messy. I've spent some time writing a GUI application for organising this,
but I end up spending more time coding than writing. Maintaining a GUI application is also a lot of
work.

Other novel writing programs are extensive and offer lots of different tools for planning and
writing. Personally, I find them to be very cluttered and distracting. Too many tools are designed
with the creator in mind, not the variety of preferences among users. Of course, this is also true
for most of the stuff I write. However, simple tools tend to be less like that.

For my writing, I use:
* **Zim-wiki**: an excellent note taking tools written in Python. I already use it for work, and it
   is also perfect for researching and drafting novel plots, characters, etc.
* **FocusWriter**: an excellent no-distraction text editor with the minimum of features you need for
   writing. I use it to write individual scene files.

### Usage

**Note:** This section is a list of features I plan to implement for the first version. This module
is under initial development. It currently parses the input file, but doesn't generate any output.

`makeNovel` takes a master layout file as its main input andparses it and generates a single
document as output.

#### General Syntax

The master document syntax is straight forward

    VARIABLE = varValue
    FUNCTION: inVal1; inVal2

Example:

    # This is a comment
    
    # Include another file
    @INC header.in

    # Set default input format
    SET FORMAT: txt
    
    SET TITLE:  Best Book Title Ever
    SET AUTHOR: J. Smith
    
    ADD CHAPTER: Chapter One; Day 1
        ADD SCENE: scene-001.txt
        SEPARATOR
        ADD SCENE: scene-002.txt

To compile the document, use:

    makeNovel -i path/to/master-file.conf

#### Full list of arguments:

| Short | Long        | Description                                                      | Default |
|-------|-------------|------------------------------------------------------------------|---------|
| `-i`  | `--infile=` | Input file that descripes the novel layout.                      | None    |
| `-d`  | `--debug=`  | Chose debug level. Valid inputs are ERROR, WARN, INFO and DEBUG. | WARN    |
| `-h`  | `--help`    | Prints help text and exits.                                      |         |
| `-v`  | `--version` | Prints version and exits.                                        |         |
