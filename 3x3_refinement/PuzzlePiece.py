from Utilities import *

class Piece:
    
    def __init__(self, border_fn, border_sampling_rate = 0.20, dist_window_size = 10):
        
        # fn: filename containing the ordered list of border points (x,y,order)
        # sampling_rate: sampling rate on the border for reduced representation
        # window_size: number of sampled points on either side of the central for 
        
        border = self.__load_border(border_fn)
        
        self.border_sampling_rate = border_sampling_rate
        border_sample = self.sample_border(border_sampling_rate)
        
        self.dist_window_size = dist_window_size
        border_distances = self.create_border_distances(dist_window_size)
        
    def __load_border(self, border_fn = None):
        
        # load the ordered piece border points 
        
        if border_fn == None:
            return None
        
        self.pts = {}
        
        fin = open(border_fn, 'r')
        h = fin.readline()
        for i,l in enumerate(fin):
            tok = l.rstrip().split(',')
            self.pts[i] = {}
            self.pts[i]['x'] = int(tok[0])
            self.pts[i]['y'] = int(tok[1])
        fin.close()
        
    def sample_border(self, sampling_rate = 0.20):
        
        # sample the border and store the sampled points 
        
        self.sampled_pts = {}
        
        indices = [i for i in range(0,len(self.pts), int(1/sampling_rate)) ]
        
        for i,index in enumerate(indices):
            self.sampled_pts[i] = {'orig_idx': index,
                                   'x': self.pts[index]['x'],
                                   'y': self.pts[index]['y']
                                  }
    
    def create_border_distances(self, dist_window_size = 10):
        
        # for the sampled points, create all pair-wise distances
        
        self.sample_dists = {}
        indices = self.sampled_pts.keys()
        for idx in [*indices]:
            window = [ idx + v for v in range(-dist_window_size, dist_window_size + 1) ]
            for i,v in enumerate(window):
                if v<0:
                    window[i] += len(indices)
                elif v >= len(indices):
                    window[i] -= len(indices)
            
            self.sample_dists[idx] = [] 
            for j,jdx in enumerate(window[:-1]):
                for k,kdx in enumerate(window[j+1:]):
                    self.sample_dists[idx].append(EucDist( [self.sampled_pts[jdx]['x'], self.sampled_pts[jdx]['y'] ],
                                                           [self.sampled_pts[kdx]['x'], self.sampled_pts[kdx]['y'] ] ))
                   
                                                                                                         
        
        