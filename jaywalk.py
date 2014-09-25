import random
import time
import math
import imp
import sys,tty,termios
import types

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd,termios.TCSADRAIN,settings)
        return ch

#read input
def get():
    while(1):
        inkey = _Getch()
        #loop accounts for multicharacter gets, such as arrow keys
        while(1):
            k=inkey()
            if k!='':break
        if k=='\x1b[A':
            return "up"
        elif k=='\x1b[B':
            return "down"
        elif k=='\x1b[C':
            return "right"
        elif k=='\x1b[D':
            return "left"
        elif k=='\x1b':
            break


class Monster(object):
    
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.isAlive=True
    
    def __repr__(self):
        if self.isAlive:
            return "%"
        else:
            return "x"

    def move(self,pRow,pCol,maxRow,maxCol):
        hDifference=pCol-self.col
        vDifference=pRow-self.row
        #monsters are hungry for players in their own row or players whose row is closer than their col
        if self.row==pRow or abs(hDifference)>=abs(vDifference):
            self.col=(self.col+((hDifference)/abs(hDifference)))%maxCol
        elif self.col==pCol or abs(vDifference)>abs(hDifference):
            self.row=(self.row+((vDifference)/abs(vDifference)))%maxRow



class Player(object):
    
    def __init__(self):
        #self.bombs=5
        self.isAlive=True
    
    def __repr__(self):
        return "&"

#class Bomb(object):
#    
#    def __init__(self, pRow, pCOl):
#        self.row=pRow
#        self.col=pCol
#        self.isActive=True
#    
#    def __repr__(self):
#        if isActive:
#            return "o"
#        else:
#            return None


class Game(object):

    def __init__(self):
        self.height=15
        self.width=25
        self.data=[]
        self.aliveMonsters=0
        self.monsterList=[]
        self.player=Player()
        self.player.row=5
        self.player.col=10
        for row in range(self.height):
            boardRow=[]
            for col in range(self.width):
                boardRow+=[' ']
            self.data+=[boardRow]

    def __repr__(self):
        s='\n'
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col]==' ':
                    s+='.'
                elif self.data[row][col]=='#':
                    s+='#'
                else:
                    s+=(repr(self.data[row][col]))

            s+= '\n'
        s+='\n\n'
        return s

    def newBoard(self):
        monsterCounter=0
        #obstacleCounter=0
        #maxObstacles=self.height*self.width/50
        #while obstacleCounter<=maxObstacles:
        #   col=random.randint(0,self.width-1)
        #   row=random.randint(0,self.height-1)
        #   self.data[row][col]='#'
        #   obstacleCounter+=1
        while monsterCounter<=10:
            col=random.randint(0,self.width-1)
            row=random.randint(0,self.height-1)
            if self.data[row][col]==' ':
                b=Monster(row,col)
                self.data[row][col]=b
                self.monsterList+=[b]
                monsterCounter+=1
        self.data[self.player.row][self.player.col]=self.player
        self.aliveMonsters=monsterCounter

    def clearSprites(self):
        for row in range(self.height):
            for col in range(self.width):
                if isinstance(self.data[row][col], Monster) or isinstance(self.data[row][col], Player):
                    self.data[row][col]=' '



    def playGame(self):
        self.newBoard()
        while self.player.isAlive and self.aliveMonsters>0:
            print(self)
            k=get()
            #self.canMove(self.player,k)
            if k=='up':
                self.player.row=(self.player.row-1)%len(self.data)
            elif k=='down':
                self.player.row=(self.player.row+1)%len(self.data)
            elif k=='left':
                self.player.col=(self.player.col-1)%len(self.data[1])
            elif k=='right':
                self.player.col=(self.player.col+1)%len(self.data[1])

            self.clearSprites()
            for monster in self.monsterList:
                if monster.isAlive:
                    monster.move(self.player.row,self.player.col,len(self.data),len(self.data[1]))
                    if self.data[monster.row][monster.col]!=' ':
                        monster.isAlive=False
                        self.data[monster.row][monster.col].isAlive=False
                        self.aliveMonsters-=1
                self.data[monster.row][monster.col]=monster
                if self.data[self.player.row][self.player.col]!=' ':
                    self.player.isAlive=False
            self.data[self.player.row][self.player.col]=self.player
        print("GG")