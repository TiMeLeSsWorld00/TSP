#Метод ветвей и границ
import math
import numpy as np

def lenght_way(C, way):#Рассчитывает длинну пути
    summ=0
    for i in range(len(way)):
        summ+=C[way[i][0]][way[i][1]]
    return summ

def minline(C):
    #C - матрица, у которой считаем минимум по строкам
    sumh = 0
    for i in range(len(C)):
        minh = math.inf
        for j in range(len(C[i])):
            if C[i][j] < minh:
                minh = C[i][j]
        for j in range(len(C[i])):
            if minh != math.inf:
                C[i][j] -=minh
        if minh != math.inf:
            sumh +=minh
    return sumh


def mincolumn(C):
    #C - матрица, у которой считаем минимум по столбцам
    sumh = 0
    for i in range(len(C)):
        minh = math.inf
        for j in range(len(C[i])):
            if C[j][i] < minh:
                minh = C[j][i]
        for j in range(len(C[i])):
            if minh != math.inf:
                C[j][i] -=minh
        if minh != math.inf:
            sumh +=minh
    return sumh


def tet(C):# Выбирает тету, то есть путь по которому мы идём или не идём
    #C - матрица, у которой считаем максимум среди величин нулей(сумма минимального элемента в строке и столбце на пересечении которых 0)
    tet_dict=dict()
    for i in range(len(C)):
        for j in range(len(C[i])):
            if C[i][j] == 0:
                mintet_line = math.inf
                mintet_column = math.inf
                for k in range(len(C[i])):
                    if mintet_line>C[i][k] and k!=j:
                        mintet_line = C[i][k]
                for l in range(len(C)):
                    if mintet_column > C[l][j] and l!=i:
                        mintet_column = C[l][j]
                tet_dict[(i,j)]=mintet_column+mintet_line
    maxtet = -math.inf
    maxtet_i = tuple()
    for i in tet_dict:
        if maxtet < tet_dict[i]:#не понятно что делать в случае если значения тет будут совпадать
            maxtet = tet_dict[i]
            maxtet_i = i
    return maxtet_i[0], maxtet_i[1],  maxtet    # maxtet_i[0] -строка, maxtet_i[1] - столбец maxtet - значение

def added(ep, str, i, j, minh, ep_priv, flag, tet=0):#Добавляет в структуру пути
    #ep - дерево оценок, str - левая\правая ветвь, i\j - строка\столбец с максимальной величиной нуля
    #левая - идем через путь i-j, правая - не идем
    #minh - суммa минимальных элементов по строкам и столбцам и оценка матрицы
    #ep_priv - значение родительского элемента
    #flag - 0 если не пошли, 1 если пошли
    #value = minh + ep_priv
    if str == "left":
        ep.append(["left", [i,j], ep_priv, flag])
    else:
        ep.append(["right", [i,j], ep_priv, flag])

def do_in_left(C,ep_line, ep_col):#что мы делаем если идём выбранным путём
    #С - матрица, в которой вычеркиваем ep_line строку и ep_col столбец, не меняя индексов матрицы
    for j in range(len(C)):
        C[ep_line][j] = math.inf
        C[j][ep_col] = math.inf
    C[ep_col][ep_line]=math.inf

def do_in_right(C,ep_line, ep_col):
    C[ep_line][ep_col] = math.inf

def sort_way_kostil(way):#Помогает выявлять малые циклы в nocyclefortoday
    i=0
    while i<len(way):
        flag=1
        c=[]
        first=way[i][1]
        endd=way[i][0]
        for j in range(i+1,len(way)):
            if way[j][0]==first:
                c.append(way[j])
                way[j]=way[i+1]
                way[i+1]=c.pop()
            if way[j][1]==endd:
                c.append(way[i])
                way[i]=way[j]
                for k in range(i+1,j+1):
                    c.append(way[k])
                    way[k] = c.pop(0)
                flag=0
        if flag:
            i+=1


def sort_way(way,n):#Привеодит путь к зацикленному виду
    beginset=set()
    endset=set()
    for i in way:
        beginset.add(i[0])
        endset.add(i[1])
    for i in range(n):
        if i not in beginset:
            beginn=i
        if i not in endset:
            endd=i
    way.append([beginn,endd])
    for i in range(len(way)):
        c=[]
        first=way[i][1]
        for j in range(i+1, len(way)):
            if way[j][0]==first:
                c.append(way[j])
                way[j]=way[i+1]
                way[i+1]=c[0]

def nocyclefortoday(C,ep):#Исключает возможность зацикливания
    mn=list()
    for i in ep:
        if i[0]=='left':
            mn.append(i[1])
    bad=list()
    sort_way_kostil(mn)
    for i in range(len(mn)):
        beginn=mn[i][0]
        endd=mn[i][1]
        for j in range(len(mn)):
            if mn[j][0]==endd:
                endd=mn[j][1]
            bad.append([endd,beginn])
    for i in range(len(mn)):
        beginn=mn[i][1]
        endd=mn[i][0]
        for j in range(len(mn)):
            if mn[j][1]==endd:
                endd=mn[j][0]
            bad.append([endd,beginn])
    for i in bad:
        C[i[0],i[1]]=math.inf

def delway(ep,ii,jj):#Чиствка неверного перехода
    for i in range(len(ep)):
        if ep[i][1][0]==ii and ep[i][1][1]==jj:
            ep.pop(i)
            break


def komi(C,maxlenght,ep_priv,ep,n,level=0,flag=0):# Рекурсивно реализованный метод ветвей и границ

    C_left = np.zeros((n, n))
    C_right = np.zeros((n, n))
    if level>=n-1:
        return 0
    num_line_left, num_col_left, value_left = tet(C)
    num_line_right, num_col_right, value_right = num_line_left, num_col_left, value_left

    for i in range(len(C)):
        for j in range(len(C[i])):
            C_left[i][j] = C[i][j]
            C_right[i][j] = C[i][j]

    do_in_left(C_left,num_line_left, num_col_left)
    do_in_right(C_right,num_line_right, num_col_right)

    value_left=minline(C_left)+mincolumn(C_left) # на левом пути тету прибавлять не нужно
    minline(C_right)
    mincolumn(C_right) # на правом пути минимумы прибавлять не нужно

    if value_right>=value_left and value_left+ep_priv<=maxlenght: #ветвление
        level+=1
        ep_priv+=value_left
        max_lenght1=ep_priv+value_right-value_left
        # if maxlenght>ep_priv+value_right-value_left:
        #     max_lenght1=ep_priv+value_right-value_left
        # else:
        #     max_lenght1 = maxlenght
        added(ep, "left", num_line_left, num_col_left, value_left, ep_priv, 1)
        nocyclefortoday(C_left,ep)
        flag=komi(C_left,max_lenght1,ep_priv,ep,n,level)
        if flag==None:
            return
        if flag>maxlenght:
            delway(ep,num_line_left,num_col_left)
            flag=komi(C_right, maxlenght, ep_priv-value_left+value_right, ep,n,level-1)
            return flag
    elif value_right<value_left and value_right+ep_priv<=maxlenght:
        ep_priv+=value_right
        max_lenght1 = ep_priv + value_left - value_right
        # if maxlenght>ep_priv+value_left-value_right:
        #     max_lenght1=ep_priv+value_left-value_right
        # else:
        #     max_lenght1 = maxlenght
        flag=komi(C_right,max_lenght1,ep_priv,ep,n,level)
        if flag == None:
            return
        if flag>maxlenght:
            added(ep, "left", num_line_left, num_col_left, value_left, ep_priv, 1)
            flag=komi(C_left, maxlenght, ep_priv-value_right+value_left, ep,n,level+1)
            if flag==math.inf:
                delway(ep,num_line_left,num_col_left)
            return flag
    else:
        return math.inf


while True:
    print('Введите 1, если матрица радомно сгенерированна с помощью предоставленного генератора(убедитесь что она сгенерированна)')
    print('Введите 0, если матрица задаётся из файла(нужно будет ввести имя файла, когда будет запрос)')
    try:
        answer=int(input())
        break
    except:
        print('Возникла ошибка, проверьте правильность ввода')
print('Введите размерность матрицы')
n = int(input())
a = {i for i in range(n)}
C_mom = np.zeros((n, n))
C0 = np.zeros((n, n))
ep = []
if answer:
    f = open('randmatrix.txt')
else:
    print('Введите имя файла для считывния(с учётом расширения)')
    f=open(input().strip())
C0 = [[int(i) for i in line.split()] for line in f]
f.close()
default_way = [[i, i + 1] for i in range(n - 1)]
default_way.append([n - 1, 0])
max_lenght = lenght_way(C0, default_way)
for i in range(len(C0)):
    for j in range(len(C0[i])):
        if i == j:
            C0[i][j] = math.inf
        C_mom[i][j] = C0[i][j]

k = 0
ep_priv = minline(C_mom) + mincolumn(C_mom)
flag = komi(C_mom, max_lenght, ep_priv, ep, n)
dist = 0
way = []
for i in range(len(ep)):
    if ep[i][0] == "left" and ep[i][3]:
        way.append(ep[i][1])
sort_way(way, n)
print(lenght_way(C0,way))
for i in range(len(way)):  # Вывод пути
    if i == 0:
        print(way[i][0], '->', way[i][1], sep='', end='')
    else:
        print(end='->')
        print(way[i][1], end='')
print()
