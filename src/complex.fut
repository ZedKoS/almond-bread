
module type complex = {
    type t
    type real

    val complex : (real, real) -> t
    val re : t -> real
    val im : t -> real
    val conj : t -> t

    val + : t -> t -> t
    val - : t -> t -> t
    val * : t -> t -> t

    val neg : t -> t
    val abs : t -> real
}

module type complex64 = complex with real = f64


module c64: complex64 = {
    type real = f64
    type t = { re: real, im: real }

    def complex (re, im) = { re, im }
    
    def re (z: t) = z.re
    def im (z: t) = z.im
    def conj (z: t) = z with im = -z.im

    def neg z = intrinsics.({ re = -re z, im = -im z })
    def a + b = intrinsics.({ re = re a + re b, im = im a + im b })
    def a - b = a + neg b
    def a * b = intrinsics.({
        re = re a * re b - im a * im b,
        im = re a * im b + im a* re b
    })

    def abs (z: t) = re (z * conj z) |> f64.sqrt
}

module split64: complex64 = {
    type real = f64
    type t = { re: real, im: real }

    def complex (re, im) = { re, im }
    
    def re (z: t) = z.re
    def im (z: t) = z.im
    def conj (z: t) = z with im = -z.im

    def neg z = intrinsics.({ re = -re z, im = -im z })
    def a + b = intrinsics.({ re = re a + re b, im = im a + im b })
    def a - b = a + neg b
    def a * b = intrinsics.({
        re = re a * re b + im a * im b,
        im = re a * im b + im a * re b
    })

    def abs (z: t) = re (z * conj z) |> f64.sqrt
}

module dual64: complex64 = {
    type real = f64
    type t = { re: real, im: real }

    def complex (re, im) = { re, im }
    
    def re (z: t) = z.re
    def im (z: t) = z.im
    def conj (z: t) = z with im = -z.im

    def neg z = intrinsics.({ re = -re z, im = -im z })
    def a + b = intrinsics.({ re = re a + re b, im = im a + im b })
    def a - b = a + neg b
    def a * b = intrinsics.({
        re = re a * re b, -- im a * im b == 0
        im = re a * im b + im a * re b
    })

    def abs (z: t) = re z -- re (z * conj z) == (re z)^2
}


type c64 = c64.t
type split64 = split64.t
type dual64 = dual64.t
