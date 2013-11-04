# Sublime Grasp

This is simply a wrapper around grasp.
When it's complete, everything that works for grasp should work from here.

At the moment, the only thing that works for sure is searching for things.

## Usage

You must be in a javascript file, as grasp currently only supports javascript.
The current key binding is `ctrl`+`shift`+`g`.
This will bring up the input panel on the bottom awaiting your grasp command.

You can enter things like `if.test` to select all of the conditional tests.
Or `return.arg` to select all of the arguments being returned.

## Installation

#### Package Control

Just search for grasp.

### Manual

Clone this repository from your Sublime packages directory:

#### Linux

```
$ cd ~/.config/sublime-text-2/Packages
$ git clone https://github.com/joneshf/sublime-grasp
```

#### Macosx (untested)

```
$ cd "~/Library/Application Support/Sublime Text 2/Packages"
$ git clone https://github.com/joneshf/sublime-grasp
```

#### Windows

```
$ cd "%APPDATA%\Sublime Text 2"
$ git clone https://github.com/joneshf/sublime-grasp
```

## Contributing

Pretty much anything goes.