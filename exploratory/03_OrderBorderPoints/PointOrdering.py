import math

# load the piece points
pn = 'W'

p_in = open(pn + '_border.csv')
h = p_in.readline()

border = dict()

for i,l in enumerate(p_in):
    tok = l.rstrip().split(',')
    border[i] = { 'x':int(tok[0]),
                  'y':int(tok[1]), 
                  'order':None }
p_in.close()

# create dictionary to hold order of points by key
k = border.keys()
dist_mat = [[999999 for i in range(len(k))] for j in range(len(k))] 

for i in range(0,len(k)-1):
    for j in range(i+1,len(k)):
        x1 = border[i]['x']
        x2 = border[j]['x']
        y1 = border[i]['y']
        y2 = border[j]['y']
        d = math.sqrt( (x1-x2)**2 + (y1-y2)**2 )
        dist_mat[i][j] = d
        dist_mat[j][i] = d
      
# set the first point
current_pt = 0
ordered_pts = []
early_stop = False

# step through points finding the closest to create the border order
for i in range(len(k)):
    border[current_pt]['order'] = i
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
        
        if border[dist_idx]['order'] is None:
            current_pt = dist_idx
            break
        
    if early_stop:
        break
        
fout = open(pn + '_border_ordered.csv', 'w')
fout.write('x,y,order\n')

for i,o in enumerate(ordered_pts):
    fout.write(','.join([ str(border[o]['x']),
                          str(border[o]['y']),
                          str(i) ]) + '\n')
fout.close()
    
            
            
            
