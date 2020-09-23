from BitVector import BitVector
from random import randrange, randint, sample
class BitFunction:
    def __init__(self, fn):
        self.fn = fn
        self.size = len(fn)
        self.tau = self.size-1

    def __getitem__(self, idx): return self.fn[idx]

    def __setitem__(self, idx, val): self.fn[idx] = val

    def __len__(self): return len(self.fn)
    
    def __str__(self):
        outstr = ""
        for i in range(len(self.fn)-1,-1,-1):
            outstr += ("Bit " + str(i)
                + ": " + str((i + 1) % self.size) + " + ("
                + (" + ".join([str(term) for term in self.fn[i]])) + ")\n")
        return outstr
    
    @classmethod
    def fromLFSR(self,hexStr, size):
        taps = list(BitVector(intVal = int(hexStr, 16), size = size))
        LFSRFunc = [[idx] for (idx, t) in enumerate(taps) if t == 1]
        try:
            LFSRFunc.remove([0])
        except ValueError:
            pass
        return BitFunction([[] for _ in range(size-1)] + [LFSRFunc])

    def shiftTerms(self, terms, idxA, idxB):
        alteredTerms = []
        for term in terms:
            valid = True
            for i in term:
                valid &= (i >= (idxA-idxB))
            if valid:
                altTerm = [(i - idxA + idxB) for i in term]
                alteredTerms.append(altTerm)
                self.fn[idxA].remove(term)
                self.fn[idxB] += [altTerm]
            else:
                print("Term " + str(term) + " cannot be shifted that far")
        return [idx for term in alteredTerms for idx in term]

    def getMinDestination(self, term):
        return max((self.size - 1) - min(term), self.tau)

    def getMaxDestination(self, term):
        return min((self.size + self.tau) - (max(term) + 1), self.size - 1)

    def addNonLinearTerm(self,maxAnds):
        minDest = maxDest = 0
        while not (minDest < maxDest):
            numTaps = randint(2,maxAnds)
            newTerm = sample(range(1, self.size), numTaps)#[randrange(1,self.size) for _ in range(numTaps)]
            maxDest = self.getMaxDestination(newTerm)
            minDest = self.getMinDestination(newTerm)

        idx1,idx2 = sample(range(minDest,maxDest+1),2)

        self.fn[self.size - 1] += [newTerm]
        self.fn[self.size - 1] += [newTerm[:]]
        
        newTaps = []
        newTaps.append(self.shiftTerms([newTerm], self.size-1, idx1))
        newTaps.append(self.shiftTerms([newTerm], self.size-1, idx2))
        return [tap for sublist in newTaps for tap in sublist]

    def generateNLFSR(self, maxAnds, density):
        self.tau = int(density * self.size)
        tapped = BitVector(intVal = 0, size = self.size)

        self.shiftTerms(
            [term for term in self.fn[self.size-1] if term[0] > self.tau],
             self.size-1, self.tau
        )
        
        while tapped.count_bits() < self.tau:
            newTaps = self.addNonLinearTerm(maxAnds)
            for tap in newTaps:
                tapped[tap] = 1
        return
