# Covert a puzzle piece image to .csv for further processing
library(imager)

# For 3x3 puzzle, get the 9 pieces
pieces = c('NW', 'N', 'NE',
           'W', 'C', 'E',
           'SW', 'S', 'SE')

# for each piece, brighten/darken and extract XY coords
z <- sapply(pieces, function(pn) {
  p <- load.image(sprintf('%s.jpg', pn))
  pg <- grayscale(p)
  
  # trim to the maximum darkness
  pg[which(pg <= .25)] = 0
  pg[which(pg > .25)] = 1
  
  pg.df <- as.data.frame(pg)
  write.csv(pg.df, sprintf('%s.csv',pn), row.names = FALSE, quote=FALSE)
})
