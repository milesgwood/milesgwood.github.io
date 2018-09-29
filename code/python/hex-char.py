import binascii

x = b'test'
x = binascii.hexlify(x)
y = str(x,'ascii')

print(x) # Outputs b'74657374' (hex encoding of "test")
print(y) # Outputs 74657374

x_unhexed = binascii.unhexlify(x)
print(x_unhexed) # Outputs b'test'

x_ascii = str(x_unhexed,'ascii')
print(x_ascii) # Outputs test
