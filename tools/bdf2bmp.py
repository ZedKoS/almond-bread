#!/usr/bin/env python3.10

from functools import reduce
import sys
from typing import Iterator, NamedTuple, Optional


_iota_counter = 0

def iota(n: Optional[int] = None) -> int:
    global _iota_counter

    if n is not None:
        _iota_counter = n
    _iota_counter += 1

    return _iota_counter - 1


class BDFType:
    def __init__(self, size: int, pyty):
        self.size = size
        self.pyty = pyty


    @staticmethod
    def from_str(s: str):
        if len(s) != 4:
            return None

        if s == b"  i8":
            return i8
        if s == b" i16":
            return i16
        if s == b" i32":
            return i32
        if s == b" i64":
            return i64

        if s == b"  u8":
            return u8
        if s == b" u16":
            return u16
        if s == b" u32":
            return u32
        if s == b" u64":
            return u64

        if s == b" f16":
            return f16
        if s == b" f32":
            return f32
        if s == b" f64":
            return f64

        if s == "bool":
            return bdf_bool
        
        return None


i8  = BDFType(1, int)
i16 = BDFType(2, int)
i32 = BDFType(3, int)
i64 = BDFType(4, int)

u8  = BDFType(1, int)
u16 = BDFType(2, int)
u32 = BDFType(3, int) 
u64 = BDFType(4, int) 

f16 = BDFType(2, float)
f32 = BDFType(3, float) 
f64 = BDFType(4, float) 

bdf_bool = BDFType(1, bool)


class BDFData:

    def __init__(
        self,
        ver: int,
        ndims: int,
        ty: BDFType,
        dims: list[int],
        vals: list):

        self.ver = ver
        self.ndims = ndims
        self.ty = ty
        self.dims = dims
        self.vals = vals


def main():
    filenames = parse_args()

    for filename in filenames:
        bdf = None

        print(f"Opening {filename}.bmp")

        with open(filename, 'rb') as f:
            bdf_bytes = f.read()
            print(f"File size: {len(bdf_bytes)}")
            try:
                bdf = parse_bdf(bdf_bytes)
            except Exception as e:
                exit(f"Could not parse the BDF: {e}")

        print(f"Converting {filename}.bmp")

        bmp = convert(bdf)
        # print(f"Raw BMP: {bmp}")

        with open(filename + '.bmp', 'wb') as f:
            f.write(bmp)
        
        print(f"Completed {filename}.bmp")


def parse_args() -> list[str]:
    progname = sys.argv[0]
    args = sys.argv[1:]

    if len(args) == 0:
        exit(f"Usage: {progname} <filenames...>")
    
    return args


def parse_bdf(raw: bytes) -> BDFData:
    if chr(raw[0]) != 'b':
        raise Exception(f"file header must start with 'b' [{raw[0]}]")


    ver = raw[1]
    ndims = raw[2]
    ty = BDFType.from_str(raw[3:7])

    print(f"ty: {ty}")

    dims = []
    values = b""

    index = 7
    for i in range(ndims):
        dim = int.from_bytes(raw[index:index+8], 'little')
        dims.append(dim)
        index += 8

    print(f"Dims: {dims}")

    size = reduce(lambda x, y: x * y, dims)
    if size == 0:
        size = 1

    values = raw[index:]

    # for i in range(size):
        # print(f"{i}/{size}")
        # dimvalues = []
        # val = parse_value(raw, ty)
        # values += val
        # dimvalues.append(val)
        # values.append(dimvalues)
    
    # print(f"Values: {values}")
    
    return BDFData(ver, ndims, ty, dims, values)


def parse_value(raw: Iterator[int], ty: BDFType):
    v = next(raw)
    return v.to_bytes(ty.size, 'little')


def convert(data: BDFData):
    assert data.ndims == 3
    assert data.dims[2] == 3

    raw_bmp = bytearray(b"")

    # header
    raw_bmp += b"BM"

    size_bytes_index = len(raw_bmp)
    raw_bmp += b"\0" * 4 # size

    raw_bmp += b"\0" * 4 # reserved

    start_offset_index = len(raw_bmp)
    raw_bmp += b"\0" * 4 # start offset
 
    raw_bmp += int.to_bytes(40, 4, 'little')
    raw_bmp += int.to_bytes(data.dims[0], 4, 'little', signed=True)
    raw_bmp += int.to_bytes(data.dims[1], 4, 'little', signed=True)
    raw_bmp += int.to_bytes(1, 2, 'little') # planes
    raw_bmp += int.to_bytes(24, 2, 'little') # bpp
    raw_bmp += b"\0" * 4 # no compression
    raw_bmp += b"\0" * 4 # size, 0 since no compression

    raw_bmp += b"\0" * 8
    raw_bmp += b"\0" * 4
    raw_bmp += b"\0" * 4

    offset = int.to_bytes(len(raw_bmp), 4, 'little')
    
    for i in range(4):
        j = i + start_offset_index
        raw_bmp[j] = offset[i]

    raw_bmp += data.vals

    size = int.to_bytes(len(raw_bmp), 4, 'little')

    for i in range(4):
        j = i + size_bytes_index
        raw_bmp[j] = size[i]
    
    print(f"Length of BMP: {len(raw_bmp)}")

    return raw_bmp


if __name__ == "__main__":
    main()