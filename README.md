# almond-bread
A tool for generating images of the Mandelbrot set, written in [Futhark], provided
with the necessary utilities to convert Futhark output into an image.

## Setup

### Dependencies
To compile and use this project, you need:
* [Python 3.10](https://www.python.org/downloads/release/python-3100/) (may change in the future)
* An installation of the [Futhark language][Futhark]
* make, e.g. [GNU Make](https://www.gnu.org/software/make/) (not required - you can easily compile everything manually)

### Compilation

Download the repository:
```
git clone https://github.com/ZedKoS/almond-bread.git
```

This will create a folder named almond-bread. Let's build the executable:
```
cd almond-bread/
make
```

If all went well, you will find a file called `mandelbrot` in the newly-created `bin/` folder

## Usage (W.I.P)
At the moment, you will need to go through two steps in order to generate an image (.bmp).
1. In the folder `almond-bread/`, run the following command, substituting the arguments between `<brackets>` as needed:
   ```
   echo [<a>, <b>, <rx>, <ry>] <width> <height> <iterations> | bin/mandelbrot > <out>
   ```
   Where:
   * `a` and `b` are the components of the complex number in the middle of the image (`z = a + bi`)
      e.g. 0, 1 for `z = i`
   * `rx` and `ry` are the extents of the image (e.g. 1e-3, 0.01, etc.). You usually want these to be the same
     if you are generating a square image without any stretching.
   * `width` and `height` are the width and the height of the generated image respectively, in pixels.  
     It is recommended that `width/height = rx/ry`, or else the image will be stretched.
   * `iterations` tells the program how many steps to take to generate each pixel. A lower iteration count (e.g. 16) will be faster but will
     not be accurate if the image is zoomed in (i.e. `rx` and `ry` are very small)
   * `out` is where the program will place the generated file, encoded in the Futhark **Binary Data Format** (_**BDF**_). You will
     need to follow step (2) in order to view it as an image.
 
2. Locate the generated **BDF** file. Then, inside `almond-bread/`, run `bdf2bmp.py` in the `tools/` folder as follows:
   ```
   tools/bdf2bmp.py <bdf-file>
   ```
   Where `bdf-file` is the path to generated file (e.g. `out/myimage`).
   
   The tool will create a file named `<bdf-file>.bmp`, which can be viewed by many programs.

That's it!

## Deleting the binaries

To remove the executable, run:
```
make clean
```

[Futhark]: https://futhark-lang.org/
