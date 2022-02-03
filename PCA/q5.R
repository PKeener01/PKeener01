source("PCA_Plot.R")

library(car)
library(corrplot)
library(ggplot2)
library(psych)

inPath = file.path("c:", "Users", "smpat", "OneDrive", "Desktop"
                   , "HW", "hw3")

employ = read.table(file.path(inPath, "Employment.txt"), header = TRUE, sep = "\t")
  
head(employ)

summary(employ)

prin = prcomp(employ[,-c(1)], scale = T)
prin
plot(prin)
abline(1,0,col="red")
summary(prin)

print$varimax



a = principal(employ[,-c(1)], nfactors = 4, rotate = "none")
print(a)
plot(a)

s

b = principal(employ[,-c(1)], rotate="varimax", nfactors = 3)
print(b$loadings, cutoff = .4, sort=T)

max(b$scores[,1])
min(b$scores[,1])

max(b$scores[,2])
min(b$scores[,2])

b$scores

 

fa.parallel(employ[,-c(1)], nfactors = 9)
