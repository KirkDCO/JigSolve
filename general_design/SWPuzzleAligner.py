from EuclideanSimilarity import *

class SWPuzzleAligner:
    
    def __init__(self, sim_calc = None):
        
        self.sim_calc = sim_calc

    def Align(self, M = None, N = None, window=10, cutoff_percentile = 0.1):
        
        # build similarity matrix
        # TODO: should build similarity matrix externally and supply to function
        sim_matrix = [[0 for k in range(len(N)+1)] for l in range(len(M)+1)] 

        for i in range(len(M) + 1): 
            for j in range(len(N) + 1): 
                if (i == 0 or j == 0): 
                    continue
                else:
                    sim_matrix[i][j] = self.sim_calc.SimilarityScore(M, N, i-1, j-1, window)

        # determine cutoff value - where should this actually happen?
        sims = []
        for i in range(1,len(sim_matrix)):
            for j in range(1,len(sim_matrix[i])):
                sims.append(sim_matrix[i][j])

        sims.sort()
        cutoff = sims[int(len(sims) * cutoff_percentile)]
        
        # build suffix table from pairwise matrix + penalties
        # places to store maximum score and which position
        mx = 0.0
        mx_M = 0
        mx_N = 0

        # Create suffix table
        SuffTable = [[0 for k in range(len(N)+1)] for l in range(len(M)+1)] 
        cutoff_multiplier = 2 # penalty for extended poor scoring cells
        for i in range(len(M) + 1): 
            for j in range(len(N) + 1): 
                if (i == 0 or j == 0): 
                    SuffTable[i][j] = 0
                else:
                    d = sim_matrix[i][j]
                    if d < cutoff:
                        SuffTable[i][j] = SuffTable[i-1][j-1] + 1
                        cutoff_multiplier = 1.0
                    else:
                        SuffTable[i][j] = SuffTable[i-1][j-1] - cutoff_multiplier
                        cutoff_multiplier *= 2.0
                        
                    SuffTable[i][j] = max(0,SuffTable[i][j])
    
                    if SuffTable[i][j] > mx:
                        mx = SuffTable[i][j]
                        mx_M = i
                        mx_N = j

        # determine the length of the best scoring window
        for length in range(1, min(mx_M, mx_N) + 1):
            if SuffTable[mx_M-length][mx_N - length] == 0:
                break

        return SuffTable, mx, mx_M, mx_N, length + 1