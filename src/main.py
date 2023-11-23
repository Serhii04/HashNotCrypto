from hashlib import sha3_256
import math
import random
import binascii
import hashlib

import matplotlib.pyplot as plt
import numpy as np



def sha_from_int(message: int) -> str:
    """return hash of int value message"""
    return sha3_256(bytes.fromhex(hex(message)[2:])).hexdigest()

def first_attack(m: int, expanded_output: bool=False) -> int or (int, int):  # m means message
    """Find first message, that is bigger than m, but have the same hash
    
    Args:
        m (int): some message.
        expanded_output (bool): if True, reeturns aditional information

    Returns:
        tm (int): message that has the same hase as m.
    """
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

def second_attack(m: int) -> int:
    """search for a message, that has the same hash
    
    Args:
        m (int): some message.

    Returns:
        tm (int): message that has the same hase as m.
    """
    m_hash = sha3_256(bytes.fromhex(hex(m)[2:])).hexdigest()
    
    b=pow(2, math.ceil(m.bit_length() / 4))
    
    tm = m ^ random.randint(a=0, b=b)
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()

    while tm_hash[-4:] != m_hash[-4:]:
        tm = m ^ random.randint(a=0, b=b)
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()

    return tm

def custom_find(hashes: [str, ...], element: str) -> int | None:
    k = 4
    
    for i, hash in enumerate(hashes):
        if hash[-k:] == element[-k:]:
            return i

    return None

def first_birstday_attack(m: int) -> (int, int):
    tm = m
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
    hashes = [tm_hash]

    temp = None
    while temp is None:
        tm += 1
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
        temp = custom_find(hashes=hashes, element=tm_hash)
        hashes.append(tm_hash)

    tm2 = m + temp
    
    return tm, tm2

def second_birstday_attack(m: int) -> (int, int):
    tm = m
    tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
    hashes = [tm_hash]
    messages = [tm]
    b=pow(2, math.ceil(m.bit_length() / 4))

    temp = None
    while temp is None:
        tm = m ^ random.randint(a=0, b=b)
        tm_hash = sha3_256(bytes.fromhex(hex(tm)[2:])).hexdigest()
        temp = custom_find(hashes=hashes, element=tm_hash)
        hashes.append(tm_hash)
        messages.append(tm)

    tm2 = messages[temp]
    
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


    fig, ax = plt.subplots()
    ax.plot(t, s)
    text = f"{title}, Mf = {M:0.2f}, Df = {D:0.2f}."
    s = np.array([M for i in range(k)])
    ax.plot(t, s, "k")
    ax.set(xlabel='Test number', ylabel='Number of iterations', title=text)
    # ax.text(0.5, 0.5, 'matplotlib', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.grid()
    
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.show()

def main():
    PIB = "Волинець Сергій Анатолійович"
    print(PIB)

    PIB_int = int(PIB.encode("utf-8").hex(), 16)
    print(f"Hex of PIB: {hex(PIB_int)}")

    print(f"Hash of PIB: {sha_from_int(PIB_int)}")

    first = first_attack(m=PIB_int)
    print("")
    print("First attack")
    print(f"Goten message: {hex(first)}")
    print(f"Goten hash: {sha_from_int(first)}")

    second = second_attack(m=PIB_int)
    print("")
    print("Second attack")
    print(f"Goten message: {hex(second)}")
    print(f"Goten hash: {sha_from_int(second)}")


    tm1, tm2 = first_birstday_attack(m=PIB_int)
    print("")
    print("First birstday attack")
    print(f"Goten message1: {hex(tm1)}")
    print(f"Goten hash1: {sha_from_int(tm1)}")
    print(f"Goten message2: {hex(tm2)}")
    print(f"Goten hash2: {sha_from_int(tm2)}")

    tm1, tm2 = second_birstday_attack(m=PIB_int)
    print("")
    print("Second birstday attack")
    print(f"Goten message1: {hex(tm1)}")
    print(f"Goten hash1: {sha_from_int(tm1)}")
    print(f"Goten message2: {hex(tm2)}")
    print(f"Goten hash2: {sha_from_int(tm2)}")

    graph_info_about(func=first_attack, m=PIB_int, title="First attack")


if __name__ == "__main__":
    main()