#!/usr/bin/python
__author__ = 'Thomas Dixon'
__license__ = 'MIT'
import copy
import struct
import binascii

F32 = 0xFFFFFFFF

_k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
      0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
      0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
      0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
      0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
      0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
      0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
      0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
      0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
      0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
      0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
      0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
      0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
      0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
      0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
      0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
_h = [0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
          0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4]

def _pad(msglen):
    mdi = msglen & 0x3F
    length = struct.pack('!Q', msglen << 3)

    if mdi < 56:
        padlen = 55 - mdi
    else:
        padlen = 119 - mdi

    return b'\x80' + (b'\x00'*padlen) + length

def _rotr(x, y):
    return ((x >> y) | (x << (32 - y))) & F32
def _maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)
def _ch(x, y, z):
    return (x & y) ^ ((~x) & z)

def new(m=None):
    return SHA224(m)

class SHA224(object):
    _output_size = 7
    blocksize = 1
    block_size = 64
    digest_size = 28

    def __init__(self, m=None):
        self._counter = 0
        self._cache = b''
        self._k = copy.deepcopy(_k)
        self._h = copy.deepcopy(_h)

        self.update(m)

    def _compress(self, c):
        w = [0] * 64
        w[0:16] = struct.unpack('!16L', c)

        for i in range(16, 64):
            s0 = _rotr(w[i-15], 7) ^ _rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = _rotr(w[i-2], 17) ^ _rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & F32
            print(i,'w',w[i])

        a, b, c, d, e, f, g, h = self._h

        for i in range(64):
            s0 = _rotr(a, 2) ^ _rotr(a, 13) ^ _rotr(a, 22)
            t2 = s0 + _maj(a, b, c)
            s1 = _rotr(e, 6) ^ _rotr(e, 11) ^ _rotr(e, 25)
            t1 = h + s1 + _ch(e, f, g) + self._k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & F32
            d = c
            c = b
            b = a
            a = (t1 + t2) & F32

        for i, (x, y) in enumerate(zip(self._h, [a, b, c, d, e, f, g, h])):
            self._h[i] = (x + y) & F32
            print(i,'h[i]',self._h[i])

    def update(self, m):
        if not m:
            return

        self._counter += len(m)
        m = self._cache + m

        for i in range(0, len(m) // 64):
            self._compress(m[64 * i:64 * (i + 1)])
        self._cache = m[-(len(m) % 64):]

    def digest(self):
        r = copy.deepcopy(self)
        r.update(_pad(self._counter))
        data = [struct.pack('!L', i) for i in r._h[:self._output_size]]
        return b''.join(data)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')
"""
#tset
if __name__ == '__main__':
    def check(msg, sig):
        m = SHA224()
        m.update(msg.encode('ascii'))
        print(m.hexdigest() == sig)

    tests = {
        "":
            'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
        "a":
            'abd37534c7d9a2efb9465de931cd7055ffdb8879563ae98078d6d6d5',
        "abc":
            '23097d223405d8228642a477bda255b32aadbce4bda0b3f7e36c9da7',
        "message digest":
            '2cb21c83ae2f004de7e81c3c7019cbcb65b71ab656b22d6d0c39b8eb',
        "abcdefghijklmnopqrstuvwxyz":
            '45a5f72c39c5cff2522eb3429799e49e5f44b356ef926bcf390dccc2',
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            'bff72b4fcb7d75e5632900ac5f90d219e05e97a7bde72e740db393d9',
        ("12345678901234567890123456789012345678901234567890123456789"
         "012345678901234567890"):
            'b50aecbe4e9bb0b57bc5f3ae760a8e01db24f203fb3cdcd13148046e'
    }

    for inp, out in tests.items():
        check(inp, out)
"""









