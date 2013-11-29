# Kismet GPS Tools

A collection of post-processing tools for Kismet GPS files.

Currently only supports .netxml input files, and outputs Shapefiles. KML, and other formats, will be supported later on.

Runs on Python 2.x as well as 3.x, and requires the `pyshp` library.


## Usage

```bash
$ ./kismet-gps-tools.py -i path-to-your-input.netxml -f shapefile
```

Shapefiles are saved by default to `shapefiles/networks.*`.


## Credits and License

Copyright © 2013 Yuval Adam. This software is free for usage under the GPLv3 license.
