# set the piece to work with
pn = 'C'

# import the puzzle piece and create a dictionary/linked list
p_in = open(pn + '.csv')
h = p_in.readline()

piece_coords = dict()

for l in p_in:
    tok = [ int(v) for v in l.rstrip().split(',') ]
    if tok[0] not in piece_coords:
      piece_coords[tok[0]] = dict()
      
    if tok[1] not in piece_coords[tok[0]]:
      piece_coords[tok[0]][tok[1]] = dict()
      
    piece_coords[tok[0]][tok[1]] = {'value':tok[2],
                                    'left':None,
                                    'right':None,
                                    'up':None,
                                    'down':None,
                                    'visited':False,
                                    'outer_border':False}
      
p_in.close()

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
curr_x = 1
curr_y = 1
stack = list()

while True:
    curr_node = piece_coords[curr_x][curr_y]
    curr_node['visited'] = True
    
    # check for black
    if curr_node['value'] == 0:
        curr_node['outer_border'] = True
        (curr_x, curr_y) = stack.pop()
        continue
        
    # try to exapnd right
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
        
fout = open(pn + '_border.csv','w')
fout.write('x,y\n')

# uncomment these to generate a figure showing the 
# inside, outside, and border
#ext = open(pn + '_outside.csv', 'w')
#ext.write('x,y\n')
#
#ins = open(pn + '_inside.csv', 'w')
#ins.write('x,y\n')

for x in piece_coords.keys():
    for y in piece_coords[x].keys():
        if piece_coords[x][y]['outer_border']:
           fout.write(','.join( [ str(x), str(y) ] ) + '\n')
#        else:
#            if piece_coords[x][y]['visited']:
#                ext.write(','.join( [str(x), str(y) ] ) + '\n')
#            else:
#                ins.write(','.join( [str(x), str(y) ]) + '\n')

fout.close()
#ext.close()
#ins.close()

        
    


            
  
