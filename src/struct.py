import struct

def char(c):
    return struct.pack("=c", c.encode("ascii"))


def word(w):
    return struct.pack("=h", w)


def dword(d):
    return struct.pack("=l", d)


def color(r, g, b):
    r = max(0, min(r, 1))
    g = max(0, min(g, 1))
    b = max(0, min(b, 1))
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)])