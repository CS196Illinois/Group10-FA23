from sklearn.decomposition import PCA
import numpy as np
import pandas
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.ndimage import gaussian_filter1d

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

# fig = plt.figure()
# ax = fig.add_subplot()
columns = ["AccZ", "AccY", "AccX"]
data = pandas.read_csv(r"data.csv", usecols=columns)
data = data.apply(pandas.to_numeric, errors='coerce')
data = data.dropna()
accx = data['AccX']  # Replace 'label_column' with the name of the column containing the labels
accy = data['AccY']
accz = data['AccZ']

accx, accy, accz = accx.to_numpy().reshape(-1, 1), accy.to_numpy().reshape(-1, 1), accz.to_numpy().reshape(-1, 1),

def get_fft(signal):
    N = len(signal)
    T = 1.0 / 667
    y = signal
    yf = fft(y)
    xf = fftfreq(N, T)[:N // 2]
    return xf[1:], 2.0/N * np.abs(yf[1:N//2])


def get_pca(x, y, z):
    pca = PCA(n_components=1)
    accelerations = np.array([x, y, z])
    accelerations = accelerations.reshape((accelerations.shape[0], accelerations.shape[1]))
    x_pca = pca.fit_transform(accelerations.T)
    return x_pca


fig, (ax1, ax2) = plt.subplots(1, 2)
magnitudes = [np.linalg.norm(vec) for vec in zip(accx, accy, accz)]
xf1, yf1 = get_fft(magnitudes)
ax1.plot(xf1, yf1)
smoothed_magnitudes = magnitudes - gaussian_filter1d(magnitudes, sigma=0.5)
smoothed_magnitudes = gaussian_filter1d(smoothed_magnitudes, sigma=2)
xf2, yf2 = get_fft(smoothed_magnitudes)
ax2.plot(xf2, yf2)
plt.savefig('fourier.png')

# ax.scatter(accx, accy, accz)
# plt.show()
# scaler = StandardScaler()
# x_std = scaler.fit_transform(x)
#
#

#
# plt.title("Analysis")
#
# plt.show()
