# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 04:16:52 2019

@author: hihih
"""
import sys
import copy
import struct
import binascii



F64 = 0xFFFFFFFFFFFFFFFF

_k = [0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
      0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
      0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
      0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
      0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
      0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
      0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
      0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
      0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
      0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
      0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
      0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
      0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
      0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
      0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
      0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
      0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
      0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
      0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
      0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

_h = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1,
      0x510e527fade682d1, 0x9b05688c2b3e6c1f, 0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]


def _pad(msglen):
    mdi = msglen & 0x7F
    length = struct.pack('!Q', msglen << 3)

    if mdi < 112:
        padlen = 111 - mdi
    else:
        padlen = 239 - mdi

    return b'\x80' + (b'\x00'*(padlen+8)) + length

def _rotr(x, y):
    return ((x >> y) | (x << (64 - y))) & F64
def _maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)
def _ch(x, y, z):
    return (x & y) ^ ((~x) & z)

def new(m=None):
    return SHA512(m)

class SHA512(object):
    _output_size = 8

    blocksize = 1
    block_size = 128
    digest_size = 64

    def __init__(self, m=None):
        self._counter = 0
        self._cache = b''
        self._k = copy.deepcopy(_k)
        self._h = copy.deepcopy(_h)

        self.update(m)

    def _compress(self, chunk):
        w = [0] * 80
        w[0:16] = struct.unpack('!16Q', chunk)

        for i in range(16, 80):
            s0 = _rotr(w[i-15], 1) ^ _rotr(w[i-15], 8) ^ (w[i-15] >> 7)
            s1 = _rotr(w[i-2], 19) ^ _rotr(w[i-2], 61) ^ (w[i-2] >> 6)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & F64
            print(i,'w',w[i])

        a, b, c, d, e, f, g, h = self._h

        for i in range(80):
            s0 = _rotr(a, 28) ^ _rotr(a, 34) ^ _rotr(a, 39)
            t2 = s0 + _maj(a, b, c)
            s1 = _rotr(e, 14) ^ _rotr(e, 18) ^ _rotr(e, 41)
            t1 = h + s1 + _ch(e, f, g) + self._k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & F64
            d = c
            c = b
            b = a
            a = (t1 + t2) & F64

        for i, (x, y) in enumerate(zip(self._h, [a, b, c, d, e, f, g, h])):
            self._h[i] = (x + y) & F64
            print('h[i]',self._h[i])

    def update(self, m):
        if not m:
            return

        self._counter += len(m)
        m = self._cache + m

        for i in range(0, len(m) // 128):
            self._compress(m[128 * i:128 * (i + 1)])
        self._cache = m[-(len(m) % 128):]

    def digest(self):
        r = copy.deepcopy(self)
        r.update(_pad(self._counter))
        data = [struct.pack('!Q', i) for i in r._h[:self._output_size]]
        return b''.join(data)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode('ascii')

"""
if __name__ == '__main__':
    def check(msg, sig):
        m = SHA512()
        m.update(msg.encode('ascii'))
        print(m.hexdigest() == sig)

    tests = {
        "":
            'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
        "a":
            '1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75',
        "abc":
            'ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f',
        "message digest":
            '107dbf389d9e9f71a3a95f6c055b9251bc5268c2be16d6c13492ea45b0199f3309e16455ab1e96118e8a905d5597b72038ddb372a89826046de66687bb420e7c',
        "abcdefghijklmnopqrstuvwxyz":
            '4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613a59ed5441fb0f321389f77f48a879c7b1f1',
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
            '1e07be23c26a86ea37ea810c8ec7809352515a970e9253c26f536cfc7a9996c45c8370583e0a78fa4a90041d71a4ceab7423f19c71b9d5a3e01249f0bebd5894',
        ("12345678901234567890123456789012345678901234567890123456789"
         "012345678901234567890"):
            '72ec1ef1124a45b047e8b7c75a932195135bb61de24ec0d1914042246e0aec3a2354e093d76f3048b456764346900cb130d2a4fd5dd16abb5e30bcb850dee843'
    }

    for inp, out in tests.items():
        check(inp, out)
"""
