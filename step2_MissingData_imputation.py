import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import missingpy
from missingpy import KNNImputer
from sklearn import linear_model
import math

df = pd.read_csv('portfolio.csv', delimiter=',')

#index contains indices from 5 categories of assets
index = pd.read_csv('index.csv', delimiter=',')

#####################  regression #####################
# Here we assume that the portfolio can be constructed with major asset index
# Therefore the missing data (portfolio return) can be imputed by  

# convert to returns
return_1 = df['price']/df['price'].shift(1) - 1
Equity = (index['Equity']/index['Equity'].shift(1) - 1).to_frame()
Utility = (index['Utility']/index['Utility'].shift(1) - 1).to_frame()
FI = (index['Fixed Income']/index['Fixed Income'].shift(1) - 1).to_frame()
REIT = (index['REIT']/index['REIT'].shift(1) - 1).to_frame()
Commodity = (index['Commodity']/index['Commodity'].shift(1) - 1).to_frame()

df2 = return_1.to_frame()

#remove outliers (2 times the standard deviation from the mean)
df2.loc[abs(df2['price'] - np.mean(df2['price'])) > 2*np.std(df2['price']), 'price'] = np.nan

df['returns'] = df2
df['Equity'] = Equity
df['Utility'] = Utility
df['FI'] = FI
df['REIT'] = REIT
df['Commodity'] = Commodity

df1 = df

#remove tail days returns
df1.loc[df1['date'] == '2018-02-02', 'returns'] = np.nan
df1.loc[df1['date'] == '2018-02-05', 'returns'] = np.nan
df1.loc[df1['date'] == '2018-02-08', 'returns'] = np.nan
df1.loc[df1['date'] == '2018-03-22', 'returns'] = np.nan

df1 = df1.dropna()

x_train = df1[['Equity', 'Utility', 'FI', 'REIT', 'Commodity']]


y_train = df1['returns'] 

#perform multivariate regression
regr = linear_model.LinearRegression(fit_intercept = True)
regr.fit(x_train, y_train)
y_pred = regr.predict(x_train)

df3 = df.drop(0)

new_y_pred = regr.predict(df3[['Equity', 'Utility', 'FI', 'REIT', 'Commodity']])
df3['y_pred'] = new_y_pred

#only use predicted values to fill in days that data are missing
df3.loc[np.isnan(df3['returns']) == True, 'returns'] = df3.loc[np.isnan(df3['returns']) == True, 'y_pred']
df3.to_csv('./Data/portfolio_interpolate1.csv')
#################################################################


##################### KNN Imputation #####################
# KNN did outperform regression
#imputer = KNNImputer()

#lowerbound = np.mean(df['price']) - 2*np.std(df['price'])
#upperbound = np.mean(df['price']) + 2*np.std(df['price'])

##lowerbound
##upperbound

#df.loc[df['price'] < np.squeeze(lowerbound), 'price'] = np.nan
#df.loc[df['price'] > np.squeeze(upperbound), 'price'] = np.nan


#df_price = imputer.fit_transform(df['price'].reshape(-1, 1))

#### df_price stores imputated portfolio price ###
#plt.plot(df_price)
##########################################################

###################### EM algorithm# ########################
#EM algorithm did not outperform regression
# def Normalmixture(x,k,mu,sigma,Lambda,em_iter=50):
#     """
#     This function inputs the data (x) and the number of components (k)
#     as well as initials estimates for the means (mu), std deviations (sigma),
#     and probabilities (lambda).  You should also include arguments for 
#     determining convergence although here I just have a fixed number of
#     iterations (em.iter) of the EM algorithm with a default of 50 iterations
#     """
#     n = x.shape[0]
#     x = sorted(x)
#     Vars = sigma**2
#     means = mu
#     lam = Lambda/sum(Lambda)  # guarantee that lambdas sum to 1
#     delta = np.zeros((n*k,k)) 
#     # In this template, we have a fixed number of EM iterations; you may want 
#     # to have a more refined convergence criterion 
#     # compute updates of deltas 
#     for s in range(0,em_iter):
#         for i in range(0,n):
#             xi = x[i]
#             for j in range(0,k):
#                 mj = means[j]
#                 varj = Vars[j]
#                 denom = 0
#                 for u in range(0,k):
#                     mu = means[u]
#                     varu = Vars[u]
#                     denom = denom + lam[u]*dnorm(xi,mu,math.sqrt(varu))
#                 delta[i,j] = lam[j]*dnorm(xi,mj,sqrt(varj))/denom
#         # compute updated estimates of means, variances, and probabilities - the 
#         # function weighted.mean may be useful here for computing the estimates of
#         # the means and variances.
#         for j in range(0,k):
#             #deltaj = as.vector(delta[,j])
#             #Lambda[j] = mean(deltaj)
#             deltaj = delta[:,j]
#             Lambda[j] = mean(deltaj)
#             means[j] = weighted.mean(x, deltaj/sum(deltaj))
#             Vars[j] = weighted.mean((x - means[j])^2, deltaj/sum(deltaj))    
#         lam = Lambda/sum(Lambda)
#         l = 0
#         L = 0
#         for i in range(0,n):
#             for j in range(0,k):
#                 l = l + dnorm(x[i], means[j], sqrt(Vars[j]))*lam[j]
#                 L = L + log(l)
#                 l = 0 
#       # Log-likelihood computation - you may want to compute this after each EM
#       # iteration (i.e. within the outer loop)
#     loglik = L        
#     r = list(mu=means,var=Vars,delta=delta,Lambda=Lambda,loglik=loglik)
#     return r
