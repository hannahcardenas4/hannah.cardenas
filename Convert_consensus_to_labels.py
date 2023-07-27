#%% 
import numpy as np
from tifffile import imread, imwrite
from os.path import join
import os
from skimage import measure, morphology


in_path = './binary_images'
imgname_readin = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2_consensus_image.tiff'
consensus_image = imread(join(in_path,imgname_readin))

#print(consensus_image)

def convert_to_labels(consensus_image, threshold=0.5):
    # Convert the consensus image to a binary image using a threshold
    binary_image = (consensus_image >= threshold).astype(np.uint8)
    binary_image = morphology.binary_erosion(binary_image)
    
    # Apply label assignment to the binary image
    labels = measure.label(binary_image, connectivity=1, background=0)
    return labels

labels = convert_to_labels(consensus_image, threshold = 0.5)
#print(labels)


print("Shape of image array:", consensus_image.shape)
#%%

#find number of labels 
max_value = np.max(labels)
uq_index = np.unique(labels)
n_labels = len(uq_index)
print("Total labels: ", max_value)
print(uq_index)
print(n_labels)

for l in uq_index:
    print(l,np.sum(labels == l))

#%%
out_path = './consensus_image'
imgname=imgname_readin.replace("_consensus_image.tiff","_consensus_image_mask.tiff")
outpath_file_path = join(out_path, imgname)
imwrite(outpath_file_path, labels)

# %%
