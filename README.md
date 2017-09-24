## makeNovel

**Note:** This tool is under development.

This is a simple Python3 module that will compiles individual scene files into a novel in a single
document. The structure of the final document is defined in a master file.

### Background

There are many ways to write a novel from the technical side of things. I prefer to work on my
projects by writing each scene as an individual file. However, having a folder with loads of smaller
text documents can become messy when they need to be compiled into a full novel. This tool provides
a way of setting up the layout in a master document in a text file.

The structure of the master file is simple. Set global parameters like book title and authors, add
chapters, and scenes to each chapter. The scene files are easy to move around to where you want
them, and you can add comments to the master document with the character `#`. I also plan to add
different output formats to the tool. Initially plain text, html and fodt. The latter is a flat file
format (flat odt) which is an open document standard. It works in OpenOffice and LibreOffice, and
probably also in Microsoft Word.

I've spent some time previously writing a GUI application for organising novels, but I end up
spending more time coding than writing. Maintaining a GUI application is also a lot of work. So I
have more or less abandoned those projects.

There are many novel writing programs out there. I find most of them too cluttered. Document editors
do work fairly well, but I prefer even simpler tools. The two main tools I use are:

* **Zim-wiki**: an excellent note taking tools written in Python. I already use it for work, and it
   is also perfect for researching and drafting novel plots, characters, etc.
* **FocusWriter**: an excellent no-distraction text editor with the minimum of features you need for
   writing. I use it to write individual scene files.

### Usage

Only a bare minimum of functionality is implemented. But all the commands below work. At the moment
`makeNovel` only works with fodt files. These can be written by FocusWriter, and opened in
LibreOffice and OpenOffice (and perhaps Microsoft Word).

#### Master File Format

`makeNovel` takes a master layout file as its main input andparses it and generates a single
document as output.

##### General Syntax

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

##### All Commands

###### SET Commands

* `TITLE`: The book title
* `FORMAT`: Assumed format of input files. Accepts txt and fodt. Will also support html.
* `INPATH`: Root folder of scene files. This is where the script starts to look. If you organise
   the files in folders under that, the relative path needs to be added to the `ADD SCENE` entry.
* `SEPARATOR`: Sets the text used for separators inserted with the `SEPARATOR` command. Default
   value is `***`.
* `JUSTIFY`: Set to `ON`, `TRUE` or `1` to enable straight margins for paragraphs.

###### ADD Commands

* `AUTHOR`: Adds an author to the list of authors. Separate multiple authors with `;`. The command
   can also be run multiple times to add authors.
* `PROLOGUE`: Adds a prologue section to the novel. Title is an optional argument.
* `CHAPTER`: Adds a chapter section to the novel. Each command increases the chapter number by one.
   Title is an optional argument.
* `EPILOGUE`: Adds an epilogue section to the novel. Title is an optional argument.
* `SCENE`: Adds a scene to the most recently added prologue, chapter or epilogue. If a scene is
   added before any of these have been defined, an error is reported.
* `SEPTITLE`: Adds a separating title before the next scene.

###### Other Commands

* `BREAK`: Adds a blank paragraph. Can be used as a short break between scenes.
* `SEPARATOR`: Adds a paragraph with the text defined by `SET SEPARATOR` between two scenes.

#### Run makeNovel

To compile the document, use:

    makeNovel -i path/to/master-file.conf

##### Full list of arguments:

| Short | Long        | Description                                                      | Default |
|-------|-------------|------------------------------------------------------------------|---------|
| `-i`  | `--infile=` | Input file that descripes the novel layout.                      | None    |
| `-d`  | `--debug=`  | Chose debug level. Valid inputs are ERROR, WARN, INFO and DEBUG. | WARN    |
| `-h`  | `--help`    | Prints help text and exits.                                      |         |
| `-v`  | `--version` | Prints version and exits.                                        |         |
