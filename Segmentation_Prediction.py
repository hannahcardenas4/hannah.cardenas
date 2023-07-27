import numpy as np
from tifffile import imread, imwrite
from cellpose import models
import os
from os.path import join
import sys

model_path = './models_for_binary'
model_list = [i for i in os.listdir(model_path)]
#model_name = 'cellpose_residual_on_style_on_concatenation_off_Slices_2023_06_28_Hannah'
#model = models.CellposeModel(pretrained_model=join(model_path,model_list),net_avg=True,gpu=True)
print(model_list)

in_path = './deconvolved_images/exposure_tests'
imglist = [i for i in os.listdir(in_path) if (('.tif' in i) and ('CellPose' not in i))]
print(imglist)

channels = [[0,0]]
model_number = 0
out_path = './masks_for_binary'

for i in model_list:
    print(i)
    model = models.CellposeModel(pretrained_model=join(model_path,i),net_avg=True,gpu=True)
    model_number += 1
    for imgname in imglist:
        print(join(in_path,imgname))
        img = imread(join(in_path,imgname))
        masks, flows, styles = model.eval(img, diameter=40, channels=channels,cellprob_threshold=0.25
                                                ,       flow_threshold=0.8,do_3D=True,anisotropy=2.5)
    
        out_masks = np.array(masks)
        print(out_masks.shape)
        imgname = imgname.replace(".tiff", "_CellPose_mynuclei_decon_scratch_v2_m" + str(model_number) + ".tiff")
        imwrite(join(out_path,imgname),out_masks) 