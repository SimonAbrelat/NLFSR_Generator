# Generating NLFSRs

These files implement the concepts outlined in Elena Dubrova's [A Scalable Method for Constructing Galois NLFSRs with Period 2 <sup>n</sup> −1 using Cross-Join Pairs](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6290394) and 
[A Transformation From the Fibonacci to the Galois NLFSRs](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5290281) to create a generator randomized NLFSRs, with variables for max term length and tap density.


## Files

BitFunction.py: This file contains the BitFunction class, which is designed to interact with the NLFSR class. The Class contains a method for converting [hexCodes](http://users.ece.cmu.edu/~koopman/lfsr/index.html) associated with primitive polynomials in GF(2) to their respective LFSR bit functions. As well as a function for converting an LFSR to a random NLFSR.

The BitFunction may be printed to show a representation of each bit's update function, of the form x<sub>i+1</sub> + g<sub>i</sub>(x<sub>0</sub>, ..x<sub>n-1</sub>), with grouped terms being products (AND) and '+' separated terms being a sum (XOR).

NLFSR.py: This file contains the NLFSR class, which is constructed with a seed value and a BitFunction as its parameters. It is designed to iterate and evalute its given BitFunction over its BitVector contents
## Usage
While all aspects of the NLFSRs are available to be altered, the generation of a NLFSR is based on the premise of a full period LFSR, with no alterations. Altering the BitFunction manually could result in a nonfunctional NLSFR, unless done with caution. 

I recomend constructing an NLFSR in the designed fashion:

```python
example = NLFSR(seed, BitFunction.fromLFSR(hexCode, bitsize)) 
example.fn.generateNLFSR(max_terms, density)
```

An example with real values, if you want to run for yourself:

```python
example = NLFSR(seed, BitFunction.fromLFSR("810A", 16)) 
example.fn.generateNLFSR(4, .8)
```

Note on Max-term-length and Tap-density:
while term length is arbitrary, small values like 4 and 5 consistently yield better results in terms of both NLSFR complexity and size, as larger values lead to fewer terms with more gates. Larger term lengths also lead to longer calculation times.

Due to the way The NLFSRs are created, Larger density values  (i.e. 60% - 85%, ideally) tend to yield better results, and calculate faster. Density is represented as a decimal float.