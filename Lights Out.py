from copy import copy
from random import randint
def make_mask(h,w):
    a=0
    for r in range(h):
        a*=2
        for c in range(w):
            a*=2
            a+=1
        a*=2
    return a

def make_action(n):
    m=[2,7,2]
    a=0
    for i in range(len(m)):
        a = a^(m[i]<<i*(n+2)>>1)
    return a

def decode(n):
    return str(bin(n))[2::]

def flip(m,ma,sn,mn):
    m=m^(ma<<int(mn/sn)*(sn+2)+mn%sn>>sn+1)
    return m

def display(m,sn,board=True):
    s=decode(m)[::-1]
    s+=((sn*(sn+2*board))-len(s))*"0"
    print(" "+"__"*sn)
    for i in range(sn):
        print("|"+"".join([["--","[]"][int(c)] for c in s[1+i*(sn+2*board):1+i*(sn+2*board)+sn]])+"|")
    print(" "+"¯¯"*sn)
    print()

def make_puzzle(n):
    m=0
    ma=make_action(n)
    for i in range(n**2):
        if randint(0,1):
            m=flip(m,ma,n,i)
    return mask & m

size=int(input("Board size: "))
solutions=[]
ma=make_action(size)
mask=make_mask(size,size)
mmask=make_mask(1,size)
m=mask & flip(0,ma,size,40)#make_puzzle(size)
print("Solving:")
display(m,size)
moves=[]
for i in range(2**size):
    mc=0
    nm=copy(m)
    s=decode(i)[::-1]
    for mn in range(len(s)):
        if s[mn]=="1":
            nm=flip(nm,ma,size,mn)
            mc+=1
    s=s+(size-len(s))*"0"
    for i in range(size-1):
        b=decode(((nm>>(i*(size+2)))&mmask)>>1)
        b=(size-len(b))*"0"+b
        b=b[::-1]
        s+=b
        for mn in range(len(b)):
            if b[mn]=="1":
                nm=flip(nm,ma,size,mn+(i+1)*size)
                mc+=1
    nm=nm&mask
    if nm==0:
        solutions.append(s+(size-len(s))*"0")
        print("Solution",len(solutions))
        print(" "+"__"*size)
        print("\n".join(["|"+"".join([["--","[]"][int(a)] for a in s[c*size:(c+1)*size]])+"|" for c in range(size)]))
        print(" "+"¯¯"*size)
        print("Moves:",mc,"\n"*2)
        moves.append(mc)
print("Solutions:",len(solutions))
print("Minimum solution:",min(moves),"moves")

