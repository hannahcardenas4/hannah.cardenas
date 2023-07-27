#%%
from matplotlib.pyplot import imsave
import numpy as np
from tifffile import imread, imwrite
from os.path import join
import os
from skimage import measure
#%%

in_path = './binary_images'
imgname_readin = [i for i in os.listdir(in_path) if (('.tif' in i) and ('20230410_pos003_t00' in i))]

binary_image1 = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2_binary_image_m1.tiff'
binary_image2 = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2_binary_image_m2.tiff'
binary_image3 = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2_binary_image_m3.tiff'
binary_image4 = '20230410_pos003_t00_CellPose_mynuclei_decon_scratch_v2_binary_image_m4.tiff'

image_array1 = imread(join(in_path,binary_image1))
image_array2 = imread(join(in_path,binary_image2))
image_array3 = imread(join(in_path,binary_image3))
image_array4 = imread(join(in_path,binary_image4))

binary_images = [image_array1, image_array2, image_array3, image_array4]
#%%
def create_consensus_image(binary_images):
    # Make sure all input images have the same shape
    consensus_image = np.median(binary_images, axis=0)
    print(consensus_image.shape)
    print(consensus_image)
    print(np.unique(consensus_image))

    return consensus_image

consensus_image = create_consensus_image(binary_images)
#binary_image = consensus_image 

# Iterate over each dimension of the image array
#for i in range(consensus_image.shape[0]):
 #   for j in range(consensus_image.shape[1]):
  #      for k in range(consensus_image.shape[2]):
            # Check if the value is greater than or equal to 1
   #         if consensus_image[i, j, k] > 0.5:
                # Set the corresponding value in the binary image array to 1
    #            binary_image[i, j, k] = 1
     #       else:
                # Set the corresponding value in the binary image array to 0
      #          binary_image[i, j, k] = 0

#print(binary_image)
#print(np.unique(binary_image))
#print(binary_image.shape)    
#%%
out_path = './binary_images'
imgname=binary_image1.replace("_binary_image_m1.tiff","_consensus_image.tiff")
outpath_file_path = join(out_path, imgname)
imwrite(outpath_file_path, consensus_image)

# %%