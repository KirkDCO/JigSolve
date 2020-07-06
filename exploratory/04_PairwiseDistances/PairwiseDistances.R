# set the piece of interest filename suffix
n <- 'S'
p <- read.csv(sprintf('%s_border_ordered.csv',n))

plot(p$x, p$y, pch=19, cex=.25)

# sample every 5th point, arbitray choice
i <- as.integer(seq(1,nrow(p), by=5)) 
points(p$x[i], p$y[i], pch=19, col='blue')
p_samp <- p[i,]
p_samp$order = NULL

# create a window of 10 samples points on either side
# 10 is also an arbitrary choice
pts <- c(c(-10:-1),0,c(1:10)) + 1
pts <- ifelse(pts<=0, pts+nrow(p_samp), pts)
pts <- ifelse(pts>nrow(p_samp), pts-nrow(p_samp), pts)
z <- sapply(pts, function(j) {
  points(p_samp$x[j], p_samp$y[j], pch=19, col='orange')
})

# compute all pairwise distances between points
dists <- t(sapply(1:nrow(p_samp), function(i) {
  pts <- c(c(-10:-1),0,c(1:10)) + i
  pts <- ifelse(pts<=0, pts+nrow(p_samp), pts)
  pts <- ifelse(pts>nrow(p_samp), pts-nrow(p_samp), pts)
  m <- rbind(p_samp[pts,])  
  dist(m)
}))
dists <- cbind(as.integer(rownames(p_samp)), dists)

write.table(dists, sprintf('%s_dists.csv',n), quote=FALSE, sep = ',',
          row.names = FALSE, col.names = FALSE)
# note that the samples point number is 1-based, which will mess with
# interpreting in Python
