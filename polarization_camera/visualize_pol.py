#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib as mpl
import imageio
import PIL
import scipy.ndimage
import scipy.signal

imgs = []
for i in range(4):
    # Load grayscale image
    imgs.append(np.array(PIL.Image.open(f'images/img1-{i+1}.jpg').convert("L")).astype(float))

    # Load single color channel
    # imgs.append(np.array(PIL.Image.open(f'images/img1-{i+1}.jpg'))[:,:,1].astype(float))

    # Blur image
    imgs[-1] = scipy.ndimage.gaussian_filter(imgs[-1], 1)

    # Crop image
    # imgs[-1] = imgs[-1][200:450,300:600]

    # Load using imageio instead
    # imgs.append(np.array(imageio.Image.open(f'images/img-2-{i+1}.jpg')).astype(float))

    # TODO: Manually convert the color channels to grayscale
    # rgb_weights = np.array([0.3, 0p.6, 0.1])

avg_img = np.mean(np.array(imgs), axis=0)

# Stokes parameters
S0 = (imgs[0] + imgs[1] + imgs[2] + imgs[3])/2
S1 = imgs[0] - imgs[1]
S2 = imgs[2] - imgs[3]
p = np.sqrt(S1**2 + S2**2)/S0
psi = np.arctan2(S1, S2)/2
# Cf. https://en.wikipedia.org/w/index.php?title=Stokes_parameters&oldid=873298000

# Plot angle
# plt.figure()
# normalizer = matplotlib.colors.Normalize(vmin=0, vmax=np.pi)
# tmp = (p[:,:,None]*matplotlib.cm.ScalarMappable(cmap='hsv', norm=normalizer).to_rgba(psi)*255)[:,:,0:3]
# plt.imshow(tmp.astype(np.uint8), cmap='hsv', vmin=0, vmax=np.pi)
# plt.colorbar()

# Overlay angle
plt.figure()
gray_img = np.dstack((avg_img,)*3)
angle_img = mpl.cm.hsv(psi/np.pi)[:,:,0:3]*255
p = (0.8/p.max()) * p[:,:,None] # normalize and reshape
# Linear interpolation between pol. angle and grayscale intensity
interp_img = (p**2*angle_img + (1-p)*(gray_img))
plt.imshow(interp_img.astype(np.uint8))
plt.ion()
plt.show()

# Local variables:
# compile-command: "python -i visualize_pol.py"
# End:
