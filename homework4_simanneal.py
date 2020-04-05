# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import random
from simanneal import Annealer

import itertools
import matplotlib.pyplot as plt

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



def runonce(t,k,v):


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

    while sigma > 0:

        #get interactions
        currentInter = 0
        desiredInter = math.ceil(sigma/(v**t))
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

        sigma -= currentInter
        randomMCA.append(tempRow)
        exhArr.remove(tempRow)
        N+=1

    #print(randomMCA)
    #print(N)
    return N

def main():
        #Q1
    inarr = input("Enter t,k,v, seperated by a comma: ").split(",")
    t = inarr[0]
    k = inarr[1]
    v = inarr[2]

    num = (input("Enter a number of trials: "))

    if(num == ""):
        num = 10
    else:
        num = int(num)
    totalN = 0
    NValues = []
    ct = {}

    for i in range(num):
        currN = runonce(t,k,v)
        totalN+=currN
        NValues.append(currN)

        if(currN not in ct):
            ct[currN] = 1
        else:
            ct[currN] += 1

    NValues.sort()
    CountN = []
    for val in NValues:
        CountN.append(ct[val])

    titleS = "Average N for "+str(num)+ " trials at t: "+t+" k: "+k+" v: "+v+" avg: "+str(round(totalN/num,3))
    plt.title(titleS)
    plt.plot(NValues, CountN)
    plt.show()

    print("Here are t:", t,"k:", k, "v:", v)
    print("Average", round(totalN/num,3))

main()

------------------------------------------------------------------------------------------SIMLATED ANNEAL EXAMPLE BELOW--------------------------------------------------------
def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]
        return e


if __name__ == '__main__':

    # latitude and longitude for the twenty largest U.S. cities
    cities = {
        'New York City': (40.72, 74.00),
        'Los Angeles': (34.05, 118.25),
        'Chicago': (41.88, 87.63),
        'Houston': (29.77, 95.38),
        'Phoenix': (33.45, 112.07),
        'Philadelphia': (39.95, 75.17),
        'San Antonio': (29.53, 98.47),
        'Dallas': (32.78, 96.80),
        'San Diego': (32.78, 117.15),
        'San Jose': (37.30, 121.87),
        'Detroit': (42.33, 83.05),
        'San Francisco': (37.78, 122.42),
        'Jacksonville': (30.32, 81.70),
        'Indianapolis': (39.78, 86.15),
        'Austin': (30.27, 97.77),
        'Columbus': (39.98, 82.98),
        'Fort Worth': (32.75, 97.33),
        'Charlotte': (35.23, 80.85),
        'Memphis': (35.12, 89.97),
        'Baltimore': (39.28, 76.62)
    }

    # initial state, a randomly-ordered itinerary
    init_state = list(cities.keys())
    random.shuffle(init_state)

    # create a distance matrix
    distance_matrix = {}
    for ka, va in cities.items():
        distance_matrix[ka] = {}
        for kb, vb in cities.items():
            if kb == ka:
                distance_matrix[ka][kb] = 0.0
            else:
                distance_matrix[ka][kb] = distance(va, vb)

    tsp = TravellingSalesmanProblem(init_state, distance_matrix)
    tsp.set_schedule(tsp.auto(minutes=0.2))
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()

    while state[0] != 'New York City':
        state = state[1:] + state[:1]  # rotate NYC to start

    print()
    print("%i mile route:" % e)
    print(" ➞  ".join(state))
