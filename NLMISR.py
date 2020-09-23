from BitVector import *
from itertools import islice
from BitFunction import BitFunction

class NLMISR:
    def __init__(self, fn, size = 8):
        self.fn = fn
        self.size = size
        self.bits = BitVector(intVal = 7, size = self.size)

    def __iter__(self): return self
    
    def __str__(self): return self.bits.__str__()

    def __next__(self):
        nextState = BitVector(intVal = 0, size = self.size)

        for bitIdx in range(self.size):
            summation = self.bits[self.reverse(bitIdx+1)]

            for term in self.fn[bitIdx]:
                product = 1

                for idx in term:
                    product &= self.bits[self.reverse(idx)]

                summation ^=  product

            nextState[(self.reverse(bitIdx))] = summation
        
        self.bits = nextState
        return self.bits

    def reverse(self, bitIdx): return (self.size-1-bitIdx % self.size)

    def setBitFn(self, bitIdx, newFn): self.fn[bitIdx] = newFn
            
test = NLMISR(BitFunction.fromLFSR("8241", 16), 16)
test.fn.generateNLFSR(4,.8)
print(test.fn)

testIter = iter(test)
matches = []
for (i, x) in enumerate(islice(testIter,2**16)):
    #print(i,int(test.bits))
    if i == 0:
        start = int(test.bits)
    elif (int(test.bits) == start):
        matches.append(i)
print(matches)

# doesnt work: 800000000000057C, 80000000000001E4, "800000000000000D"