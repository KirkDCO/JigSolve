from EuclideanSimilarity import *

class NWPuzzleAligner:
    
    def __init__(self, sim_calc = None):
        
        self.sim_calc = sim_calc

    def Align(self, Q = None, T = None, window=10):
        
        # build similarity matrix
        # TODO: should build similarity matrix externally and supply to function
        sim_matrix = [[0 for k in range(len(T))] for l in range(len(Q))] 

        for i in range(len(Q)): 
            for j in range(len(T)): 
                sim_matrix[i][j] = self.sim_calc.SimilarityScore(Q, T, i, j, window)

        # build suffix table from pairwise matrix 
        SuffTable = [[0 for k in range(len(T))] for l in range(len(Q))] 
        for i in range(len(Q)): 
            for j in range(len(T)): 
                if (i == 0 or j == 0): 
                    SuffTable[i][j] = -sim_matrix[i][j] 
                else:
                    SuffTable[i][j] = SuffTable[i-1][j-1] + 1/sim_matrix[i][j] 
    
        fout = open('SuffTable.csv', 'w')
        for r in SuffTable:
            fout.write(','.join([str(v) for v in r]) + '\n')
        fout.close()
        
        # find the maximum
        mx_list = [max(r) for r in SuffTable]
        mx = max([r for r in mx_list])
        mx_Q = mx_list.index(max(mx_list))
        mx_T = SuffTable[mx_Q].index(mx)
            
        return mx, mx_Q, mx_T