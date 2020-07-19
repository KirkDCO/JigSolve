class CutoffPenalizer:
    
    def __init__:
        
        self.cutoff_multiplier = 1.0
        
    def SimScorePenalty(self, score, SuffTable, m_pt, n_pt, cutoff):
        
        if SuffTable[m_pt][n_pt] > cutoff:
            score *= self.cutoff_multiplier
            self.cutoff_multiplier *= 2.0
        else:
            self.cutoff_multiplier = 1.0
            
        return score
        