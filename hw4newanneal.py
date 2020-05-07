from __future__ import print_function
import random
import itertools
import math
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from datetime import datetime
from simanneal import Annealer

def averageLists(lists):
    averageList = []
    totals = []
    times = []
    maxLength = 0
    #find max
    for sList in lists:
        if(len(sList) > maxLength):
            maxLength = len(sList)

    i = 0
    while i < maxLength:
        for sList in lists:
            if i < len(sList):
                totals[i]


def MCA(t, k, v, printable):
    '''
    This function takes a strength, number of rows
    and value and generates an exhaustive MCA for
    the given parameters
    int, int, int -> void
    '''
    allrows = []

    t = int(t)
    k = int(k)
    v = int(v)


    N = v**k

    #print("Here are t:", t,"k:", k, "v:", v)
    #print(N, "rows")

    for i in range(N):
        singlerow = numToRow(i,v,k)
        allrows.append(singlerow)
        if(printable != "none"):
            if(printable != "all"):
                if str(i) in printable:
                    print("Row number:",i, "Row:",singlerow)
            else:
                print(singlerow)


    return allrows

def numToRow(number, base, length):
    '''
    This function takes a number in base 10 and converts
    it to base, base, and then creates an array that is
    length long, adding leading zeros
    int, int, int -> list
    '''
    #converts a number to an array in a specific base
    shortrow = numberToBase(number, base)

    #then adds a certain number of 0s
    target = length-len(shortrow)
    temp = [0]*target
    return temp+shortrow


#Taken from here
#https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-in-any-base-to-a-string

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def colCombos(k, t):
    return list(itertools.combinations([i for i in range(int(k))],int(t)))

#https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
def nCr(n,r):
    n = int(n)
    r = int(r)
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def valueCombos(v, t):
    #Just a more simple version of the MCA function
    allrows = []
    N = v**t

    for i in range(N):
        singlerow = numToRow(i,v,t)
        allrows.append(singlerow)
    return allrows



def checkMCA(t,k,v, MCA):

    isMCA = True
    t = int(t)
    k = int(k)
    v = int(v)

    colcombo = colCombos(k,t)
    sigma = nCr(k,t)*(v**t)
    values = valueCombos(v, t)


    allInt = {}
    for comb in colcombo:
        key = str(comb)
        #print(key)
        innerDict = {}
        for value in values:
            valkey = str(value)
            innerDict[valkey] = 0

        allInt[key] = innerDict

    #print("Before:",allInt)
    for row in MCA:
        for colcom in colcombo:
            valpair = []
            for i in colcom:
                valpair.append(row[i])

            valkey = str(valpair)
            #print(valkey)
            if(allInt[str(colcom)][valkey] == 0):
                allInt[str(colcom)][valkey] += 1

    for row in MCA:
        for colcom in colcombo:
            for valpair in values:
                if(allInt[str(colcom)][str(valpair)] == 0):
                    isMCA = False
                    break

    #print("After:",allInt)
    if(isMCA):
        pass
    else:
        print("WARNING RESULT FAILED: This is not an MCA")

def runonce(t,k,v, startReRolls):


    exhArr = MCA(t,k,v,"none")
    randomMCA = []

    t = int(t)
    k = int(k)
    v = int(v)

    colcombo = colCombos(k,t)
    sigma = nCr(k,t)*(v**t)
    values = valueCombos(v, t)

    allInt = {}
    for comb in colcombo:
        key = str(comb)
        #print(key)
        innerDict = {}
        for value in values:
            valkey = str(value)
            innerDict[valkey] = 0

        allInt[key] = innerDict



    randomMCA.append([0]*k)

    sigma -= len(colcombo)

    exhArr.remove([0]*k)

    for colcom in colcombo:
        allInt[str(colcom)][str([0]*t)] += 1


    timeHistory = []
    newRows = []
    leftHistory = [sigma]

    N = 1


    ORIGINAL = startReRolls
    ORIGINALSIGMA = sigma

    while sigma > 0:

        #get interactions
        currentInter = 0
        desiredInter = math.ceil(sigma/(v**t))

        originalDesired = desiredInter

        if(ORIGINAL != "dynamic"):
            breakpoint = ORIGINAL
        else:
            breakpoint = int((sigma/ORIGINALSIGMA)*ORIGINAL)

        totalRolls = 0

        lastbest = []

        bestInter = -1

        startTS = datetime.timestamp(datetime.now())

        while (currentInter < desiredInter):
            totalRolls +=1

            currentInter = 0
            tempRow = exhArr[random.randint(0,len(exhArr)-1)]

            #count new interactions in row
            for colcom in colcombo:
                valpair = []
                for i in colcom:
                    valpair.append(tempRow[i])

                valkey = str(valpair)
                if(allInt[str(colcom)][valkey] == 0):
                    currentInter+=1

            if(currentInter >= desiredInter):
                lastbest = tempRow
                bestInter = currentInter
                breakpoint = ORIGINAL
                desiredInter = currentInter+1

            elif(currentInter < desiredInter and lastbest != []):
                if(breakpoint > 0):
                    breakpoint-=1
                else:
                    tempRow = lastbest

                    for colcom in colcombo:
                        valpair = []
                        for i in colcom:
                            valpair.append(tempRow[i])

                        valkey = str(valpair)
                        if(allInt[str(colcom)][valkey] == 0):
                            allInt[str(colcom)][valkey]+=1

                    break

            elif(currentInter < desiredInter and lastbest == []):
                pass

        testinter = 0
        for colcom in colcombo:
            valpair = []
            for i in colcom:
                valpair.append(lastbest[i])

            valkey = str(valpair)
            #print(valkey)
            if(allInt[str(colcom)][valkey] == 0):
                testinter+=1


        sigma -= bestInter
        randomMCA.append(lastbest)
        exhArr.remove(lastbest)
        endTS = datetime.timestamp(datetime.now())
        leftHistory.append(sigma)
        timeHistory.append((endTS-startTS))
        newRows.append(bestInter)
        #print("Time for row",(endTS-startTS), "rerolls",totalRolls,"decrease", originalDesired-bestInter, "interactions left",sigma)
        N+=1

    #checkMCA(t,k,v, randomMCA)
    return [N,leftHistory,timeHistory,newRows]



def main():

    #iter = input("Enter iterations: ")
    #tkv = input("Enter t,k,v: ")
    #arr = tkv.split(",")
    #t = int(arr[0])
    #k = int(arr[1])
    #v = int(arr[2])
    #iter = int(iter)


    file = open("out.csv","w")
    file.write("t,k,v,trials,rows,time\n")

    #fig, ax1 = plt.subplots()
    #plt.title("Remaining Rows vs Iteration for t,k,v "+" "+str(t)+", "+str(k)+", "+str(v)+", runs: "+str(iter))
    #ax1.set_xlabel("Rows")
    #ax1.set_ylabel("Remaining Interactions")
    #ax2 = ax1.twinx()
    #ax2.set_ylabel("New Interactions Per Second")


    #test different Ks
    t = 2
    v = 2
    for k in [10,11,12,15,20]:
        print("Running t,k,v",t,k,v)
        for rerolls in [0,5,10,15,20,100,500, "dynamic"]:
            if(rerolls != "dynamic"):
                if rerolls < 100:
                    totalRows = []
                    totalTimes = []
                    if(k < 15):
                        for i in tqdm(range(50)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                    else:
                        for i in tqdm(range(20)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                else:
                    totalRows = []
                    totalTimes = []
                    if(k < 15):
                        for i in tqdm(range(10)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                    else:
                        for i in tqdm(range(5)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
            else:
                totalRows = []
                totalTimes = []
                if(k < 15):
                    for i in tqdm(range(50)):
                        N,sigma,time,newRows = runonce(t,k,v,500)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                else:
                    for i in tqdm(range(25)):
                        N,sigma,time,newRows = runonce(t,k,v,500)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")

    k = 10
    v = 2
    for t in [3,4,5,8]:
        print("Running t,k,v",t,k,v)
        for rerolls in [0,5,10,15,20,100,500, "dynamic"]:
            if(rerolls != "dynamic"):
                if rerolls < 100:
                    totalRows = []
                    totalTimes = []
                    if(t < 5):
                        for i in tqdm(range(50)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                    else:
                        for i in tqdm(range(20)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                else:
                    totalRows = []
                    totalTimes = []
                    if(t < 5):
                        for i in tqdm(range(8)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                    else:
                        for i in tqdm(range(3)):
                            N,sigma,time,newRows = runonce(t,k,v,rerolls)
                            totalRows.append(N)
                            totalTimes.append(sum(time)/len(time))
                        file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
            else:
                totalRows = []
                totalTimes = []
                if(t < 5):
                    for i in tqdm(range(50)):
                        N,sigma,time,newRows = runonce(t,k,v,500)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")
                else:
                    for i in tqdm(range(25)):
                        N,sigma,time,newRows = runonce(t,k,v,500)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")


    t = 2
    k = 10
    for v in [3,4]:
        print("Running t,k,v",t,k,v)
        for rerolls in [0,5,10,15,20,100,500, "dynamic"]:
            if(rerolls != "dynamic"):
                if rerolls < 100:
                    totalRows = []
                    totalTimes = []

                    for i in tqdm(range(50)):
                        N,sigma,time,newRows = runonce(t,k,v,rerolls)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")

                else:
                    totalRows = []
                    totalTimes = []
                    for i in tqdm(range(10)):
                        N,sigma,time,newRows = runonce(t,k,v,rerolls)
                        totalRows.append(N)
                        totalTimes.append(sum(time)/len(time))
                    file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")

            else:
                totalRows = []
                totalTimes = []

                for i in tqdm(range(30)):
                    N,sigma,time,newRows = runonce(t,k,v,500)
                    totalRows.append(N)
                    totalTimes.append(sum(time)/len(time))
                file.write(""+str(t)+","+str(k)+","+str(v)+","+str(rerolls)+","+str(sum(totalRows)/len(totalRows))+","+str(sum(totalTimes)/len(totalTimes))+"\n")


    file.close()

    #for i in tqdm(range(iter)):
        #N,sigma,time,newRows = runonce(t,k,v)
        #ax1.plot(list(range(N)),sigma)

        #secPerInt = []
        #for i in range(N-1):
        #    secPerInt.append(time[i]/newRows[i])

        #ax2.plot(list(range(N-1)),secPerInt)


    #plt.show()

main()
