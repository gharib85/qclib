#!/usr/bin/python
#
# Modified genetic algorithm for learning quantum operators
#
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
# based on:
# J. Faber, R.N. Thess, and G. Giraldi. Learning linear operators by genetic algorithms
#


from numpy import *
from qclib import *
from randU2 import randU2, u2
from random import shuffle, choice
from operators import random_unitary_matrix
import sys

# quantum examples
X = matrix([
    [1.0 / sqrt(1 + 2**2 + 3**2), 0.0 / sqrt(5**2 + 1), 9.0 / sqrt(9**2 + 2**2), 2.0 / sqrt(2**2 + 4**2 + 6**2)],
    [2.0 / sqrt(1 + 2**2 + 3**2), 5.0 / sqrt(5**2 + 1), 2.0 / sqrt(9**2 + 2**2), 4.0 / sqrt(2**2 + 4**2 + 6**2)],
    [3.0 / sqrt(1 + 2**2 + 3**2), 0.0 / sqrt(5**2 + 1), 0.0 / sqrt(9**2 + 2**2), 6.0 / sqrt(2**2 + 4**2 + 6**2)],
    [0.0 / sqrt(1 + 2**2 + 3**2), 1.0 / sqrt(5**2 + 1), 0.0 / sqrt(9**2 + 2**2), 0.0 / sqrt(2**2 + 4**2 + 6**2)]])
Y = matrix([
    [2.0 / sqrt(1 + 2**2 + 3**2), 5.0 / sqrt(5**2 + 1), 2.0 / sqrt(9**2 + 2**2), 4.0 / sqrt(2**2 + 4**2 + 6**2)],
    [3.0 / sqrt(1 + 2**2 + 3**2), 0.0 / sqrt(5**2 + 1), 0.0 / sqrt(9**2 + 2**2), 6.0 / sqrt(2**2 + 4**2 + 6**2)],
    [1.0 / sqrt(1 + 2**2 + 3**2), 0.0 / sqrt(5**2 + 1), 9.0 / sqrt(9**2 + 2**2), 2.0 / sqrt(2**2 + 4**2 + 6**2)],
    [0.0 / sqrt(1 + 2**2 + 3**2), 1.0 / sqrt(5**2 + 1), 0.0 / sqrt(9**2 + 2**2), 0.0 / sqrt(2**2 + 4**2 + 6**2)]])

GOOD = matrix([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 0],
    [0, 0, 0, 1]])

def fitness(m):
    t = (m * X - Y)
    return float(abs(0.5 * (t * t.H).trace()))

def fitness2(m):
    err = 0
    for i in xrange(X.shape[1]):
        err += sum(m * X[:,i] - Y[:,i]) / (m.shape[0] * X.shape[1])
    return exp(-err)

#fitness = fitness

iterations = 500
poplen = 100
pc = 0.85
pm = 0.95
ps = 0.3
elitism = 30
nm = 2
perturb = 0.03


# initial random population
population = []
for i in xrange(poplen):
    population.append(random_unitary_matrix(4, real = True))

print 'Initial population:'
for c in population:
    print c

best = None
best_val = None

f = open('log.txt', 'w')

for epoch in xrange(iterations):

    print 'epoch ' + str(epoch)

    # calculate fitness
    fvalues = []
    for i in xrange(poplen):
        fvalues.append(fitness(population[i]))
    # print fvalues, min(fvalues)

    if best == None or min(fvalues) < best_val:
        best_val = min(fvalues)
        best = population[fvalues.index(best_val)]

    f.write('%d %f %f %f %f\n' % (epoch, best_val, min(fvalues), max(fvalues), sum(fvalues) / len(fvalues)))

    newpop = []
    # elitism
    if elitism > 0:
        ranking = fvalues[:]
        ranking.sort()
        for e in xrange(elitism):
            newpop.append(population[fvalues.index(ranking[e])])
    # crossover
    while len(newpop) < poplen:
        par1 = population[fvalues.index(choice(ranking[:int(ps * poplen)]))]
        par2 = population[fvalues.index(choice(ranking[:int(ps * poplen)]))]
        if random() <= pc:
            for n in xrange(2):
                child = par1.copy()
                for i in xrange(child.shape[0]):
                    for j in xrange(child.shape[1]):
                        if random() < 0.5:
                            child[i,j] = par2[i,j]
                newpop.append(child)
        else:
            newpop.append(par1)
            newpop.append(par2)
    # mutation
    for p in xrange(len(newpop)):
        if random() < pm:
            m = newpop[p]
            mutated = []
            while len(mutated) < nm:
                # random indices
                i = choice(range(m.shape[0]))
                j = choice(range(m.shape[1]))
                if mutated.count((i,j)) > 0:
                    continue
                mutated.append((i,j))
                m[i,j] += 2 * perturb * random() - perturb
                if m[i,j] > 1:
                    m[i,j] = 1
                elif m[i,j] < -1:
                    m[i,j] = -1
    population = newpop


print best_val
print best
print GOOD

f.close()

