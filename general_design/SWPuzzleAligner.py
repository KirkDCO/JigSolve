from EuclideanSimilarity import *

class SWPuzzleAligner:
    
    def __init__(self, sim_calc = None):
        
        self.sim_calc = sim_calc

    def Align(self, M = None, N = None, window=10, cutoff_percentile = 0.1, return_top = 1):
        
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
        sims = set() 
        for i in range(1,len(sim_matrix)):
            for j in range(1,len(sim_matrix[i])):
                sims.add(sim_matrix[i][j])

        sims = list(sims)
        sims.sort()
        cutoff = sims[int(len(sims) * cutoff_percentile)]
        
        # build suffix table from pairwise matrix + penalties
        SuffTable = [[0 for k in range(len(N)+1)] for l in range(len(M)+1)] 
        cutoff_multiplier = [[1 for k in range(len(N)+1)] for l in range(len(M)+1)] # penalty for extended poor scoring cells
        for i in range(len(M) + 1): 
            for j in range(len(N) + 1): 
                if (i == 0 or j == 0): 
                    SuffTable[i][j] = 0
                else:
                    d = sim_matrix[i][j]
                    if d < cutoff:
                        SuffTable[i][j] = SuffTable[i-1][j-1] + 1
                        cutoff_multiplier[i][j] = 1
                    else:
                        SuffTable[i][j] = SuffTable[i-1][j-1] - cutoff_multiplier[i-1][j-1] 
                        cutoff_multiplier[i][j] = cutoff_multiplier[i-1][j-1] * 2
                        
                    SuffTable[i][j] = max(0,SuffTable[i][j])
    
        fout = open('SuffTable.csv', 'w')
        for r in SuffTable:
            fout.write(','.join([str(v) for v in r]) + '\n')
        fout.close()
        
        # the the maximum scores and positions
        mx = [0.0 for i in range(return_top)]
        mx_M = [0 for i in range(return_top)]
        mx_N = [0 for i in range(return_top)]
        length = [0 for i in range(return_top)]
        
        #find the maxima
        for a in range(return_top):
            mx_list = [max(r) for r in SuffTable]
            mx[a] = max([r for r in mx_list])
            mx_M[a] = mx_list.index(max(mx_list))
            mx_N[a] = SuffTable[mx_M[a]].index(mx[a])
            
            #determine its length, and zero out this alignment
            for l in range(0, min(mx_M[a], mx_N[a]) + 1):
                if SuffTable[mx_M[a] - l][mx_N[a] - l] == 0:
                    length[a] = l + 1 
                    break
                else:
                    SuffTable[mx_M[a]-l][mx_N[a]-l] = 0
            
            for l in range(0, min(len(SuffTable)-mx_M[a], len(SuffTable[0])-mx_N[a])):
                if SuffTable[mx_M[a] + l][mx_N[a] + l] == 0:
                    break
                else:
                    SuffTable[mx_M[a] +l][mx_N[a] +l] = 0
                    
            fout = open('SuffTable' + str(a) + '.csv', 'w')
            for r in SuffTable:
                fout.write(','.join([str(v) for v in r]) + '\n')
            fout.close()
                    
        return {'mx':mx, 'mx_M':mx_M, 'mx_N':mx_N, 'length':length}