"""
This file contains constant values and helper functions used in the project
"""


KN=200e-6
W_L_N = 200/80
ALPHA = 2
r0 = 74e3
I0 = 13.24e-6
VDSAT = 0.2
B = 4


T0 = 300e-12
Nrow = 512
Cblc = 0.56e-15

Vpre = 1
Ncol = 256

Vt = 0.44
Vt_var = 0.015





def decToBi(n,B):
    n_copy = n
    binary = list()
    while n_copy!=0:
        binary.append(n_copy %2)
        n_copy = n_copy // 2
    while len(binary)<B:
        binary.append(0)
    return binary[::-1]
