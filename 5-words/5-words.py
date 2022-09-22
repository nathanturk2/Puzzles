from copy import copy
from time import time
words=open('words_alpha.txt','r').read().split('\n')
valid_words=[]
for w in words:
    if len(w)==5:
        valid_words.append(w)

def bin_search(l,x,ascending=True):
    start=0
    end=len(l)-1
    while start<=end:
        mid=(start+end)//2
        if l[mid]==x:
            return mid
        if (l[mid]>x)==ascending:
            end=mid-1
        else:
            start=mid+1
    return start

def bin2num(b):
    result=0
    change=1
    length=len(b)
    while len(b)>0:
        result+=int(b[-1])*change
        b=b[:-1]
        change*=2
    return result

def word2freq(word):
    # Sorting the letters from least common to most common improves performance signifficantly.
    alphabet="qjzxvkwyfbghmpduclsntoirae"
    s=0
    for l in word:
        s=s|(1<<(25-alphabet.index(l)))
    return s

def count(freq):
    c=0
    while freq>0:
        freq=(freq-1)&freq
        c+=1
    return c

def earliest(freq):
    c=0
    while freq>0:
        freq=freq//2
        c+=1
    return c-1

def next_possible(w):
    freq=lw_freq[w]
    e=earliest(lw_freq[w])
    result=0
    c=0
    i=e-1
    while c<5 and i>=0:
        if (1<<i)&freq==0:
            result=result|(1<<i)
            c+=1
        i-=1
    return result

def num2bin(n):
    result=""
    while n>0:
        result=str(n%2)+result
        n//=2
    result="0"*(26-len(result))+result
    return result

def intersect(a,b,ascending=True):
    c=[]
    ca,cb=0,0
    while ca<len(a) and cb<len(b):
        if a[ca]==b[cb]:
            c.append(a[ca])
            ca+=1
            cb+=1
        elif (a[ca]>b[cb])==ascending:
            cb+=1
        else:
            ca+=1
    return c

def intersect2(a,b):
    return set(a)&set(b)

def find_limit(total):
    c=0
    i=0
    while i<=25 and c<2:
        if (1<<(25-i))&total==0:
            c+=1
        i+=1
    return i-1

def find_cutoff(l,total=0):
    limit=find_limit(total)
    return bin_search(l,1<<(25-limit),False)

start_time=time()

sw_freq=set()
dw_freq=dict()
for w in valid_words:
    r=word2freq(w)
    if count(r)==5:
        sw_freq.add(r)
        if not(r in dw_freq.keys()):
            dw_freq[r]=[w]
        else:
            dw_freq[r].append(w)

lw_freq=sorted(list(sw_freq),reverse=True)
print("The list of words used (no repeat letters or anagreams) has a length of "+str(len(lw_freq))+".")

skips=[]
for w in range(len(lw_freq)):
    skip=set()
    p=next_possible(w)
    s=bin_search(lw_freq,p,False)
    while s<len(lw_freq):
        if lw_freq[w]&lw_freq[s]==0:
            skip.add(s)
        s+=1
    skips.append(skip)

def search(total=0,last_index=0,depth=0,possible=[]):
    limit=find_limit(total)
    cut=1<<(25-limit)
    if depth==0:
        end=find_cutoff(lw_freq,total)
        test=range(end)
    elif depth==1:
        test=sorted(list(skips[last_index]))
    else:
        sa=skips[last_index]
        test=sorted(list(intersect2(sa,possible)))
    if len(test)<5-depth:
        return []
    results=[]
    for w in test:
        if lw_freq[w]<cut:
            break
        if depth==0:
            print(str(round(w/(end-1)*100,2))+"%")
        result=lw_freq[w]|total
        if depth<4:
            s=search(result,w,depth+1,test)
            for r in s:
                results.append([lw_freq[w]]+r)
        else:
            results.append([lw_freq[w]])
    return results

alphabet="qjzxvkwyfbghmpduclsntoirae"
results=search()
legible_results=[]
for r in results:
    total=(1<<26)-1
    result=[]
    for w in r:
        total=total^w
        result.append(dw_freq[w])
    letter=alphabet[25-earliest(total)]
    result.append(["(missing: "+letter+")"])
    legible_results.append(result)

count=0
for r in legible_results:
    m=1
    line=[]
    for w in r:
        if len(w)==1:
            line.append(w[0])
        else:
            line.append("["+"|".join(w)+"]")
            m*=len(w)
    count+=m
    print(", ".join(line))
print("Found",len(results),"possible valid combinations, excluding anagrams.")
print("Accounting for anagrams,",count,"valid combinations were found.")
print("The program took",round(time()-start_time,2),"seconds to find these results.")
input()
