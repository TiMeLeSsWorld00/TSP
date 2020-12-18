import random

def randmtx(n,beginrand,endrand):
    with open('randmatrix.txt','w') as inff:
        for i in range(n):
            line=''
            for j in range(n):
                if j==i:
                    line+='0 '
                else:
                    line+=str(random.randint(beginrand,endrand))+' '
            line+='\n'
            inff.write(line)

randmtx(int(input()),0,100)