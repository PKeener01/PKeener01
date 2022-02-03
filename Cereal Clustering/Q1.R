library(MASS)
library(dbscan)

# Load data from file into DF
dir_data_in <- file.path("c:", "Users", "smpat",'Desktop',
                         "HW 5", "kellog.dat")

# ==== a ====
df <- read.table(dir_data_in, header=FALSE, sep = ""
                 , skip=2, row.names = 1)


# ==== b ====
# Compute Euclidean distance matrix
distDF = dist(df)


# ==== c ====
# run MDS using isoMDS
cerealDF <- isoMDS(distDF)

# Create the graph
plot(cerealDF$points, type = "n")

# Plot the points
text(cerealDF$points, labels = as.character(1:nrow(df)))

# Make a sheppard diagram
cereal.sh = Shepard(distDF, cerealDF$points)
plot(cereal.sh, pch = ".")
lines(cereal.sh$x, cereal.sh$yf, type = "S", col = "red")


# ==== e ====


# k means
dDF <- dist(df)
km <- kmeans(dDF,3)
fit <- cmdscale(dDF, eig=TRUE, k=2)
x = fit$points[, 1]
y = fit$points[, 2]
plot(x,y, col=km$cluster, pch = 18)

# density
dens = dbscan(df, eps = .75, minPts = 2)
dens
plot(x, y, col=dens$cluster + 1, pch = 18)


# Hierarchical
df = na.omit(df)
d = dist(df) 

clust1 = hclust(d)
plot(clust1, cex=0.7, hang = -1)

# ===== f =====

clust2 = cutree(clust1,k=3)
plot(x, y, col = clust2, pch = 18, cex = 1.5)

# Plot the points
plot(x, y, type = "n")
text(x, y, labels = rownames(df), col = clust2)
