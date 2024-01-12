import pandas as pd
import numpy as np
from fink_utils.sso.spins import estimate_hybrid_sso_params
import fink_utils
print(fink_utils.__file__)

pdf = pd.read_csv('135.csv')
print(pdf.columns)
magpsf_red = pdf['mag_red'].values # - 5 * np.log10(pdf['dobs'].values * pdf['dhelio'].values)
sigmapsf = pdf['mag_red'].values
phase = np.deg2rad(pdf['phase'].values)
ra = np.deg2rad(pdf['ra_obs'].values)
dec = np.deg2rad(pdf['dec_obs'].values)
filters = pdf['filter'].values

bounds = ([0, 0, 0, 0.1, 0, -np.pi / 2], [30, 1, 1, 1, 2 * np.pi, np.pi / 2])
outdic = estimate_hybrid_sso_params(magpsf_red, sigmapsf, phase, ra, dec, filters, bounds=bounds)
print(outdic)

"""
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('poster')

fig = plt.figure(figsize=(12, 6))

#plt.plot(pdf['mag'].values, pdf['mag_red'].values, ls='', marker='o')
plt.plot(pdf['jd_obs'].values, pdf['mag'].values, ls='', marker='.')
plt.plot(pdf['jd_obs'].values, pdf['mag_red'].values, ls='', marker='.')

plt.show()
"""
