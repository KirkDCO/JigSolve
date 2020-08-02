from EuclideanSimilarity import *

class SWPuzzleAligner:
    
    def __init__(self, sim_calc = None):
        
        self.sim_calc = sim_calc

    def Align(self, Q = None, T = None, window=10, cutoff_percentile = 0.1, return_top = 1, seq_extension = 0):
        
        # extend sequences if asked
        if seq_extension > 0:
            # extend the query to account for circular sequence
            tail_length = min(int(len(T.border_sample) * seq_extension),
                              int(len(Q.border_sample) * seq_extension))

            Q.extend_border_sample(tail_length)
            T.extend_border_sample(tail_length, reverse = True)
        else:
            Q.border_sample_ext = Q.border_sample
            T.border_sample_ext = T.border_sample
            
        # build similarity matrix
        # TODO: should build similarity matrix externally and supply to function
        sim_matrix = [[0 for k in range(len(T.border_sample_ext)+1)] for l in range(len(Q.border_sample_ext)+1)] 

        for i in range(len(Q.border_sample_ext) + 1): 
            for j in range(len(T.border_sample_ext) + 1): 
                if (i == 0 or j == 0): 
                    continue
                else:
                    sim_matrix[i][j] = self.sim_calc.SimilarityScore(Q.border_sample_ext, T.border_sample_ext, 
                                                                     i-1, j-1, window)

        # determine cutoff value - where should this actually happen?
        sims = set() 
        for i in range(1,len(sim_matrix)):
            for j in range(1,len(sim_matrix[i])):
                sims.add(sim_matrix[i][j])

        sims = list(sims)
        sims.sort()
        cutoff = sims[int(len(sims) * cutoff_percentile)]
        
        # build suffix table from pairwise matrix + penalties
        SuffTable = [[0 for k in range(len(T.border_sample_ext)+1)] for l in range(len(Q.border_sample_ext)+1)] 
        cutoff_multiplier = [[1 for k in range(len(T.border_sample_ext)+1)] for l in range(len(Q.border_sample_ext)+1)] # penalty for extended poor scoring cells
        for i in range(len(Q.border_sample_ext) + 1): 
            for j in range(len(T.border_sample_ext) + 1): 
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
        mx_Q = [0 for i in range(return_top)]
        mx_T = [0 for i in range(return_top)]
        length = [0 for i in range(return_top)]
        mx_per_length = [0 for i in range(return_top) ]
        
        #find the maxima
        for a in range(return_top):
            mx_list = [max(r) for r in SuffTable]
            mx[a] = max([r for r in mx_list])
            mx_Q[a] = mx_list.index(max(mx_list))
            mx_T[a] = SuffTable[mx_Q[a]].index(mx[a])
            
            #determine its length, and zero out this alignment
            for l in range(0, min(mx_Q[a], mx_T[a]) + 1):
                if SuffTable[mx_Q[a] - l][mx_T[a] - l] == 0:
                    length[a] = l + 1
                    mx_per_length[a] = mx[a]/length[a]
                    break
                else:
                    SuffTable[mx_Q[a]-l][mx_T[a]-l] = 0
            
            for l in range(1, min(len(SuffTable)-mx_Q[a], len(SuffTable[0])-mx_T[a])):
                if SuffTable[mx_Q[a] + l][mx_T[a] + l] == 0:
                    break
                else:
                    SuffTable[mx_Q[a] +l][mx_T[a] +l] = 0
                    
            fout = open('SuffTable' + str(a) + '.csv', 'w')
            for r in SuffTable:
                fout.write(','.join([str(v) for v in r]) + '\n')
            fout.close()
                    
        return {'mx':mx, 'mx_Q':mx_Q, 'mx_T':mx_T, 'length':length, 'mx_per_length':mx_per_length}