#%%
import math
import numpy as np
from tifffile import imread
import os
from os.path import join
from skimage.measure import regionprops
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


in_path = './masks_for_binary/20230410_pos003'
imgname_readin = [i for i in os.listdir(in_path)]


# %%
centroids = []
#mean_center = []
for i in imgname_readin:
    img_array = imread(join(in_path, i))
    print(img_array.shape)

    props = regionprops(img_array)

    for prop in props:
        centroid = prop.centroid
        centroids.append(centroid)

    # Print the centroids
    for label_id, centroid in enumerate(centroids, start=1):
        print(f"Label {label_id} centroid: {centroid}")

    centroid_array = np.array(centroids)
    center = centroid_array.mean(axis=0)
    #mean_center = center.mean(axis=0)

    # Print the center coordinates
    print("Center coordinates:", center)
    print("Center (z, y, x):", center[0], center[1], center[2])
    #print("Mean center:", mean_center)

# %%
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(center[2], center[1], center[0], c='red', marker='o')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
# %%
plt.imshow(img_array[32])
plt.plot(center[2], center[1], '.', markersize=10, color='red')