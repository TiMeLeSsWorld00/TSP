# -*- coding: utf-8 -*-
import numpy as np
import random
import math
import matplotlib.pyplot as plt

def f(x, W):
    sum = 0
    m = len(x)
    #print(m)
    for i in range(m-1):
       sum += W[int(x[i])][int(x[i+1])]
    sum += W[int(x[-1])][int(x[0])]
    return sum

def mutation(x):
    m = len(x)
    k = random.randint(0, m-2)
    x[k], x[k+1] = x[k+1], x[k]

def сrossing(pop, prob):
    n = int(len(pop)/2)
    for i in range(n):
        pop[n+i] = pop[i]
        m = len(pop[i])
        r = random.randint(0, m-1)
        l = random.randint(0, m-1)
        while r==l:
            l = random.randint(0, m-1)
        if l<r:
            l, r = r, l
        for j in range(math.ceil((l-r)/2)):
            pop[i][r + j], pop[i][l - j] = pop[i][l - j], pop[i][r + j] 
        if (1+random.randint(0, 99)<=prob):
            mutation(pop[i])
            
            
def qsort(pop, W, n):
    ii = 0
    #print(ii)
    jj = n-1 #Указатели в начало и в конец массива
    #print(jj)
    mid = f(pop[int(n / 2)], W) #Центральный элемент массива
    #Делим массив
    #for i in range(ii, jj + 1):
     #   print(f(pop[i], W))
    #print()
    while True:#ii<=jj:
        #Пробегаем элементы, ищем те, которые нужно перекинуть в другую часть
        #В левой части массива пропускаем(оставляем на месте) элементы, которые меньше центрального
        while f(pop[ii], W) < mid:
            #print(ii, " ", mid, " ", f(pop[ii], W))
            ii+=1
           # print(ii, " ", mid, " ", f(pop[ii], W))
        #print()
        #В правой части пропускаем элементы, которые больше центрального
        while f(pop[jj], W) > mid:
            jj-=1
            #print(jj, " ", mid)
        #Меняем элементы местами
        
        if ii<=jj:
            #print(pop)
            #print("swap2", pop[ii], pop[jj])
            c=[]
            for ipp in range(len(pop[ii])):
                c.append(pop[ii][ipp])
            #print(c)
            pop[ii] = pop[jj]
            pop[jj]=c
           # print("swap3", pop[ii], pop[jj])
            ii+=1
            jj-=1
        
        if ii>jj:
            break
        #Рекурсивные вызовы, если осталось, что сортировать
    if jj>0:
        #"Левый кусок"
        qsort(pop, W, jj + 1)
    if ii<n:
        #"Правый кусок"
        qsort(pop, W, n - ii)
        
      
def randWeights(W):
    #f = open('out.txt', 'r')
    #for i in range(len(W)):
     #   for j in range(0, len(W[i])):
      #      W[i][j] = f.read()
    n = len(W)
    for i in range(n):
        for j in range(0, len(W[i])):
            W[i][j] = random.randint(2, 100)
            W[j][i] = W[i][j];
        for i in range(n):
            W[i][i] = -1

def randPopulation(pop):
    m = len(pop[0])
    numbers=[i for i in range(m)]
    for i in range (2*n):
        random.shuffle(numbers)
        pop[i]=numbers
        
    



n = 400 #число особей в популяции
m = 100 #число городов
prob = 20 #вероятность мутации 
if n % 2 != 0: 
    print("think again")
pop = np.zeros((2*n, m), dtype = np.int32)
T = 20 # число поколений 
W = np.zeros((m, m), dtype = np.int32)
randWeights(W)
for i in W:
    print(*i)
#print(W)
for i in range(1):
    randPopulation(pop)

    minn = f(pop[0], W)
    gminn=[]
#print(pop)
    for t in range(T):
        if minn>f(pop[0], W):
            minn = f(pop[0], W)
            print(t, "-", minn)
        gminn.append(f(pop[0],W))
        сrossing(pop, prob)
    #print("cross\n")
    #for i in pop:
     #   print(i, " ", f(i, W))
        qsort(pop, W, len(pop))
   # print(123)
    #sorted(pop, key = lambda x: f(x, W), reverse = True)
#print(pop)    
    #print("sort\n")
#for i in pop:
   # print(*i, " ", f(i, W))
   # mid = f(pop[int(n / 2)], W)
    xnew=[i for i in range(T)]
    plt.plot(xnew,gminn,'b')

plt.grid(True)
plt.show()

print(pop[0])


