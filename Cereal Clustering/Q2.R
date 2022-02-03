library(CCA)
library(yacca)



###################################################################
# This is a nice function for computing the Wilks lambdas for 
# CCA data from the CCA library's method
# It computes the wilkes lambas the degrees of freedom and the 
# p-values
###################################################################

ccaWilks = function(set1, set2, cca)
{
  ev = ((1 - cca$cor^2))
  ev
  
  n = dim(set1)[1]
  p = length(set1)
  q = length(set2)
  k = min(p, q)
  m = n - 3/2 - (p + q)/2
  m
  
  w = rev(cumprod(rev(ev)))
  
  # initialize
  d1 = d2 = f = vector("numeric", k)
  
  for (i in 1:k) 
  {
    s = sqrt((p^2 * q^2 - 4)/(p^2 + q^2 - 5))
    si = 1/s
    d1[i] = p * q
    d2[i] = m * s - p * q/2 + 1
    r = (1 - w[i]^si)/w[i]^si
    f[i] = r * d2[i]/d1[i]
    p = p - 1
    q = q - 1
  }
  
  pv = pf(f, d1, d2, lower.tail = FALSE)
  dmat = cbind(WilksL = w, F = f, df1 = d1, df2 = d2, p = pv)
}




# Load data from file into DF
dir_data_in <- file.path("c:", "Users", "smpat",'Desktop',
                         "HW 5", "data_marsh_cleaned.csv")

df <- read.csv(dir_data_in)


# Break data into 2 subsets
water <- df[,2:6]
ground <- df[,7:9]

# Get canonical correlation
ccWater = cc(water, ground) 

# Conduct Wilks test
wilksWater = ccaWilks(water, ground, ccWater)
round(wilksWater, 2)

# Get correlations & coefficients
ccWater$cor 
# get loadings
ccWater$scores$corr.X.xscores 
ccWater$scores$corr.Y.yscores




ccWater$xcoef 
ccWater$ycoef 



c = matcor(water, ground) 
img.matcor(c, type = 2)


# The first correlation factor is made up of the listed amounts of each variate
# correlated with the other.  Think PCA.

ccWater$cor # Contains correlations for the variates
ccWater$xcoef # x-variables are multiplied by this amount to calc score
ccWater$ycoef 

scores = ccWater$scores 
cor(scores$xscores[,1], scores$yscores[,1]) # same as above ccWater$cor[1]


