#%%
import matplotlib.pyplot as plt
import numpy as np
from tifffile import imread, imwrite
import os
from os.path import join

from skimage.measure import regionprops
# %%

in_path = './2023_06_23_masks'
imgname_readin = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2.tiff'
# imgname_readin = [i for i in os.listdir(in_path) if (('.tif' in i) and ('20230410' in i))]
img_array = imread(join(in_path,imgname_readin))
print(img_array.shape)
# %% 

# Takes numpy array representing an image and threshold value
# def remove_pixels(image_readin, threshold):
#     img_array = imread(join(in_path,image_readin))
#     removed_count = np.sum(img_array < threshold) #used to count the number of true values, or count of removed pixels
#     img_array[img_array > threshold] #compares pixels that are smaller than threshold, assigns true mask
#     return img_array, removed_count

# Define threshold value
# image_array = np.array([[200, 100, 150], [50, 180, 75], [220, 110, 160]])

# new_image, count = remove_pixels(imgname_readin, threshold_value)
# print(new_image.shape)
# print(np.array_equiv(new_image, img_array))
# print("Modified Image Array:")
# print(new_image)
# print("Number of pixels removed:", count)


# %%
regions = regionprops(img_array)
print(regions)
# %%
threshold_value_area = 10000

arealist = []
threshold_area_array = []
count_removed_first = 0
for i in range(len(regions)):
    props = regions[i]
    area = props.area
    if area < threshold_value_area:
        labels_remove = img_array == i
        img_array[labels_remove]=0
        count_removed_first += 1 # count_removed = count_removed + 1
    else:
        threshold_area_array.append(area)
    arealist.append(area)

# %%

threshold_value_axis = 30

axis_maj_list = []
threshold_axis_array = []
count_removed_second = 0
for props in regions:
    axis_major = props.axis_major_length
    if axis_major < threshold_value_axis:
        count_removed_second += 1 # count_removed = count_removed + 1
    else:
        threshold_axis_array.append(axis_major)
    axis_maj_list.append(axis_major)

# %%
print(f"Removed: {count_removed_first} area values")
print(arealist)
plt.hist(arealist)
plt.show()
plt.hist(threshold_area_array)
plt.show()

# %%
print(f"Removed: {count_removed_second} axis major values")
print(axis_maj_list)
plt.hist(axis_maj_list)
plt.show()
plt.hist(threshold_axis_array)
plt.show()

# %%
out_path = './2023_06_23_masks_modified'

imgname_readin=imgname_readin.replace(".tiff","_modified.tiff")
imwrite(join(out_path,imgname_readin),img_array)

# %% 
# plt.xlim(left=20, right=200)

# %%
# plt.hist(arealist)
# plt.show()


# %%
