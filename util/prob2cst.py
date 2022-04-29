#!/bin/env python

import numpy as np
from sys import argv
from Bio import SeqIO
from itertools import product


def parse_rnafold_MEA(fn):
    pairs = []
    with open(fn) as f:
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        ss = f.readline().split()[0]
        store = []
        for i, char in enumerate(ss):
            if char=='(': store.append(i)
            elif char==')':
                pairs.append((store[-1], i))
                pairs.append((i, store[-1]))
                store = store[:-1]
    return pairs

def ssneighb(pairs, k0, k1):
    for pair in pairs:
        for i in range(-2,3):
            for j in range(-2,3):
                if k0==pair[0]+i and k1==pair[1]+j: return True
    return False

#RNA Atoms
atoms = {
    'G': ["P","OP1","OP2","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'","N9","C8","N7","C5","C6","O6","N1","C2","N2","N3","C4"],
    'C': ["P","OP1","OP2","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'","N1","C2","O2","N3","C4","N4","C5","C6"],
    'A': ["P","OP1","OP2","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'","N9","C8","N7","C5","C6","N6","N1","C2","N3","C4"],
    'U': ["P","OP1","OP2","O5'","C5'","C4'","O4'","C3'","O3'","C2'","O2'","C1'","N1","C2","O2","N3","C4","O4","C5","C6"]
}
####

#Parse Inputs
prob = np.loadtxt(argv[1])

for record in SeqIO.parse(argv[2], 'fasta'):
    seq = record.seq._data

pairs = parse_rnafold_MEA(argv[3])

threshold = float(argv[4])
#

rlen = prob.shape[0]
mask = np.triu(np.ones((rlen,rlen)), 3)
    

for k in np.argsort(-prob*mask, axis=None):
    k0=k//rlen
    k1=k%rlen
    if prob[k0,k1]<threshold: continue
    if np.abs(k0-k1)<5: continue
    if ssneighb(pairs, k0, k1): continue
    print('AmbiguousConstraint')
    atoms1 = atoms[seq[k0].upper()]
    atoms2 = atoms[seq[k1].upper()]
    for ats in product(atoms1, atoms2):
        print('AtomPair', ats[0], k0+1, ats[1], k1+1, 'FADE', -100, 26, 20, -20, 20)
    print('END')
