import math

from Utilities import *

class PuzzlePiece:
    
    def __init__(self, border_fn, border_sampling_rate = 0.20, dist_window_size = 10):
        
        # fn: filename containing the ordered list of border points (x,y,order)
        # sampling_rate: sampling rate on the border for reduced representation
        # window_size: number of sampled points on either side of the central for 
        
        self.load_border(border_fn)
        self.sample_border(border_sampling_rate)
        self.create_border_distances(dist_window_size)
        
    def load_border(self, border_fn = None):
        
        # load piece border points 
        
        if border_fn == None:
            return None
        
        self.border = {}
        
        fin = open(border_fn, 'r')
        h = fin.readline()
        for i,l in enumerate(fin):
            tok = l.rstrip().split(',')
            self.border[i] = {}
            self.border[i]['x'] = int(tok[0])
            self.border[i]['y'] = int(tok[1])
            self.border[i]['order'] = None
        fin.close()

        # put the points in order
        self.order_border()
        
    def sample_border(self, border_sampling_rate = 0.20):
        
        # sample the border and store the sampled points 
        
        self.sampled_border = {}
        
        indices = [i for i in range(0,len(self.ordered_border), floor(1/border_sampling_rate)) ]
        
        for i,index in enumerate(indices):
            self.sampled_border[i] = {'orig_idx': index,
                                   'x': self.ordered_border[index]['x'],
                                   'y': self.ordered_border[index]['y']
                                  }
    
    def create_border_distances(self, dist_window_size = 10):
        
        # for the sampled points, create all pair-wise distances
        
        self.sample_dists = {}
        indices = self.sampled_border.keys()
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
                    self.sample_dists[idx].append(EucDist( [self.sampled_border[jdx]['x'], self.sampled_border[jdx]['y'] ],
                                                           [self.sampled_border[kdx]['x'], self.sampled_border[kdx]['y'] ] ))

    def order_border(self):
        
        # put the border points in order, and assure clockwise orientation
        
        # create dictionary to hold order of points by key
        k = self.border.keys()
        dist_mat = [[999999 for i in range(len(k))] for j in range(len(k))] 
        
        for i in range(0,len(k)-1):
            for j in range(i+1,len(k)):
                x1 = self.border[i]['x']
                x2 = self.border[j]['x']
                y1 = self.border[i]['y']
                y2 = self.border[j]['y']
                d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
                dist_mat[i][j] = d
                dist_mat[j][i] = d
        
        # set first point
        current_pt = 0
        ordered_pts = []
        early_stop = False
        
        # step through points finding the closest to create the border order
        for i in range(len(k)):
            self.border[current_pt]['order'] = i
            ordered_pts.append(current_pt)
            
            li=[] 
            for j in range(len(dist_mat[current_pt])): 
                  li.append([dist_mat[current_pt][j],j]) 
            li.sort() 
            sort_index = [] 
              
            for x in li: 
                  sort_index.append(x[1]) 
        
            for j,dist_idx in enumerate(sort_index):
                if dist_idx == 0 and j != 0:
                    early_stop = True
                    break 
                
                if self.border[dist_idx]['order'] is None:
                    current_pt = dist_idx
                    break
                
            if early_stop:
                break
       
        self.ordered_border = {} 
        for i,o in enumerate(ordered_pts):
            self.ordered_border[i] = { 'x':self.border[o]['x'],
                                       'y':self.border[o]['y'],
                                       'order':i}
            
        # TODO: need to verify clockwise orientation
                                                                                                         
        
        
