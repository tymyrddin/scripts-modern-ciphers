# RootMe: AES - CBC - Bit-Flipping Attack challenge

import base64

token = "yourtoken"
t = base64.b64decode(token)  # len : 112
for i in t:
    print(hex(i), end=" ")
tmp = bytearray(t)
tmp[37] ^= 0x01

tmp += bytearray("a".encode() * 16)
expected = bytearray(";is_member=true]".encode())
current = bytearray(b"+\x10\xb1\r\x8c\xd3\x99\x05\x0f\xfa\xed\x0e\xdc\x94\xc8\x1b")
print(len(current), len(expected))
for i in range(16):
    tmp[96 + i] ^= expected[i] ^ current[i]

print("\n", base64.b64encode(tmp))
