import "complex"


type rect = {
    x: f64, y: f64,
    w: f64, h: f64
}

module mandelbrot = \(C: complex with real = f64) -> {
    module C = C
    type t = C.t

    def sqr z = C.(z * z)

    def mandelbrot c (z: C.t) = C.(sqr z + c)

    def iter_mandelbrot (n: i32) c =
        loop acc = (C.complex (0, 0), 0) for i < n do
            if C.abs acc.0 < 2 then
                let z = mandelbrot c acc.0 in
                (z, i + 1)
            else
                (acc.0, acc.1)
}


local open mandelbrot c64


def gen_points (r: rect) xres yres: [yres][xres]C.t =
    let (xstep, ystep) =
             (r.w / f64.i64 xres, r.h / f64.i64 yres)

    let xs = map f64.i64 (iota xres)
             |> map (\n -> r.x + n * xstep)
    let ys = map f64.i64 (iota yres)
             |> map (\n -> r.y + n * ystep) in

    map (\y ->
            map (\x -> C.complex (x, y)) xs) ys



-- usage: mandelbrot <rect> <res> <iterations>
def main (r: [4]f64) xres yres iter_count : [yres][xres][3]u8 =
    let r = { x = r[0], y = r[1], w = r[2], h = r[3] }
    let r = { x = r.x - r.w, y = r.y - r.h, w = r.w * 2, h = r.h * 2}

    let grid = gen_points r xres yres in

    let mset = map (\col ->
        map (iter_mandelbrot iter_count) col) grid in

    map (\col ->
        map (\(_, its) ->
            let v = f64.i32 (iter_count - its) / f64.i32 iter_count
            let bytev = u8.f64 (v * 255) in
                replicate 3 bytev) col) mset