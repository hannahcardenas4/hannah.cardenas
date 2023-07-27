#%%
import numpy as np
from tifffile import imread, imwrite
import os
from os.path import join
from skimage import measure, morphology
import matplotlib.pyplot as plt
from skimage import io
from scipy.ndimage import median_filter, grey_dilation,grey_erosion
from skimage.morphology import erosion
from skimage.transform import rescale,resize
import raster_geometry as rg
import sys

in_path = './masks_for_binary/200ms_exposure_Pos3'
imgname_readin = [i for i in os.listdir(in_path)]
# print(imgname_readin.shape)
#%%

print("Applying median filter masks")

ellipsoid = rg.ellipsoid((2,4,4),semiaxes=(1,2,2))
big_ellipsoid = rg.ellipsoid((4,8,8),semiaxes=(2,4,4))
mask_list = []
for i in imgname_readin:
    mask_3d = imread(join(in_path, i))
    sz,sx,sy = mask_3d.shape
    # Calculate median filter of the masks
    
    mask_3d = median_filter(mask_3d,footprint=ellipsoid,output=np.uint8)
    border_mask = grey_dilation(mask_3d,footprint=ellipsoid) != grey_erosion(mask_3d,footprint=ellipsoid)
    mask_3d[border_mask] = 0
    mask_3d = grey_dilation(mask_3d,footprint=ellipsoid)
    #median_3d = erosion(mask_3d,footprint=np.ones((2,4,4)))
    
    
    #imgname=maskname.replace(".tiff","_median.tiff")
    #io.imsave(join(mask_path,imgname),mask_3d,check_contrast=False)
    mask_list.append(mask_3d)
    
#%%
print("Generating binary arrays:")

#find number of labels 
unique_values = []
binary_images = []
for mask in mask_list:
    #image_array = imread(join(in_path, i))
    #print("Shape of image array:", image_array.shape)

    uq_index = np.unique(mask)
    n_labels = len(uq_index)
    unique_values.append(n_labels)
    #print(uq_index)
    #print(n_labels)

    binary_image = mask

    # Iterate over each dimension of the image array
    for j in range(mask.shape[0]):
        for k in range(mask.shape[1]):
            for l in range(mask.shape[2]):
                # Check if the value is greater than or equal to 1
                if mask[j, k, l] >= 1:
                    # Set the corresponding value in the binary image array to 1
                    binary_image[j, k, l] = 1
                else:
                    # Set the corresponding value in the binary image array to 0
                    binary_image[j, k, l] = 0

    print("Shape of binary image:", binary_image.shape)
    #print(binary_image)
    #unq_val = np.unique(binary_image)
    #n_binary_labels = len(unq_val)
    binary_images.append(binary_image)
    

print("Stored Unique Values:", unique_values)
#%% 
#print("Applying median filter masks")

# ellipsoid = rg.ellipsoid((2,4,4),semiaxes=(1,2,2))
# big_ellipsoid = rg.ellipsoid((4,8,8),semiaxes=(2,4,4))
# for i in binary_images:
#     mask_3d = np.array(i)
#     sz,sx,sy = mask_3d.shape
#     # Calculate median filter of the masks
    
#     mask_3d = median_filter(mask_3d,footprint=ellipsoid,output=np.uint8)
#     border_mask = grey_dilation(mask_3d,footprint=ellipsoid) != grey_erosion(mask_3d,footprint=ellipsoid)
#     mask_3d[border_mask] = 0
#     mask_3d = grey_dilation(mask_3d,footprint=ellipsoid)
#     #median_3d = erosion(mask_3d,footprint=np.ones((2,4,4)))
    
    
#     #imgname=maskname.replace(".tiff","_median.tiff")
#     #io.imsave(join(mask_path,imgname),mask_3d,check_contrast=False)
#     binary_images = mask_3d
    

#%%

print("Creating consensus image")

def create_consensus_image(binary_images):
    consensus_image = np.median(binary_images, axis=0)
    print("Shape of consensus image:", consensus_image.shape)
    #print(consensus_image)
    print("Unique values of consensus image:", np.unique(consensus_image))

    return consensus_image

consensus_image = create_consensus_image(binary_images)


#%%
print("Converting consensus to labels")
def convert_to_labels(consensus_image, threshold=0.5):
    # Convert the consensus image to a binary image using a threshold
    binary_image = (consensus_image >= threshold).astype(np.uint8)
    binary_image = morphology.binary_erosion(binary_image)
    
    # Apply label assignment to the binary image
    labels = measure.label(binary_image, connectivity=1, background=0)
    return labels

labels = convert_to_labels(consensus_image, threshold = 0.5)

print("Shape of image array:", consensus_image.shape)
#%%

#find number of labels 
max_value = np.max(labels)
uq_index2 = np.unique(labels)
n_labels2 = len(uq_index2)
print("Total labels: ", max_value)
#print(uq_index2)
print("Total unique label values:", n_labels2)

for l in uq_index2:
    print(l,np.sum(labels == l))

#%%
# out_path = './consensus_image'
# imgname=imgname_readin.replace(".tiff","_consensus_image_mask.tiff")
# outpath_file_path = join(out_path, consensus_image)
# imwrite(outpath_file_path, labels)

#%%
final_value = 0

for i in unique_values:
    error_value = abs(i - n_labels2)
    final_value += error_value

print("Total error value:", final_value)
# %%
