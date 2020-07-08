# Jigsaw
A jigsaw puzzle solver project

The intent is to develop an algorithm that can solve a jigsaw puzzle.  

Directories:

exploratory/ - all the file here came about during exploratory work to get an idea of how to approach the project.  Sub-directories are numbered in order of exploratory work.  The files in piece images/ and representations/ are duplicated throughout the exploratory/ sub-directories to remain consistent with how I approached the problem, and are duplicated in these two directories to gather all the results in one place.

	01_Jigsaw_JPGtoXY - simply convert the individual piece JPG files to .csv files.

	02_IdentifyBorder - covert the XY-RGB values to an exterior border one pixel wide.

	03_OrderBorderPoints - Put the XY values into an ordered list

	04_PairwiseDistances - Calculate all pairwise distances for windows around all points

	05_CurvatureMatching - Dynamic programming approach using each point's pairwise distances as a curvature metric.

	06_EuclideanMaching - Dynamic programming approach using sum of Euclidean distances of paired points between pieces for a window around a point of interest.  This method performed quite well in early tests.

	piece_images - all images generated in exploratory work

	representations - all .csv files with piece representations generated in exploratory work

  puzzle_images - this contains the original 3x3 .jpg I used.  The individual pieces are labeled by the directional location of the piece - C = Central, N = North, SW = SouthWest, etc. C_OutBorderIn.jpg was generated to verify the one pixel border work.

9x9_refinement/ - After exploratory work, start to pull all the code together into a useful design.  


