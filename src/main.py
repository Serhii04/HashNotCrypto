from hashlib import sha3_256
import math
import random
import binascii
import hashlib

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st 



def sha_from_int(message: int) -> str:
    """return hash of int value message"""
    return sha3_256(bytes.fromhex(hex(message)[2:])).hexdigest()

def first_attack(m: int, expanded_output: bool=False) -> int or (int, int):  # m means message
    m_hash = sha_from_int(m)
    
    tm = m + 1  # t means temp
    tm_hash = sha_from_int(tm)

    while tm_hash[-4:] != m_hash[-4:]:
        tm += 1
        tm_hash = sha_from_int(tm)

    if expanded_output:
        iteration = tm - m
        return tm, iteration

    return tm

def second_attack(m: int, expanded_output: bool=False) -> int:
    m_hash = sha3_256(bytes.fromhex(hex(m)[2:])).hexdigest()
    
    b=pow(2, math.ceil(m.bit_length() / 4))
    
    tm = m ^ random.randint(a=0, b=b)
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()

    iteration = 0
    while tm_hash[-4:] != m_hash[-4:]:
        tm = m ^ random.randint(a=0, b=b)
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
        iteration += 1

    if expanded_output:
        return tm, iteration

    return tm

def custom_find(hashes: [str, ...], element: str) -> int | None:
    k = 8
    
    for i, hash in enumerate(hashes):
        if hash[-k:] == element[-k:]:
            return i

    return None

def first_birstday_attack(m: int, expanded_output: bool=False) -> (int, int):
    tm = m
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
    hashes = [tm_hash]

    iteration = 0
    temp = None
    while temp is None:
        tm += 1
        iteration += 1
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
        temp = custom_find(hashes=hashes, element=tm_hash)
        hashes.append(tm_hash)

    tm2 = m + temp

    if expanded_output:
        return (tm, tm2), iteration
    
    return tm, tm2

def second_birstday_attack(m: int, expanded_output: bool=False) -> (int, int):
    tm = m
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
    hashes = [tm_hash]
    messages = [tm]
    b=pow(2, math.ceil(m.bit_length() / 4))

    temp = None
    iteration = 0
    while temp is None:
        tm = m ^ random.randint(a=0, b=b)
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
        temp = custom_find(hashes=hashes, element=tm_hash)
        hashes.append(tm_hash)
        messages.append(tm)
        iteration += 1

    tm2 = messages[temp]

    if expanded_output:
        return (tm, tm2), iteration
    
    return tm, tm2

def graph_info_about(m: int, func, title: str="", k: int=100):
    t = np.arange(0, k, 1)
    # s = 1 + np.sin(2 * np.pi * t)
    s = np.zeros(k)

    b = pow(2, m.bit_length()//8)
    for i in range(k):
        tm = m + random.randint(a=0, b=b)
        rez, iterations = first_attack(m=tm, expanded_output=True)
        s[i] = iterations

    M = np.mean(s)
    D = np.std(s)
    gama = 0.95
    # gama_a, gama_b = st.norm.interval(confidence=gama, loc=np.mean(s), scale=st.sem(s))
    # print(f"norm: ({gama_a}, {gama_b})")
    gama_a, gama_b = st.t.interval(df=len(s)-1, confidence=gama, loc=np.mean(s), scale=st.sem(s))

    fig, ax = plt.subplots(1, 2)

    text = f"{title}, Mf = {M:0.2f}, Df = {D:0.2f},\n{gama}-confidence interval = ({gama_a:0.2f}, {gama_b:0.2f})."
    fig.suptitle(text)
    fig.set_size_inches(h=5, w=10)

    ax[0].plot(t, s)
    M_line_y = np.array([M for i in range(k)])
    ax[0].plot(t, M_line_y, "k")
    ax[0].set(xlabel='Test number', ylabel='Number of iterations')
    ax[0].grid()
    ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    n_bins = 30
    ax[1].hist(s, bins=n_bins)
    ax[1].grid()
    ax[1].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax[1].set(xlabel='Number of iterations', ylabel='Count')

    plt.show()

def main():
    PIB = "Волинець Сергій Анатолійович"
    print(f"PIB = {PIB}")
    PIB_int = int(PIB.encode("utf-8").hex(), 16)
    print(f"Hex of PIB: {hex(PIB_int)}")
    print(f"Hash of PIB: {sha_from_int(PIB_int)}")

    # first = first_attack(m=PIB_int)
    # print("")
    # print("First attack")
    # print(f"Goten message: {hex(first)}")
    # print(f"Goten hash: {sha_from_int(first)}")

    # second = second_attack(m=PIB_int)
    # print("")
    # print("Second attack")
    # print(f"Goten message: {hex(second)}")
    # print(f"Goten hash: {sha_from_int(second)}")


    # tm1, tm2 = first_birstday_attack(m=PIB_int)
    # print("")
    # print("First birstday attack")
    # print(f"Goten message1: {hex(tm1)}")
    # print(f"Goten hash1: {sha_from_int(tm1)}")
    # print(f"Goten message2: {hex(tm2)}")
    # print(f"Goten hash2: {sha_from_int(tm2)}")

    # tm1, tm2 = second_birstday_attack(m=PIB_int)
    # print("")
    # print("Second birstday attack")
    # print(f"Goten message1: {hex(tm1)}")
    # print(f"Goten hash1: {sha_from_int(tm1)}")
    # print(f"Goten message2: {hex(tm2)}")
    # print(f"Goten hash2: {sha_from_int(tm2)}")

    graph_info_about(func=first_attack, m=PIB_int, title="First attack")
    graph_info_about(func=second_attack, m=PIB_int, title="Second attack")
    graph_info_about(func=first_birstday_attack, m=PIB_int, title="First birsday attack")
    graph_info_about(func=second_birstday_attack, m=PIB_int, title="Second birsday attack")


if __name__ == "__main__":
    main()

