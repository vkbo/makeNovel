## makeNovel

### NOTE: I am in the process of rewriting this tool from scratch. Unfortunately I don't currently have the time for it, so it is left in a half-finished state and is therefore not usable.

makeNovel is a tool, written in Python3, to assist in writing novels. It is intended to be used with an extended markdown format designed to work with this tool.

**Core Features**

* Each scene of the novel is kept in a separate file in whatever folder structure you prefer.
* The scene files can be written in whatever editor you wish to use, but they need to be saved as plain text files.
* The position of the scene files within chapters is controlled with a master file.
* The makeNovel tool will let you build HTML, PDF or OpenOffice document versions of the novel.
* The makeNovel can generate scene-wise maps of all the meta data added to each scene. This is in fact one of the core features of makeNovel. This can for instance be used to generate and overview of which characters, objects or locations feature in each scene and chapter of the novel.

### Background

There are many ways to write a novel from the technical side of things. I prefer to work on my projects by writing each scene as an individual file. However, having a folder with loads of smaller text documents can become messy when they need to be compiled into a full novel. This tool provides a way of setting up the layout in a master document in a text file.

I've spent some time previously writing a GUI application for organising novels, but I end up spending more time coding than writing. Those projects are on hold while I write this tool. Writing GUI applications is a lot of work.

There are many novel writing programs out there. I find most of them too cluttered. Document editors do work fairly well, but I prefer even simpler tools. With this tool, you can use any editor you like, but as a programmer I prefer to use code (plain text) editors.

For planning the novel, I use a zim-wiki, an excellent note taking application also written in Python.

## Usage

Functionality is still being implemented, here's an overview of what is in planned and partially implemented. Check back for progress.

### Input files

The novel is divided up into a single master file, describing the project, and individual scene files with associated meta data. 

#### Master File Format

`makeNovel` takes a master layout file as its main input. The keyword `@master` needs to be the first command in the file for it to be parsed as a master document.

#### Scene File Format

The scenes are contained in files where the first command is `@scene`. The files are then added to the master file with `@add` commands. See below.

#### Command Overview

##### The `@add` Commands

Format: `@add [object]: [value]`

Valid objects in `@master` files are:

* `character` - Adds a new character to the novel (string). Value is the internal character ID of your choice.
* `frontamtter` - Adds a new front matter section (string). Any scene file added here will be added to the front of the novel with no auto-generated headings or chapter numbers. Value is ignored.
* `prologue` - Adds an un-numbered chapter to the front of the novel (string). Value is the title of the chapter.
* `chapter` - Adds a numbered chapter to the novel (string). Value is the title of the chapter.
* `epilogue` - Adds an un-numbered chapter to the end of the novel (string). Value is the title of the chapter.
* `backmatter` - Adds a new back matter section (string). Any scene file added here will be added to the back of the novel with no auto-generated headings or chapter numbers. Value is ignored.

valid only after an `@add frontmatter`, `prologue`, `chapter`, `epilogue` or `backmatter` command:

* `scene` - Adds a scene file to the last chapter object (string). Value is the file name. If the extension of the file is `.nwf`, the extension can be omitted.

##### The `@set` Commands

Format: `@set [object.variable]: [value]`

Valid objects and variables in `@master` files are:

* `book.title` - The title of the novel (string).
* `book.author` - The author of the novel (string). The command can be called multiple times to set more than one author.
* `book.status` - The status of the novel project (string). I.e. "Draft One", etc.

After an `@add character` command:

* `character.name` - The full name of the character (string). Used for labels when generating charts.
* `character.status` - The status of the character (string). Used for grouping when generating charts. Can be used to separate main characters from other characters, etc.
* `character.importance` - Alternative way of grouping characters (float). Used for sorting characters when generating charts.

After an `@add frontmatter`, `prologue`, `chapter`, `epilogue` or `backmatter` command:

* `chapter.compile` - Whether to include the following scene files when compiling the document (boolean)

### Runing makeNovel

Format: `makeNovel [command] [options]`

**Commands:**

    init      Sets up a new project.
    make      Make the novel file tree into various output formats.
    build     Build various outputs like story timeline, etc.
    analyse   Prints a list of statistics like word count, etc.
    config    Set various configuration options.
    backup    Create a backup of the novel project.
    version   Print program version.
    help      Print this help message, or for any of the above commands.
    
    For more details on each command, type makenovel help [command].

