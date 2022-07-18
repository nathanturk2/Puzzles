import numpy as np
from random import randint
from copy import deepcopy
from math import log
valid_words=open('allowed-guesses.txt','r').read().split('\n')
possible_answers=open('answers.txt','r').read().split('\n')
valid_words+=possible_answers
alphabet="abcdefghijklmnopqrstuvwxyz"

def get_freq(word):
	freq=np.array([0 for i in range(len(alphabet))])
	for c in word:
		freq[alphabet.index(c)]+=1
	return freq

def get_clue(answer,guess):
	freq=get_freq(answer)
	for c in range(len(guess)):
		if answer[c]==guess[c]:
			i=alphabet.index(guess[c])
			freq[i]-=1
	colours=""
	for c in range(len(guess)):
		i=alphabet.index(guess[c])
		if answer[c]==guess[c]:
			colours+="2"
		elif freq[i]>0:
			freq[i]-=1
			colours+="1"
		else:
			colours+="0"
	return colours

def narrow(possible,guess,clue):
	new_possible=[]
	for word in possible:
		if get_clue(word,guess)==clue:
			new_possible.append(word)
	return new_possible

def get_clue_freq(possible,guess):
	d=dict()
	for word in possible:
		nclue=get_clue(word,guess)
		if not(nclue in d):
			d[nclue]=1
		else:
			d[nclue]+=1
	return d

def best_guess(possible,valid_words):
	to_remove=[]
	for g in range(len(valid_words)):
		guess=valid_words[g]
		gain_sum=0
		clue_freq=get_clue_freq(possible,guess)
		for clue in clue_freq.keys():
			p=clue_freq[clue]/len(possible)
			gain_sum+=p*log(1/p,2)
		if g==0 or gain_sum>best_gain:
			best_gain=gain_sum
			best_guess=guess
		if gain_sum==0:
			to_remove.append(g)
	to_remove.reverse()
	for r in to_remove:
		valid_words.pop(r)
	print("\nExpected info gain:",round(best_gain,4),"bits")
	return best_guess

def worst_guess(possible,valid_words):
	to_remove=[]
	for g in range(len(valid_words)):
		guess=valid_words[g]
		gain_sum=0
		clue_freq=get_clue_freq(possible,guess)
		for clue in clue_freq.keys():
			p=clue_freq[clue]/len(possible)
			gain_sum+=p*log(1/p,2)
		if g==0 or gain_sum<best_gain:
			best_gain=gain_sum
			best_guess=guess
	print("\nExpected info gain:",round(best_gain,4),"bits")
	return best_guess

def absurd_guess(possible,valid_words):
	to_remove=[]
	for g in range(len(valid_words)):
		guess=valid_words[g]
		clue_freq=get_clue_freq(possible,guess)
		gain_sum=0
		for clue in clue_freq.keys():
			p=clue_freq[clue]/len(possible)
			gain_sum+=p*log(1/p,2)
		p=clue_freq[max(clue_freq,key=clue_freq.get)]/len(possible)
		worst_gain=log(1/p,2)
		if g==0 or worst_gain>best_gain:
			best_gain=worst_gain
			best_guess=guess
		if gain_sum==0:
			to_remove.append(g)
	to_remove.reverse()
	for r in to_remove:
		valid_words.pop(r)
	print("\nExpected info gain:",round(best_gain,4),"bits")
	return best_guess

for w in possible_answers:
	print(w)

self_play=input("Self-play? ") in ["y","yes","t","true"]
modes=["Wordle","Survivle","Absurdle"]
print("Modes:")
for m in range(len(modes)):
	print(str(m+1)+". "+modes[m])
mode=int(input("Pick a mode: "))
while not(mode>=1 and mode<=3):
	print("Error: not a mode")
	mode=int(input("Pick a mode: "))
print("\nPicked",modes[mode-1])
possible=deepcopy(possible_answers)
if mode==1:
	guess="salet"
elif mode==2:
	guess="qajaq"
	#guess=worst_guess(possible,valid_words)
else:
	#guess=input("First guess: ")
	guess="aesir"
	#guess=valid_words[randint(0,len(valid_words)-1)]
	#guess="redia"
guesses_made=[guess]
clues=[]
answer=possible_answers[randint(0,len(possible_answers)-1)]
if self_play and mode!=3:
	print("Answer:",answer)
	#answer=input("Answer: ")
while guess!=answer or not(self_play):
	print("Guess:",guess)
	if not(self_play):
		clue=input("Clue:  ")
	elif mode==3:
		clue_freq=get_clue_freq(possible,guess)
		clue=max(clue_freq,key=clue_freq.get)
		if clue=="22222" and len(possible)>1:
			possible.pop(possible.index(guess))
			clue=get_clue(guess,possible[0])
			break
		else:
			print("Clue: ",clue)
	else:
		clue=get_clue(answer,guess)
		print("Clue: ",clue)
	if clue=="22222":
		break
	clues.append(clue)
	old_n=len(possible)
	possible=narrow(possible,guess,clue)
	if len(possible)<=20:
		print("Possibilities:")
		for p in possible:
			print(p)
	if mode==2:
		valid_words=narrow(valid_words,guess,clue)
	print("Possible Answers:",len(possible))
	print("Actual info gain:",round(log(old_n/len(possible),2),4),"bits")
	if mode==2:
		if guesses_made==["qajaq"] and clue=="01000":
			guess="bubba"
			print("\nExpected info gain: 1.4284 bits")
		elif guesses_made==["qajaq"] and clue=="00000":
			guess="xylyl"
			print("\nExpected info gain: 2.1656 bits")
		elif guesses_made==["qajaq","xylyl"] and clues==["00000","00000"]:
			guess="kudzu"
			print("\nExpected info gain: 2.3824 bits")
		else:
			guess=worst_guess(possible,valid_words)
	elif len(possible)>3:
		if mode==1:
			guess=best_guess(possible,valid_words)
		else:
			guess=absurd_guess(possible,valid_words)
	else:
		print()
		guess=best_guess(possible,possible)
	guesses_made.append(guess)
print("Guess:",guess)
print("Finished after "+str(len(guesses_made))+" guesses!")

