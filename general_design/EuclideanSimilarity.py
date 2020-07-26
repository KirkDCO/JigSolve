from Utilities import *

class EuclideanSimilarity:

    def __init__(self):
        pass

    def GetAlignedWindows(self, M, N, m_pt, n_pt, window):
    
        # for the given point in each set of points
        # extract the window of interest
        # align the sequence of points
        # calculate and return the distance between aligned windows

        # get the window of points for M
        M_pts = [ m_pt + v for v in range(-window,window+1)]
        for i,v in enumerate(M_pts):
            if v < 0:
                M_pts[i] += len(M)
            elif v >= len(M):
                M_pts[i] -= len(M)

        M_window = { pt:{'x':M[list(M.keys())[pt]]['x'],
                         'y':M[list(M.keys())[pt]]['y']} for pt in M_pts }

        # find the shift needed to align the given points
        # 2-dimensional for now
        x_shift = M[list(M.keys())[m_pt]]['x'] - N[list(N.keys())[n_pt]]['x']
        y_shift = M[list(M.keys())[m_pt]]['y'] - N[list(N.keys())[n_pt]]['y']

        # get window of points for N and apply shift
        N_pts = [ n_pt + v for v in range(-window,window+1)]
        for i,v in enumerate(N_pts):
            if v < 0:
                N_pts[i] += len(N)
            elif v >= len(N):
                N_pts[i] -= len(N)

        N_window = { pt:{'x':N[list(N.keys())[pt]]['x'] + x_shift,
                         'y':N[list(N.keys())[pt]]['y'] + y_shift} for pt in N_pts} 

        return M_window, N_window

    def SimilarityScore(self, M, N, m_pt, n_pt, window):

        # get the aligned windows
        M_window, N_window = self.GetAlignedWindows(M, N, m_pt, n_pt, window)

        # compute similarity score 
        # similarity in this case is the sum of Euclidean distances 
        # between matched points
        sum = 0.0
        for M_pt, N_pt in zip(M_window.keys(), N_window.keys()):
            sum += euc_dist( [ M_window[M_pt]['x'], M_window[M_pt]['y'] ],
                            [ N_window[N_pt]['x'], N_window[N_pt]['y'] ])
            
        return sqrt(sum)