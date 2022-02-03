source("PCA_Plot.R")

library(car)
library(corrplot)
library(ggplot2)
library(psych)

inPath = file.path("c:", "Users", "smpat", "OneDrive", "Desktop"
                   , "HW", "hw3")

census = read.csv(file.path(inPath, "Census2.csv"))
head(census)

cVar <- cov(census)

plot(census, pch = 16, col="steelblue2")


summary(prcomp(cov(census)))
prcomp(cor(census))

pca = prcomp(census, scale = T)
pca
summary(pca)
pca$scale


# b
census2 = census
census2$MedianHomeVal = census$MedianHomeVal/100000

head(census2)
prcomp(census2)
summary(prcomp(census2))

# c - no code
# d
prcomp(cor(census2))
summary(prcomp(cor(census2)))

# e - corr test
m=cor(census)
corrplot(m, method="ellipse")
print(corr.test(census), short=FALSE)
