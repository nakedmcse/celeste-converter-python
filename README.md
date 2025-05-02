# Celeste Converter Python

A Python implementation of a tool for converting between Celeste game assets (DATA format) and PNG images.

## Overview

This tool allows you to convert between Celeste's proprietary DATA format and standard PNG images. It's a Python port of the original [Rust-based celeste-converter](https://github.com/borogk/celeste-converter).

## Features

- Convert DATA files to PNG images
- Convert PNG images back to DATA files
- Preserve alpha channel information
- Run-length encoding (RLE) compression support

## Usage

```
python3 celeste-converter.py [options] [command] <from-directory-or-file> <to-directory-or-file>
```

Available commands:
- `data2png`: Convert DATA files to PNG images
- `png2data`: Convert PNG images to DATA files

Options:
- `-h`: Show help text
- `-v`: Enable verbose logging

### Examples

```sh
# Convert all .data files in the "assets" directory to PNG files in the "output" directory
python3 celeste-converter.py data2png ./assets ./output

# Convert all PNG files back to DATA format
python3 celeste-converter.py png2data ./modified_assets ./output

# Convert multi.data to multi-mod.png
python3 celeste-converter.py data2png multi.data multi-mod.png

# Convert with verbose logging
python3 celeste-converter.py -v data2png ./assets ./output
```

## Building from Source

This requires the pillow module to be installed.
