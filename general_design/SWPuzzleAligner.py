from EuclideanSimilarity import *
from Utilities import *

from math import *

class SWPuzzleAligner:
    
    def __init__(self, sim_calc = None):
        
        self.sim_calc = sim_calc

    def Align(self, Q = None, T = None, window=10, cutoff_percentile = 0.1, return_top = 1):
        
        # build similarity matrix
        # TODO: should build similarity matrix externally and supply to function
        sim_matrix = [[0 for k in range(len(T)+1)] for l in range(len(Q)+1)] 

        for i in range(len(Q) + 1): 
            for j in range(len(T) + 1): 
                if (i == 0 or j == 0): 
                    continue
                else:
                    sim_matrix[i][j] = self.sim_calc.SimilarityScore(Q, T, i-1, j-1, window)

#         fout = open('sim_mat.csv', 'w')
#         for r in sim_matrix:
#             fout.write(','.join([str(v) for v in r]) + '\n')
#         fout.close()
        
        # determine cutoff value
        sims = set() 
        for i in range(1,len(sim_matrix)):
            for j in range(1,len(sim_matrix[i])):
                sims.add(sim_matrix[i][j])

        sims = list(sims)
        sims.sort()
        cutoff = sims[int(len(sims) * cutoff_percentile) - 1]
        
        # build suffix table from pairwise matrix + penalties
        SuffTable = [[0 for k in range(len(T)+1)] for l in range(len(Q)+1)] 
        cutoff_multiplier = [[1 for k in range(len(T)+1)] for l in range(len(Q)+1)] # penalty for extended poor scoring cells
        for i in range(len(Q) + 1): 
            for j in range(len(T) + 1): 
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
        
        # the the maximum scores and positions
        mx = [0.0 for i in range(return_top)]
        mx_Q = [0 for i in range(return_top)]
        mx_T = [0 for i in range(return_top)]
        length = [0 for i in range(return_top)]
        
        #find the maxima
        a = 0
        while a < return_top:
            # get the first candidate alignment
            mx_list = [max(r) for r in SuffTable]
            mx_cand = max([r for r in mx_list])
            mx_Q_cand = mx_list.index(max(mx_list))
            mx_T_cand = SuffTable[mx_Q_cand].index(mx_cand)
            length_cand = 0
            
            #determine its length, and zero out this alignment
            for l in range(0, min(mx_Q_cand, mx_T_cand) + 1):
                if SuffTable[mx_Q_cand - l][mx_T_cand - l] == 0:
                    length_cand = l + 1
                    break
                else:
                    SuffTable[mx_Q_cand-l][mx_T_cand-l] = 0
            
            for l in range(1, min(len(SuffTable)-mx_Q_cand, len(SuffTable[0])-mx_T_cand)):
                if SuffTable[mx_Q_cand + l][mx_T_cand + l] == 0:
                    break
                else:
                    SuffTable[mx_Q_cand +l][mx_T_cand +l] = 0
                    
            # determine if it is an edge-on-edge alignment - if so, drop it
            # slopes = set() 
            # for j in range(mx_T_cand, mx_T_cand - length_cand + 2, -1):
            #     rise = abs(T[j]['y'] - T[j-1]['y'])
            #     run = abs(T[j]['x'] - T[j-1]['x'])
            #     
            #     if run == 0:
            #         slopes.add(0) # infinite slope set to 0
            #     else:
            #         slopes.add( floor(rise/run) ) 
            #         
            # if len(slopes) == 1:
            #     continue
            # else:
            #     mx[a] = mx_cand
            #     mx_Q[a] = mx_Q_cand
            #     mx_T[a] = mx_T_cand
            #     length[a] = length_cand
            #     a += 1
            x_vals = [ T[j]['x'] for j in range(mx_T_cand, mx_T_cand - length_cand +1, -1) ]
            y_vals = [ T[j]['y'] for j in range(mx_T_cand, mx_T_cand - length_cand +1, -1) ]
                    
            x_avg = avg(x_vals)
            y_avg = avg(y_vals)
            xi_xbar = [ x - x_avg for x in x_vals ]
            yi_ybar = [ y - y_avg for y in y_vals ]
            
            num = sum([ x * y for x,y in zip(xi_xbar, yi_ybar) ])
            den = sqrt(sum([x**2 for x in xi_xbar]) * sum([y**2 for y in yi_ybar]))
            
            if den == 0:
                r = 0
            else:
                r = num/den
                
            print(r)
            
            a += 1
                      
        return {'mx':mx, 'mx_Q':mx_Q, 'mx_T':mx_T, 'length':length}