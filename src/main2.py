import numpy as np
import random
import hashlib
from bisect import bisect, bisect_left

from typing import Callable
def alg1(K: int, L: int, R: Callable, n: int, h: Callable) -> [[int, int], ...]:
    # x = np.zeros((K, 2), dtype=int)
    x = [[0 for i in range(2)] for j in range(K)]
    max_allow_x = pow(2, n) - 1
    
    for i in range(K):
        x[i][0] = random.randint(0, max_allow_x)
        x_cur = x[i][0]
        for j in range(L):
            # x[i, j + 1] = h(R(x[i, j]))
            x_cur = h(R(x_cur))

        x[i][1] = x_cur

    return x
def bisect_left_castom(a, x, m, lo=0, hi=None, *, key=None,):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    # Note, the comparison uses "<" to match the
    # __lt__() logic in list.sort() and in heapq.
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if key(a[mid]) % m < x % m:
                lo = mid + 1
            else:
                hi = mid
    return lo


def index(a, x, m):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left_castom(a, x, m=m, key=lambda x: (x[1]))
    if i != len(a) and a[i][1] % m == x % m:
        return i
    
    return None
def alg2(K: int, L: int, R: Callable, x: [[int, int], ...], hash_val, n: int, h: Callable) -> int:
    m = pow(2, n)
    y = hash_val
    x_s = sorted(x, key=lambda x: x[1] % m)

    for j in range(L):
        id = index(x_s, y, m)
        if id is not None:
            x_ = x_s[id][0]

            for m_ in range(L - (j + 1)):
                x_ = h(R(x_))

            r_val = R(x_)
            if h(r_val) % m == hash_val % m:
                return r_val
            else:
                return None
        

        # for i in range(K):
        #     # if x[i][1] % m == y % m:
        #     if x[i][1] == y:
        #         x_ = x[i][0]

        #         for m_ in range(L - (j + 1)):
        #             x_ = h(R(x_))

        #         r_val = R(x_)
        #         if h(r_val) % m == hash_val % m:
        #             return r_val
        #         else:
        #             return None

        y = h(R(y))

    return None
def alg2_slow(K: int, L: int, R: Callable, x: [[int, int], ...], hash_val, n: int, h: Callable) -> int:
    m = pow(2, n)
    y = hash_val
    x_s = sorted(x, key=lambda x: x[1] % m)

    for j in range(L):
        for i in range(K):
            # if x[i][1] % m == y % m:
            if x[i][1] == y:
                x_ = x[i][0]

                for m_ in range(L - (j + 1)):
                    x_ = h(R(x_))

                r_val = R(x_)
                if h(r_val) % m == hash_val % m:
                    return r_val
                else:
                    return None

        y = h(R(y))

    return None
def sha_int_to_int(message: int) -> str:
    """return hash of int value message"""
    return int("0x" + hashlib.sha256(str(message).encode('ASCII')).hexdigest(), base=16)
# Task
def attack1(K: int, L: int, n: int, rand_v_hash):
    # _r = random.randint(0, pow(2, 128 - n) - 1)
    _r =  0x3762d7a3fb50e749963972a36f9c
    m = pow(2, n)

    def R(x: int):
        return _r + (x % m)
    
    x = alg1(K=K, L=L, R=R, n=n, h=sha_int_to_int)
    
    # for l in x:
    #     print(l)

    preimage = alg2(K=K, L=L, R=R, x=x, hash_val=rand_v_hash, n=n, h=sha_int_to_int)
    
    return preimage

if __name__ == "__main__":
    for _ in range(20):
        K = pow(2, 10)
        L = pow(2, 5)
        n = 16
        
        rand_v = random.randint(0, pow(2, 256) - 1)
        rand_v_hash = sha_int_to_int(rand_v)


        preimage = attack1(K=K, L=L, n=n, rand_v_hash=rand_v_hash)

        if preimage is None:
            print('"Прообраз не знайдено"')
        else:
            preimage_hash = sha_int_to_int(preimage)
            print(f"rand_x = {hex(rand_v)}")
            print(f"rand_x_hash = {hex(rand_v_hash)}")
            print(f"preimage = {hex(preimage)}")
            print(f"preimage_hash = {hex(preimage_hash)}")
def test_attack1(N: int):
    if N < 1:
        return [None]

    n = 16

    K_vals = [pow(2, 10), pow(2, 12), pow(2, 14)]
    L_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
    results = [[0 for j in range(3)] for i in range(3)]

    for i in range(3):
        for j in range(3):
            for k in range(N):
                rand_v = random.randint(0, pow(2, 256) - 1)
                rand_v_hash = sha_int_to_int(rand_v)
                preimage = attack1(K=K_vals[i], L=L_vals[j], n=n, rand_v_hash=rand_v_hash)

                if preimage is not None:
                    results[i][j] += 1
            
            results[i][j] = results[i][j] / N

    return results
rez = test_attack1(N = 0)

for l in rez:
    print(l)
        
# Task 2
def alg2_extended(K: int, L: int, tables: [[[int, int], ...], ...], r_values: [int, ...], hash_val, n: int, h: Callable) -> int:
    m = pow(2, n)
    y = [hash_val for i in range(K)]
    sorted_tables = []
    for table in tables:
        sorted_tables.append(sorted(table, key=lambda x: x[1] % m))

    # x_s = sorted(x, key=lambda x: x[1] % m)

    for j in range(L):
        for i in range(K):
            id = index(sorted_tables[i], y[i], m)
            if id is not None:
                x_ = sorted_tables[i][id][0]

                for m_ in range(L - (j + 1)):
                    x_ = h(r_values[i] + (x_ % m))

                r_val = r_values[i] + (x_ % m)
                if h(r_val) % m == hash_val % m:
                    return r_val
                else:
                    return None
            

            y[i] = h(r_values[i] + (y[i] % m))

    return None
def attack2(K: int, L: int, n: int, rand_v_hash):
    m = pow(2, n)
    
    tables = []
    r_values = []
    for i in range(K):
        _r = random.randint(0, pow(2, 128 - n) - 1)

        def R(x: int):
            return _r + (x % m)
        
        alg1_rez = alg1(K=K, L=L, R=R, n=n, h=sha_int_to_int)
        tables.append(alg1_rez)
        r_values.append(_r)


    # for l in x:
    #     print(l)

    preimage = alg2_extended(K=K, L=L, tables=tables, r_values=r_values, hash_val=rand_v_hash, n=n, h=sha_int_to_int)
    
    return preimage
if __name__ == "__main__":
    for _ in range(20):
        K = pow(2, 5)
        L = pow(2, 5)
        n = 16
        
        rand_v = random.randint(0, pow(2, 256) - 1)
        rand_v_hash = sha_int_to_int(rand_v)


        preimage = attack2(K=K, L=L, n=n, rand_v_hash=rand_v_hash)

        if preimage is None:
            print('"Прообраз не знайдено"')
        else:
            preimage_hash = sha_int_to_int(preimage)
            print(f"rand_x = {hex(rand_v)}")
            print(f"rand_x_hash = {hex(rand_v_hash)}")
            print(f"preimage = {hex(preimage)}")
            print(f"preimage_hash = {hex(preimage_hash)}")
def test_attack2(N: int):
    if N < 1:
        return [None]

    n = 16

    K_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
    L_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
    results = [[0 for j in range(3)] for i in range(3)]

    for i in range(3):
        for j in range(3):
            for k in range(N):
                rand_v = random.randint(0, pow(2, 256) - 1)
                rand_v_hash = sha_int_to_int(rand_v)
                preimage = attack2(K=K_vals[i], L=L_vals[j], n=n, rand_v_hash=rand_v_hash)

                if preimage is not None:
                    results[i][j] += 1
            
            results[i][j] = results[i][j] / N

    return results

from datetime import datetime
rez2 = test_attack2(N = 0)

for l in rez2:
    print(l)
        
# Halman Theorem (Probability)
from mpmath import mpf, mpc, mp, mpmathify, fadd, fdiv, fsub, fmul
from math import trunc
def calc_halman_probability(n, K, L):
    # m - K, t - L
    N = pow(2, n)

    sum = 0 
    for i in range(1, K + 1):
        for j in range(L):
            # sum += pow(mpmathify(1) - mpmathify(mpmathify(i * L) / mpmathify(N)), j + 1)
            p = fsub(1, fdiv(i * L, N))
            ppp = 1
            for i in range(j + 1):
                ppp = fmul(ppp, p)

            sum = fadd(sum, ppp)

    return fdiv(sum, N)
# def calc_halman_probability(n, K, L):
#     # m - K, t - L
#     N = pow(2, n)

#     sum = 0 
#     for i in range(1, K + 1):
#         p = fsub(1, fdiv(i * L, N))

#         ppp = 1
#         for t in range(L + 1):
#             ppp = fmul(ppp, p)

#         sum = fadd(sum, fdiv(fsub(1, ppp), fsub(1, p)))
#         sum = fsub(sum, 1)


#     return fdiv(sum, N)
K_vals = [pow(2, 10), pow(2, 12), pow(2, 14)]
L_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
results = [[0 for j in range(3)] for i in range(3)]

for i in range(3):
    for j in range(3):
        p = calc_halman_probability(n=16, K=K_vals[i], L=L_vals[j])
        # print(p)
        print(f"{int(p* 100)}\% & ", end="")
    
    print("")
K_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
L_vals = [pow(2, 5), pow(2, 6), pow(2, 7)]
results = [[0 for j in range(3)] for i in range(3)]

for i in range(3):
    for j in range(3):
        p = calc_halman_probability(n=16, K=K_vals[i], L=L_vals[j])
        results[i][j] = 1 - pow(1 - p, K_vals[i])



print("K tables probabilities")
for l in results:
    for i in l:
        print(f"{int(i * 100)}\% & ", end="")
    
    print("")