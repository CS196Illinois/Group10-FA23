from sklearn.decomposition import PCA
import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
columns = ["AccZ", "AccY", "AccX"]
data = pandas.read_csv(r"data.csv", usecols = columns)
data = data.apply(pandas.to_numeric, errors='coerce')
data = data.dropna()
x = data['AccX']   # Replace 'label_column' with the name of the column containing the labels
y = data['AccY']
z = data['AccZ']



# Standardize the features
scaler = StandardScaler()
x_std = scaler.fit_transform(x)

pca = PCA()
x_pca = pca.fit_transform(x_std)

plt.scatter(x_pca[:, 0], x_pca[:, 1], c=y, cmap='red')

plt.title("Analysis")

plt.show()
