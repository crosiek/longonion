#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

def translate_image(source_image, dx, dy):
    translation_matrix = np.array([[1, 0, dx],
                                   [0, 1, dy]],
                                  dtype=np.double)
    result = cv2.warpAffine(source_image, translation_matrix, (0,0), flags=cv2.INTER_CUBIC)
    return result


def squared_distance(img1, img2):
    return np.sum((np.double(img1)-np.double(img2))**2)


def main(argv):
    global image

    image = cv2.imread('sample1.jpg')
    # cv2.imshow('Image', translate_image(image, 15.2, 1.2))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Generate sample translated image
    translated_image = translate_image(image, 20, 0)

    # Perform rough mesh optimization
    dxs, dys = np.meshgrid(np.linspace(-100,100,9), np.linspace(-100,100,9))
    distances = np.vectorize(lambda dx, dy: squared_distance(translated_image, translate_image(image, dx, dy)))(dxs, dys)
    idx = np.argmin(distances)
    p0 = (dxs.flat[idx], dys.flat[idx])

    # Run minimizer to improve fit
    fun = lambda p: squared_distance(translated_image, translate_image(image, *p))
    p_steps = []
    def callback(p):
        print("Step: " + str(p))
        p_steps.append(p)
    optres = scipy.optimize.minimize(fun, p0, callback=callback, method='trust-constr')
    print(optres)

    # Plot meshgrid
    plt.contourf(dxs, dys, distances)
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
