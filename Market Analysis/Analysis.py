# ===============================
# Final Project
# XGBoost Implementation
#
# Code written by Patrick Keener
#     5/27/2021
#
# ===============================

import time
from math import inf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from xgboost import plot_tree

# input path

# Clean datas
folderPath = r'C:\tradingData\Sharadar\sectorData\GICS_Sector'
fileName = "Technology_GICS_sector_data.csv"
filePath = folderPath + "\\" + fileName
df = pd.read_csv(filePath)

# Keep only quarterly records, excluding restatements
df = df[df["dimension"] == "ARQ"]

# Keep only USD-denominated statements
df = df[df["currency"] == "USD"]

# Drop observations that don't have industry since that is what we're predicting
# and this is a supervised learning technique
df.dropna(axis = 0, inplace = True)

# Convert calendar date to date time format for TS manipulation
df["calendardate"] = pd.to_datetime(df["calendardate"])

# reset index
df.reset_index(drop = True, inplace = True)


# ===== Find Average Values for Items

# Average Assets
df["avgTotAssets"] = (df.groupby("ticker")["assets"].shift(0) 
+ df.groupby("ticker")["assets"].shift(1))/2

# Average Equity
df["avgTotEquity"] = (df.groupby("ticker")["equity"].shift(0) 
+ df.groupby("ticker")["equity"].shift(1))/2

# Average Liabilities
df["avgTotLiab"] = (df.groupby("ticker")["liabilities"].shift(0) 
+ df.groupby("ticker")["liabilities"].shift(1))/2


# === Du Pont Analysis

# # Ensure denominators are not = 0
# df[df["netinc"]== 0] = 1
# df[df["ebt"]== 0] = 1
# df[df["revenue"]== 0] = 1
# df[df["avgTotAssets"]== 0] = 1
# df[df["avgTotEquity"]== 0] = 1
# df[df["assets"]== 0] = 1
# df[df["equity"]== 0] = 1
# df[df["liabilities"]== 0] = 1


# Level 1
df["taxBurden"] = df["ebt"]/df["netinc"]
df["interestBurden"] = df["intexp"]/df["ebt"]
df["EBITmargin"] = df["ebit"]/df["revenue"]

# Adjust for divide by 0
df["taxBurden"].replace([np.inf, -np.inf], 1, inplace = True)
df["interestBurden"].replace([np.inf, -np.inf], 1, inplace = True)
df["EBITmargin"].replace([np.inf, -np.inf], 0, inplace = True)




# Level 2
df["profitMargin"] = df["EBITmargin"]*(1-df["interestBurden"])*(1-df["taxBurden"])
df["assetTurnover"] = df["revenue"]/df["avgTotAssets"]

# Adjust for divide by 0
df["assetTurnover"].replace([np.inf, -np.inf], 1, inplace = True)

# Level 3
df["ROA"] = df["profitMargin"] * df["assetTurnover"]
df["leverageRatio"] = df["avgTotAssets"]/df["avgTotEquity"]

# Adjust for divide by 0
df["leverageRatio"].replace([np.inf, -np.inf], 100, inplace = True)

# Level 4
df["ROE"] = df["ROA"] * df["leverageRatio"]


# Solvency Ratios
df["debtToAssets"] = df["debt"]/df["assets"]
df["debtToCapital"] = df["debt"]/(df["liabilities"] + df["equity"])
df["debtToEquity"] = df["debt"]/df["equity"]
df["interestCoverageRatio"] = df["ebit"]/df["intexp"]

# Adjust for divide by 0
df["debtToAssets"].replace([np.inf, -np.inf], 100, inplace = True)
df["debtToCapital"].replace([np.inf, -np.inf], 100, inplace = True)
df["debtToEquity"].replace([np.inf, -np.inf], 100, inplace = True)
df["interestCoverageRatio"].replace([np.inf, -np.inf], 1, inplace = True)



# Dividend Ratios
df["divPayRt"] = df["ncfdiv"]/df["netinc"]
df["plowBackRt"] = (df["netinc"] - df["ncfdiv"])/df["netinc"]
df["sustGrowthRt"] = df["ROE"] * df["plowBackRt"]

# Adjust for divide by 0
df["divPayRt"].replace([np.inf, -np.inf], 1, inplace = True)
df["plowBackRt"].replace([np.inf, -np.inf], -1, inplace = True)


# Remove unnecessary Columns
colsToDrop = ["ticker", "dimension", "sector", "calendardate", "currency"]
df.drop(inplace = True, labels = colsToDrop, axis = 1)
del colsToDrop

colvals = df["scalemarketcap"].drop_duplicates().sort_values()
df["scalemarketcap"].drop_duplicates()

df["scalemarketcap"] = pd.Categorical(df["scalemarketcap"]
, categories =colvals, ordered = True)
del colvals

df.drop("scalemarketcap", inplace = True, axis = 1)

df.dropna(axis = 0, inplace = True) # drop NAs again

# ==============================================================
# ===================== Begin XGBoost ==========================
# ==============================================================


y = df["industry"]
x = df.drop(labels = ["industry"], axis = 1)



# Create Train and Test sets
xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = .2)

del x, y


# ==== Train Model

model = XGBClassifier(n_estimators = 10)

start = time.time()

model.fit(xtrain, ytrain)

end = time.time()
totTime = end - start
print(totTime)

ypred = model.predict(xtest)


# ========== Evaluation

# accuracy score & contingency table
accuracy_score(ytest, ypred)
pd.crosstab(ypred, ytest, margins = False)


plot_tree(model, num_trees = 1, rankdir = "LR")
plt.show()