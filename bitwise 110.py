from copy import copy
from time import sleep
def decode(n):
    t=copy(n)
    s=""
    while t!=0:
        s=s+["  ","[]"][t%2]
        t=t>>1
    return s
sleep(3)
count=0
w=1
l=(1<<99)-1
for i in range(int(input("Generations: "))):
    print(decode(w))
    a=w
    w=w<<1
    b=w
    c=w<<1
    w=(~a & b) | (b & ~c) | (~b & c)
    w=(w>>1)
