from math import *
import copy

from Utilities import *

class PuzzlePiece:
    
    def __init__(self, border_fn, border_sampling_rate = 0.20):
        
        # fn: filename containing the list of border points
        # sampling_rate: sampling rate on the border for reduced representation
        # window_size: number of sampled points on either side of the central for 
        
        self.load_border(border_fn)
        
        self.border_sampling_rate = border_sampling_rate
        self.sample_border(border_sampling_rate)
        
        #self.window_size = window_size # window_size determined how big the window was for 
        #self.create_distances(window_size) # computing pairwise distances and angles
        #self.create_angles(window_size) # removed from parameter list while these are no longer used
        
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
        
        self.border_sample = {}
        
        indices = [i for i in range(0,len(self.ordered_border), floor(1/border_sampling_rate)) ]
        
        for i,index in enumerate(indices):
            self.border_sample[i] = {'orig_idx': index,
                                     'x': self.ordered_border[index]['x'],
                                     'y': self.ordered_border[index]['y']
                                     }
    
    def create_distances(self,window_size = 10):
        
        # for the sampled points, create all pair-wise distances
        
        self.sample_dists = {}
        indices = self.border_sample.keys()
        for idx in [*indices]:
            window = [ idx + v for v in range(-window_size, window_size + 1) ]
            for i,v in enumerate(window):
                if v<0:
                    window[i] += len(indices)
                elif v >= len(indices):
                    window[i] -= len(indices)
            
            self.sample_dists[idx] = [] 
            for j,jdx in enumerate(window[:-1]):
                for k,kdx in enumerate(window[j+1:]):
                    self.sample_dists[idx].append(euc_dist( [self.border_sample[jdx]['x'], self.border_sample[jdx]['y'] ],
                                                            [self.border_sample[kdx]['x'], self.border_sample[kdx]['y'] ] ))

    def create_angles(self, window_size = 10):
        
        # for the sampled points, create all pair-wise angles
        
        self.sample_angles = {}
        indices = self.border_sample.keys()
        for idx in [*indices]:
            window = [ idx + v for v in range(-window_size, window_size + 1) ]
            for i,v in enumerate(window):
                if v<0:
                    window[i] += len(indices)
                elif v >= len(indices):
                    window[i] -= len(indices)
            
            self.sample_angles[idx] = [] 
            for j,jdx in enumerate(window[:-1]):
                for k,kdx in enumerate(window[j+1:]):
                    self.sample_angles[idx].append(angle( [self.border_sample[jdx]['x'], self.border_sample[jdx]['y'] ],
                                                            [self.border_sample[kdx]['x'], self.border_sample[kdx]['y'] ] ))
                    
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
                d = sqrt( (x1-x2)**2 + (y1-y2)**2 )
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
       
        # puts points in order and compute center
        self.x_center = 0.0
        self.y_center = 0.0
        self.ordered_border = {} 
        for i,o in enumerate(ordered_pts):
            self.ordered_border[i] = { 'x':self.border[o]['x'],
                                       'y':self.border[o]['y'],
                                       'order':i}
            self.x_center += self.border[o]['x']
            self.y_center += self.border[o]['y']
        self.x_center /= len(self.border)
        self.y_center /= len(self.border)
            
        # verify clockwise orientation
        # gather angles from origin point to first 25% of points
        # in steps of 5 - get a collection of angles which should generally 
        # move in one direction clockwise or counter-clockwise
        angle_direction = 0
        for i in range(1, int(len(self.border)/4), 5):
            ang = angle( [self.border[0]['x'], self.border[0]['y']],
                         [self.border[i]['x'], self.border[0]['y']] )
            if ang > 0:
                angle_direction += 1 # clockwise
            elif ang < 0:
                angle_direction -= 1 # counter-clockwise
        
        # if general direction is not clockwise, reverse order
        if angle_direction > 0:
            new_order = {}
            for i,k in enumerate(list(self.ordered_border.keys())[::-1]):
                new_order[i] = { 'x':self.ordered_border[k]['x'],
                                 'y':self.ordered_border[k]['y'] }
            self.ordered_border = new_order
            
    def extend_border_sample(self, tail_length, reverse=False):
       
        # extend the sequence from the end to account for border effects
        self.ext_to_old_index = {} # dictionary to translate new indices to old indices
        
        if not reverse:
            self.border_sample_ext = copy.deepcopy(self.border_sample)
            self.ext_to_old_index = {i:i for i in range(len(self.border_sample))}
                                     
            for i,idx in enumerate(range(len(self.border_sample), len(self.border_sample) + tail_length)):
                self.border_sample_ext[len(self.border_sample) + i] = \
                   copy.deepcopy(self.border_sample[i])
                self.ext_to_old_index[idx] = i
                                     
        else:
            self.border_sample_ext = {}
            ext_to_old = {}
            for i,idx in enumerate(range(len(self.border_sample) - tail_length,
                                         len(self.border_sample))):
                self.border_sample_ext[i] = { 'orig_idx': self.border_sample[idx]['orig_idx'],
                                              'x': self.border_sample[idx]['x'],
                                              'y': self.border_sample[idx]['y']}
                ext_to_old[i] = idx
                    
            for i,idx in enumerate(range(0, len(self.border_sample))):
                self.border_sample_ext[tail_length + i] = \
                    { 'orig_idx':self.border_sample[idx]['orig_idx'],
                      'x': self.border_sample[idx]['x'],
                      'y': self.border_sample[idx]['y']}
                ext_to_old[tail_length + i] = idx
                
            # reverse target for complementarity between query and target
            self.border_sample_ext = { i:self.border_sample_ext[i]
                                       for i in list(self.border_sample_ext.keys())[::-1] } 
            self.ext_to_old_index = { len(ext_to_old) - k - 1: v for k,v in ext_to_old.items() }

    def reposition(self, source_window, destination, destination_window):
        
        # reposition this piece to the supplied target based on the supplied points window
        # for now, use the border_sample points
        for i,v in enumerate(destination_window):
            if v < 0:
                destination_window[i] += len(destination.border_sample)
            elif v >=len(destination.border_sample):
                destination_window[i] -= len(destination.border_sample)   
        destination_points= [destination.border_sample[q] 
                    for q in [list(destination.border_sample.keys())[i] 
                              for i in destination_window]]

        for i,v in enumerate(source_window):
            if v < 0:
                source_window[i] += len(self.border_sample)
            elif v >=len(self.border_sample):
                source_window[i] -= len(self.border_sample)   
        source_points = [self.border_sample[t] 
                  for t in [list(self.border_sample.keys())[::-1][i] 
                            for i in source_window]]
        
        xshift = int((sum([p['x'] for p in destination_points]) - \
                      sum([p['x'] for p in source_points])) / len(destination_window))
        yshift = int((sum([p['y'] for p in destination_points]) - \
                      sum([p['y'] for p in source_points])) / len(source_window))

        for p in self.border.items():
            p[1]['x'] += xshift
            p[1]['y'] += yshift
                    
    def merge(self, piece):
        
        # merge the supplied piece with this piece
        # assume pieces are positioned appropriately
        
        combo_array = {}
        min_x = 999999
        min_y = 999999
        max_x = -999999
        max_y = -999999

        for p in self.border.items():
            if p[1]['x'] not in combo_array.keys():
                combo_array[p[1]['x']] = []   
            combo_array[p[1]['x']].append(p[1]['y'])
            if p[1]['x'] < min_x:
                min_x = p[1]['x']
            if p[1]['x'] > max_x:
                max_x = p[1]['x']
            if p[1]['y'] < min_y:
                min_y = p[1]['y']
            if p[1]['y'] > max_y:
                max_y = p[1]['y']

        for p in piece.border.items():
            if p[1]['x'] not in combo_array.keys():
                combo_array[p[1]['x']] = []   
            combo_array[p[1]['x']].append(p[1]['y'])
            if p[1]['x'] < min_x:
                min_x = p[1]['x']
            if p[1]['x'] > max_x:
                max_x = p[1]['x']
            if p[1]['y'] < min_y:
                min_y = p[1]['y']
            if p[1]['y'] > max_y:
                max_y = p[1]['y']
                        
        self.compute_border(combo_array, min_x, max_x, min_y, max_y)
                        
    def compute_border(self, point_array, min_x, max_x, min_y, max_y):
        # compute new boundary
        # floodfill from exploratory 02 
        # convert sparse array to piece_coords complete array
        piece_coords = dict()
        composite_x = []
        composite_y = []
        checks = []
         
        for x in range(min_x-10, max_x+11):
            for y in range(min_y-10, max_y+11):
                if x not in piece_coords:
                    piece_coords[x] = dict()
        
                if y not in piece_coords[x]:
                    piece_coords[x][y] = dict()
        
                v = 1 # default to white point
                if x in point_array:
                    if y in point_array[x]:
                        v = 0 # black point
                        composite_x.append(x)
                        composite_y.append(y)
                        checks.append( (x,y) )
        
                piece_coords[x][y] = {'value': v,
                                      'left':None,
                                      'right':None,
                                      'up':None,
                                      'down':None,
                                      'visited':False,
                                      'outer_border':False}
            
        min_x = min(piece_coords.keys())
        max_x = max(piece_coords.keys())
        min_y = min(piece_coords[min_x].keys())
        max_y = max(piece_coords[min_x].keys())
       
        # create a place to store (x,y) coordinates
        outer_border = list()
        
        # link up the list
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                if x > min_x:
                    piece_coords[x][y]['left'] = (x-1, y)
                if x < max_x:
                    piece_coords[x][y]['right'] = (x+1, y)
                if y > min_y:
                    piece_coords[x][y]['down'] = (x, y-1)
                if y < max_y:
                    piece_coords[x][y]['up'] = (x, y+1)
                    
        # start flooding
        curr_x = min_x
        curr_y = min_y
        stack = list()
        
        while True:
            curr_node = piece_coords[curr_x][curr_y]
            curr_node['visited'] = True
           
            # check for black
            if curr_node['value'] == 0:
                curr_node['outer_border'] = True
                (curr_x, curr_y) = stack.pop()
                continue
                
            # try to expand right
            if curr_node['right'] is not None:
                stack.append( (curr_x, curr_y) )
                (curr_x, curr_y) = curr_node['right']
                curr_node['right'] = None
                continue
            if curr_node['down'] is not None:
                stack.append( (curr_x, curr_y) )
                (curr_x, curr_y) = curr_node['down']
                curr_node['down'] = None
                continue
            if curr_node['left'] is not None:
                stack.append( (curr_x, curr_y) )
                (curr_x, curr_y) = curr_node['left']
                curr_node['left'] = None
                continue
            if curr_node['up'] is not None:
                stack.append( (curr_x, curr_y) )
                (curr_x, curr_y) = curr_node['up']
                curr_node['up'] = None
                continue
            
            # if all directions fail, back up one if possible
            if len(stack) == 0:
                break
            else:
                (curr_x, curr_y) = stack.pop()
                       
        # inside, outside, and border
        border_x = []
        border_y = []

        for x in piece_coords.keys():
            for y in piece_coords[x].keys():
                if piece_coords[x][y]['outer_border']:
                    border_x.append(x)
                    border_y.append(y)
                    
        self.border = {}
        for i,(x,y) in enumerate(zip(border_x, border_y)):
            self.border[i] = { 'x':x,
                               'y':y, 
                               'order':None }
            
        self.order_border()
        self.sample_border(self.border_sampling_rate)
        self.create_distances(self.window_size)
        self.create_angles(self.window_size)
