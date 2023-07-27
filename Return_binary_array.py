#%%
import numpy as np
from tifffile import imread, imwrite
import os
from os.path import join
import matplotlib.pyplot as plt

#%%
in_path = './masks_for_binary/m4_masks'
imgname_readin = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2.tiff'
#imgname_readin = [i for i in os.listdir(in_path) if (('.tif' in i) and ('20230410_pos003_t00' in i))]
#counter = 1
image_array = imread(join(in_path,imgname_readin))
print("Shape of image array:", image_array.shape)

#find number of labels 
max_value = np.max(image_array)
uq_index = np.unique(image_array)
print("Total labels: ", max_value + 1)
print(uq_index)

# %%

# 3D image array called 'image_array'
# Shape of image_array: (height, width, channels)

# Create a new array to store the binary values
binary_image = image_array

# Iterate over each dimension of the image array
for i in range(image_array.shape[0]):
    for j in range(image_array.shape[1]):
        for k in range(image_array.shape[2]):
            # Check if the value is greater than or equal to 1
            if image_array[i, j, k] >= 1:
                # Set the corresponding value in the binary image array to 1
                binary_image[i, j, k] = 1
            else:
                # Set the corresponding value in the binary image array to 0
                binary_image[i, j, k] = 0

print("Shape of binary image:", binary_image.shape)
print(binary_image)
unq_val = np.unique(binary_image)
print(unq_val)
#%%
out_path = './binary_images'

imgname_readin=imgname_readin.replace(".tiff","_binary_image_m4.tiff")
outpath_file_path = join(out_path, imgname_readin)
imwrite(outpath_file_path, binary_image)

