import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

cn = pd.read_csv("Weekend challenge\\files\\channel.csv", header=None)
cn = cn.to_numpy().reshape(len(cn))
cn = np.pad(cn, (0, 994), mode='constant', constant_values=0)

# frequency response of channel
cn_freq = fft(cn)

# read data files
df = pd.read_csv("Weekend challenge\files\file1.csv", header=None)
df = df.to_numpy().reshape(len(df))

# split into the OFDM blocks
blocks = np.reshape(df, (-1, 1056))

all_syms = np.array([])
for block in blocks:
    syms = fft(block[32:])
    syms = syms/cn_freq
    all_syms = np.append(all_syms, syms[1:512])

bits = ""

for sym in all_syms:
    if sym.real > 0 and sym.imag > 0:
        bits += "00"
    if sym.real < 0 and sym.imag > 0:
        bits += "01"
    if sym.real < 0 and sym.imag < 0:
        bits += "11"
    if sym.real > 0 and sym.imag < 0:
        bits += "10"

# bytes vector
bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]

# location of all the bytes with value 0
zeros = np.where(np.array(bytes_list) == 0)[0]

# length of file in bytes
length_vector = [chr(bytes_list[i]) for i in range(zeros[0]+1, zeros[1])]
length = 0
for i in range(len(length_vector)):
    length = length * 10 + int(length_vector[i])

raw_data = bits[(zeros[1]+1)*8:(zeros[1]+1+length)*8]
print(raw_data)
