import random
import itertools
import math
import matplotlib.pyplot as plt
from datetime import datetime

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

def runonce(t,k,v, mode):


    exhArr = MCA(t,k,v,"none")
    #we now have the possible rows
    #rows = input("Enter rows to print seperated by a comma, all, or nothing: ")
    #if rows == "":
    #    exhArr = MCA(t,k,v, "none")
    #elif rows == "all":
    #    exhArr = MCA(t,k,v, "all")
    #else:
    #    exhArr = MCA(t,k,v,rows.split(","))

    randomMCA = []

    t = int(t)
    k = int(k)
    v = int(v)
    #next get all indexes for columns with strength t
    colcombo = colCombos(k,t)
    #print(colcombo)

    #total interactions
    sigma = nCr(k,t)*(v**t)
    #print(sigma)

    #all the possible value combos
    values = valueCombos(v, t)
    #print(values)

    #build outer dictionary, column combos as keys,
    #values are dictionaries with value pairs as keys and counts as values
    allInt = {}
    for comb in colcombo:
        key = str(comb)
        #print(key)
        innerDict = {}
        for value in values:
            valkey = str(value)
            innerDict[valkey] = 0

        allInt[key] = innerDict



    #now we have a storage structure for interactions
    #print(allInt)

    #add a row of 0s
    randomMCA.append([0]*k)

    #remove the count of those interactions
    sigma -= len(colcombo)

    #take out the 0th possibility
    exhArr.remove([0]*k)

    #mark in the hashmap that 0's are taken
    for colcom in colcombo:
        allInt[str(colcom)][str([0]*t)] += 1


    #a row of all 0s gets takes care of as many combinations
    #as we have possible row combinations
    N = 1

    ORIGINAL = 500
    while sigma > 0:

        #get interactions
        currentInter = 0
        desiredInter = math.ceil(sigma/(v**t))

        breakpoint = ORIGINAL
        lastbest = []
        bestInter = -1

        if(mode == "hill"):
            while (currentInter < desiredInter):

                currentInter = 0
                tempRow = exhArr[random.randint(0,len(exhArr)-1)]

                #count new interactions in row
                for colcom in colcombo:
                    valpair = []
                    for i in colcom:
                        valpair.append(tempRow[i])

                    valkey = str(valpair)
                    #print(valkey)
                    if(allInt[str(colcom)][valkey] == 0):
                        currentInter+=1
                # print("Given row",tempRow)
                # print("Breakpoint",breakpoint,"expected interactions", desiredInter,"current interactions",currentInter)
                # input()

                #if we have enough, update the hashmap
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
                            #print(valkey)
                            if(allInt[str(colcom)][valkey] == 0):
                                allInt[str(colcom)][valkey]+=1

                        break

                elif(currentInter < desiredInter and lastbest == []):
                    pass
            #print("Adding row",lastbest, "removing",bestInter,"interactions from sigma:",sigma)

            testinter = 0
            for colcom in colcombo:
                valpair = []
                for i in colcom:
                    valpair.append(lastbest[i])

                valkey = str(valpair)
                #print(valkey)
                if(allInt[str(colcom)][valkey] == 0):
                    testinter+=1

            #print("testinter",testinter,"bestinter",bestInter)

            sigma -= bestInter
            randomMCA.append(lastbest)
            exhArr.remove(lastbest)
            N+=1



        else:
            while (currentInter < desiredInter):
                currentInter = 0
                tempRow = exhArr[random.randint(0,len(exhArr)-1)]

                #count new interactions in row
                for colcom in colcombo:
                    valpair = []
                    for i in colcom:
                        valpair.append(tempRow[i])

                    valkey = str(valpair)
                    #print(valkey)
                    if(allInt[str(colcom)][valkey] == 0):
                        currentInter+=1
                #if we have enough, update the hashmap
                if(currentInter >= desiredInter):
                    for colcom in colcombo:
                        valpair = []
                        for i in colcom:
                            valpair.append(tempRow[i])

                        valkey = str(valpair)
                        #print(valkey)
                        if(allInt[str(colcom)][valkey] == 0):
                            allInt[str(colcom)][valkey]+=1

            #print("Adding row",tempRow)
            sigma -= currentInter
            randomMCA.append(tempRow)
            exhArr.remove(tempRow)
            N+=1

    #print(randomMCA)
    #print(N)
    checkMCA(t,k,v, randomMCA)
    return N

def suite(t, k, v, trials, mode):


    num = int(trials)

    totalN = 0
    NValues = []
    ct = {}

    completionTimes = []

    for i in range(num):

        startTS = datetime.timestamp(datetime.now())
        currN = runonce(t,k,v, mode)
        endTS = datetime.timestamp(datetime.now())
        if(i == 0):
            print("Predicted total runtime: ",(endTS-startTS)*num,"seconds")
        totalN+=currN
        NValues.append(currN)
        #print("Finished in",endTS-startTS,"seconds")
        completionTimes.append(endTS-startTS)

        if(currN not in ct):
            ct[currN] = 1
        else:
            ct[currN] += 1

    NValues.sort()

    RealNValues = list(ct.keys())
    RealNValues.sort()
    CountN = []
    for val in RealNValues:
        CountN.append(ct[val])

    #titleS = "Average N for "+str(num)+ " trials at t: "+t+" k: "+k+" v: "+v+" avg: "+str(round(totalN/num,3))
    #plt.title(titleS)
    #plt.plot(NValues, CountN)
    #plt.show()

    #print("Here are t:", t,"k:", k, "v:", v)
    #print("Average", round(totalN/num,3))
    # print(RealNValues)
    # print(CountN)

    print("Average completion time for",mode," = ",round(sum(completionTimes)/len(completionTimes),5))
    print("Average", round(totalN/num,3))
    return [RealNValues, CountN]




def main():

    mode = input("Do you want to run a range of t, k, v? (Y/N): ")
    if(mode.lower() == "y"):
        inarr = input("Enter beginning t,k,v, seperated by a comma: ").split(",")
        t1 = inarr[0]
        k1 = inarr[1]
        v1 = inarr[2]

        inarr = input("Enter ending t,k,v, seperated by a comma: ").split(",")
        t2 = inarr[0]
        k2 = inarr[1]
        v2 = inarr[2]

        num = (input("Enter a number of trials: "))
        mode = input("Enter a mode (normal/hill): ")

        #run through strengths
        runs = []
        if(t1 != t2):
            for stren in range(int(t1),int(t2)+1):
                runs.append(suite(stren,k1,v1,num, mode))

            titleS = "Average N for "+str(num)+ " trials from CA("+t1+", "+k1+", "+v1+") to CA("+t2+", "+k2+", "+v2+")"
            plt.title(titleS)
            for run in runs:
                plt.plot(run[0],run[1])
            plt.show()

        #run through columns
        elif(k1 != k2):
            for col in range(int(k1),int(k2)+1):
                runs.append(suite(t1,col,v1,num,mode))

            titleS = "Average N for "+str(num)+ " trials from CA("+t1+", "+k1+", "+v1+") to CA("+t2+", "+k2+", "+v2+")"
            plt.title(titleS)
            for run in runs:
                plt.plot(run[0],run[1])
            plt.show()

        #run through values
        elif(v1 != v2):
            for val in range(int(v1),int(v2)+1):
                runs.append(suite(t1,k1,val,num,mode))

            titleS = "Average N for "+str(num)+ " trials from CA("+t1+", "+k1+", "+v1+") to CA("+t2+", "+k2+", "+v2+")"
            plt.title(titleS)
            for run in runs:
                plt.plot(run[0],run[1])
            plt.show()

        else:
            print("Can only vary one thing at once")
    else:
        inarr = input("Enter t,k,v, seperated by a comma: ").split(",")
        t1 = inarr[0]
        k1 = inarr[1]
        v1 = inarr[2]

        comp = input("Compare hill to normal? ")

        num = (input("Enter a number of trials: "))



        if comp.lower() == "n" or comp.lower() == "no":
            mode = input("Enter a mode (normal/hill): ")
            runs = suite(t1,k1,v1,num,mode)

            #
            titleS = "Average N for "+str(num)+ " trials for CA("+t1+", "+k1+", "+v1+")"
            # print(runs)
            plt.title(titleS)
            plt.plot(runs[0],runs[1])
            plt.show()

        else:
            hillRuns = suite(t1,k1,v1,num,'hill')
            randomRuns = suite(t1,k1,v1,num,'normal')

            #
            titleS = "Average N for "+str(num)+ " trials for CA("+t1+", "+k1+", "+v1+") for HillClimbing and Random"
            # print(runs)

            plt.title(titleS)
            hillLine, = plt.plot(hillRuns[0],hillRuns[1])
            hillLine.set_label("HillClimbing")

            randomLine, = plt.plot(randomRuns[0],randomRuns[1])
            randomLine.set_label("Random")
            plt.legend()
            plt.show()


main()
