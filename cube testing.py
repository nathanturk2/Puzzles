from copy import deepcopy
class Cube:
    def __init__(self):
        self.swaps = {'B': (29, 32, 35, 3, 4, 5, 6, 7, 8, 2, 10, 11, 1, 13, 14, 0, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 53, 30, 31, 52, 33, 34, 51, 42, 39, 36, 43, 40, 37, 44, 41, 38, 45, 46, 47, 48, 49, 50, 9, 12, 15),
        'D': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 42, 43, 44, 18, 19, 20, 21, 22, 23, 15, 16, 17, 27, 28, 29, 30, 31, 32, 24, 25, 26, 36, 37, 38, 39, 40, 41, 33, 34, 35, 51, 48, 45, 52, 49, 46, 53, 50, 47),
        'F': (0, 1, 2, 3, 4, 5, 17, 14, 11, 9, 10, 45, 12, 13, 46, 15, 16, 47, 24, 21, 18, 25, 22, 19, 26, 23, 20, 6, 28, 29, 7, 31, 32, 8, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 33, 30, 27, 48, 49, 50, 51, 52, 53),
        'L': (44, 1, 2, 41, 4, 5, 38, 7, 8, 15, 12, 9, 16, 13, 10, 17, 14, 11, 0, 19, 20, 3, 22, 23, 6, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 51, 39, 40, 48, 42, 43, 45, 18, 46, 47, 21, 49, 50, 24, 52, 53),
        'R': (0, 1, 20, 3, 4, 23, 6, 7, 26, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 47, 21, 22, 50, 24, 25, 53, 33, 30, 27, 34, 31, 28, 35, 32, 29, 8, 37, 38, 5, 40, 41, 2, 43, 44, 45, 46, 42, 48, 49, 39, 51, 52, 36),
        'U': (6, 3, 0, 7, 4, 1, 8, 5, 2, 18, 19, 20, 12, 13, 14, 15, 16, 17, 27, 28, 29, 21, 22, 23, 24, 25, 26, 36, 37, 38, 30, 31, 32, 33, 34, 35, 9, 10, 11, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53)}
        self.state=[]
        for f in range(6):
            self.state+=[f for i in range(9)]
        self.solvedState=self.state
    def __str__(self):
        return str(self.state)
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.state == other.state
        else:
            return False
    def make_move(self,move,cswap=-1):
        if cswap==-1:
            swap=self.swaps[move[0].upper()]
        else:
            swap=cswap
        nstate=[0]*54
        if move[0]==move[0].upper():
            for i in range(54):
                nstate[i]=self.state[swap[i]]
        else:
            for i in range(54):
                nstate[swap[i]]=self.state[i]
        self.state=nstate
    def make_moves(self,moves):
        for move in moves:
            self.make_move(move)
    def is_solved(self):
        return self.solvedState==self.state
    def make_swap(self,moves):
        store_state=self.state
        self.state=[i for i in range(54)]
        self.make_moves(moves)
        swap=self.state
        self.state=store_state
        return swap
    def perm_degree(self,moves):
        swap=self.make_swap(moves)
        store_state=self.state
        self.make_move('A',swap)
        c=1
        while not(store_state==self.state):
            self.make_move('A',swap)
            c+=1
        return c

def find_high_degree(cube,depth=5,search='R'):
    global r
    afound=''
    sfound=0
    for i in 'FBUDRLfbudrl':
        t=search+i
        ts=cube.perm_degree(search+i)
        if ts>sfound:
            sfound=ts
            afound=t
    if depth>0 and ts>1:
        for i in 'FBUDRLfbudrl':
            branch=find_high_degree(cube,depth-1,search+i)
            t=branch[0]
            ts=branch[1]
            if ts>sfound:
                sfound=ts
                afound=t
    return [afound,sfound]
r=0
mycube=Cube()
while True:
    moves=input("Moves to try: ")
    result=mycube.perm_degree(moves)
    print("It took",result,"steps to repeat.")
    print("This takes a grand total of",result*len(moves),"quarter turns to execute.\n")
