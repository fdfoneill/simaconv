# simaconv

This is a simple project, really just a wrapper around a script used to convert .csv files from SIMA into ESRI shapefile format.

# Usage

## SimaFile: Introduction

The main access point for the `simaconv` package is the `SimaFile` class, available either through `simaconv.SimaFile` or `simaconv.simafile.SimaFile`. This class has three basic methods, each of which is one step in the conversion of a SIMA CSV file to shapefile format. The first is the instantialization method (__init__()), which expects the filepath to a SIMA csv file. For example, consider the following snippet:

```python
from simaconv import SimaFile

sf = SimaFile(C:/path/to/file.csv)
```

## The `cleanFile()` Function

The class contains a CSV parser that will do its level best to figure out what's going on in the given CSV. In the past, however, we have occasionally had issues with the SIMA files containing characters that cannot be interpreted, or internal double-quotes within fields that cause those fields (especially the "geometry" field) to be split into multiple columns. This behavior is undesirable.

To that end, the simaconv.simafile module contains a stand-alone function called `cleanFile()`, which accepts a CSV file path as its single argument. This function replaces the most common double-quoted strings with their single-quoted equivalent, hopefully eliminating that particular problem. The list of words that appear in double-quotes, however, is ever-growing, so users may need to add to the `cleanFile` function as they recieve new data from SIMA.

The issue of non-English characters is unfortunately not yet automated. They must be detected and removed by hand at this time.

## SimaFile: loadJson

ArcPy's tools for creating shapefile fields require each field to have a name and data type. Unfortunately, the naming requirements for Shapefile fields are quite strict, and most of SIMA's field names do not comply (they are too long). For a long time it was necessary to manually associate each field with a new fieldname and data type; this is no longer the case. The `simaconv` package contains a json file (simaconv/resources/shortnames_and_dtypes.json) that associates all the field names from those files received thus far with short names and data types (as the filename suggests). This json file must be read into a `SimaFile` instance through the `loadJson()` method, as follows:

```python
from simaconv import SimaFile

sf = SimaFile(C:/path/to/file.csv)

sf.loadJson()
```

This may seem like an extraneous step, but the `loadJson` method also allows the user to read in a custom json file (rather than the default), if they wish to store their records of short names and data types somewhere other than simaconv/resources.

## SimaFile: writeShapefile

This final method writes the data held by a `SimaFile` instance into an output shapefile. If all goes well, the new shapefile will appear in the location specified by the `out_file_path` passed as the method's only argument. This process can take some time; luckily ArcPy prints a large amount of output to the screen as a reassurance that something is in fact happening.

## Summary

In sum, the full process of converting a SIMA csv to shapefile format might look something like this:

```python
import simaconv.simaFile as sf

input_csv = "C:/path/to/input/file.csv"
output_shapefile = "C:/path/to/output/write/location.shp"

sf.cleanFile(input_csv)

simafile = sf.SimaFile(input_csv)
simafile.loadJson()
simafile.writeShapefile(output_shapefile)
```

# License

MIT License

Copyright (c) 2020 F. Dan O'Neill

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
