
import heapq
import pprint
STANDER = ['E','A','D','G','B','E']

#ALL = ['C','#C','D','#D','E','F','#F','G','#G','A','#A','B',]
ALL = ['A','#A','B','C','#C','D','#D','E','F','#F','G','#G']


def tuning_analysis(chroma_file):
    out = [0]*12

    with open(chroma_file,'r') as f:
        lines = f.readlines()
        for i in range(12) :
            s = sum([ float(line.strip().split(';')[i]) for line in lines ])
            out[i] = [ALL[i],s]
    return out



#  tuning_analysis('../test_chroma.csv')
    



