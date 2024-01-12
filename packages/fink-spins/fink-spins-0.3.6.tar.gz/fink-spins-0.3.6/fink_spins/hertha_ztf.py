import pandas as pd
import numpy as np
from fink_utils.sso.spins import estimate_hybrid_sso_params, add_ztf_color_correction

import io
import requests
import sys

# get ZTF data
r = requests.post(
     'https://fink-portal.org/api/v1/sso',
     json={
         'n_or_d': sys.argv[1],
         'withEphem': True,
         'output-format': 'json'
     }
)

pdf = pd.read_json(io.BytesIO(r.content))

# Combine all in V band
pdf = add_ztf_color_correction(pdf)
magpsf_red = pdf['i:magpsf_red'].values + pdf['color_corr'].values
filters = np.array(['V'] * len(pdf))

# Extract others
sigmapsf = pdf['i:sigmapsf'].values
phase = np.deg2rad(pdf['Phase'].values)
ra = np.deg2rad(pdf['i:ra'].values)
dec = np.deg2rad(pdf['i:dec'].values)

bounds = ([0, 0, 0, 0.3, 0, -np.pi / 2], [30, 1, 1, 1, 2 * np.pi, np.pi / 2])
p0 = [15.0, 0.15, 0.15, 0.8, np.pi, 0.0]
outdic = estimate_hybrid_sso_params(magpsf_red, sigmapsf, phase, ra, dec, filters, bounds=bounds, p0=p0)
print(outdic)

# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_context('poster')

# fig = plt.figure(figsize=(12, 6))

# pdf2 = pd.read_csv('135.csv')

#plt.plot(pdf['mag'].values, pdf['mag_red'].values, ls='', marker='o')
# plt.plot(pdf['i:jd'].values, pdf['i:magpsf_red'].values, ls='', marker='.')
# plt.plot(pdf2['jd_obs'].values, pdf2['mag_red'].values, ls='', marker='.')

# plt.show()
