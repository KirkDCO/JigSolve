from Utilities import *

class PairwiseDistanceSimilarity:

    def __init__(self):
        pass

    def SimilarityScore(self, M, N, m_pt, n_pt, window):

        # compute similarity score 
        # similarity in this case is the sum of Euclidean distances 
        # between the vectors of pairwise distances calculated on the window 
        return euc_dist( M[m_pt], N[n_pt] )
    