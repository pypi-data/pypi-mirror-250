# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:54:19 2022

@author: turnerp
"""

import pandas as pd
import numpy as np
from glob2 import glob
import pickle
import os
import tifffile
from sklearn.model_selection import train_test_split
from cellpose import models,metrics
from cellpose import utils, models, io, dynamics
import matplotlib.pyplot as plt
from ast import literal_eval
from imgaug import augmenters as iaa
from datetime import datetime
import shutil
import torch
import tqdm
from multiprocessing import Pool
from itertools import repeat
import math
import json

def get_akseg_path(data, akseg_dir,akseg_file="images"):
    
    user_initial = data.user_initial
    folder = data.folder
    file_name = data.file_name
    
    path = os.path.join(akseg_dir, "Images", user_initial, akseg_file, folder, file_name)
    
    return path



def load_files(file_list, device=None, use_gpu=False, recalculate=False):

    images = []
    image_paths = []
    
    masks = []
    mask_paths = []
    
    flows = []
    flow_paths = []
    
    files = []
    
    for i in range(len(file_list)):
        
        try:
            load_path = file_list[i]

            file_name = os.path.basename(load_path)
            
            load_folder = os.path.abspath(load_path).split("\\")[-3]
            
            image_path = load_path.replace(load_folder,"\\images\\")
            mask_path = load_path.replace(load_folder,"\\masks\\")
            flow_path = load_path.replace(load_folder,"\\flows\\")
            flow_dir = flow_path.replace(file_name,"")
            
            image_path = os.path.abspath(image_path)
            mask_path = os.path.abspath(mask_path)
            flow_path = os.path.abspath(flow_path)
            flow_save_path = flow_path.replace(".tif","_flows.tif")
            
            image = tifffile.imread(image_path)
        
            if os.path.exists(mask_path):
                mask = tifffile.imread(mask_path)
                
                annotations = len(np.unique(mask))
                
            else:
                mask = None
            
            if os.path.exists(flow_dir)==False:
                os.makedirs(flow_dir)
                
            if recalculate==True and os.path.isfile(flow_save_path):
                os.remove(flow_save_path)
                
            if annotations > 1:
                
                images.append(image)
                image_paths.append(image_path)
                
                masks.append(mask)
                mask_paths.append(image_path)
                
                flow_paths.append(flow_path)
                

        except Exception:
            pass
        

    uncomputed_flows = [path for path in flow_paths if os.path.exists(path.replace(".tif","_flows.tif"))==False]
    
    if len(uncomputed_flows)==0 and len(flow_paths) > 0:
        
        for flow_path in flow_paths:
            flows.append(tifffile.imread(flow_path.replace(".tif","_flows.tif")))
            
    else:
        
        if os.path.exists(mask_path):
            
            flows = dynamics.labels_to_flows(masks, files=flow_paths,
                                            use_gpu=False, device=None, redo_flows=False)
        

    files = {"images":images,
            "image_paths":image_paths,
            "masks":masks,
            "mask_paths":mask_paths,
            "flows":flows,
            "flow_paths":flow_paths}
    
    return files





def process_files(files, device, gpu, recalculate=False):

    images = []
    image_paths = []
    
    masks = []
    mask_paths = []
    
    flows = []
    flow_paths = []
    
    for file in files:

        images.append(file["image"])
        image_paths.append(file["image_path"])
        masks.append(file["mask"])
        mask_paths.append(file["mask_path"])
        flow_paths.append(file["flow_path"])
    
    uncomputed_flows = [path for path in flow_paths if os.path.exists(path.replace(".tif","_flows.tif"))==False]
    
    if len(uncomputed_flows)==0 and len(flow_paths) > 0:
        
        for flow_path in flow_paths:
            flows.append(tifffile.imread(flow_path.replace(".tif","_flows.tif")))
            
    else:
        
        if os.path.exists(mask_paths[0]):
            
            flows = dynamics.labels_to_flows(masks, files=flow_paths,
                                            use_gpu=False, device=None, redo_flows=False)
        

    files = {"images":images,
            "image_paths":image_paths,
            "masks":masks,
            "mask_paths":mask_paths,
            "flows":flows,
            "flow_paths":flow_paths}
    
    return files



def apply_training_augmentations(dataset,augmentation,iterations):
    
    images = dataset['images']
    image_paths = dataset['image_paths']
    masks = dataset['masks']
    mask_paths = dataset['mask_paths']
    flows = dataset['flows']
    flow_paths = dataset['flow_paths']
    
    images_extended = images.copy()
    image_paths_extended = image_paths.copy()
    masks_extended = masks.copy()
    mask_paths_extended = mask_paths.copy()
    flows_extended = flows.copy()
    flow_paths_extended = flow_paths.copy()
    
    for i in range(iterations):
        
        augmented_images = []
        
        for j in range(len(images)):
                       
            image = images[j]
            
            if augmentation==True:
                
                image_aug = imgaug_augment(image)
                augmented_images.append(image_aug)
 
            else:
                augmented_images.append(image)

        images_extended = images_extended + augmented_images
        image_paths_extended = image_paths_extended + image_paths
        masks_extended = masks_extended + masks
        mask_paths_extended = mask_paths_extended + mask_paths
        flows_extended = flows_extended + flows
        flow_paths_extended = flow_paths_extended + flow_paths
        
             
    files = {"images":images_extended,
            "image_paths":image_paths_extended,
            "masks":masks_extended,
            "mask_paths":mask_paths_extended,
            "flows":flows_extended,
            "flow_paths":flow_paths_extended}
    
    return files

def imgaug_augment(image):
    
    img = image.copy()
    
    seq = iaa.Sequential(
        [
        iaa.Sometimes(0.5, iaa.Multiply((0.3, 3))),
        iaa.Sometimes(0.5, iaa.MultiplyElementwise((0.9, 1.1))),
        iaa.Sometimes(0.5, iaa.GammaContrast((0.5, 1.5))),
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 1))),
        ],
        random_order=False)


    rgb = np.zeros((img.shape[0],img.shape[1],3),dtype=np.uint16)
    rgb[:,:,0] = img

    seq_det = seq.to_deterministic()
    rgb = seq_det.augment_images([rgb])

    img = rgb[0][:,:,0].astype(np.uint16)
    
    return img


def cache_data(load_path):
    
    if len(load_path) > 0:
    
        file_name = os.path.basename(load_path)
        
        load_folder = os.path.abspath(load_path).split("\\")[-3]
        
        image_path = load_path.replace(load_folder,"\\images\\")
        mask_path = load_path.replace(load_folder,"\\masks\\")
        flow_path = load_path.replace(load_folder,"\\flows\\")
        flow_dir = flow_path.replace(file_name,"")
        
        image_path = os.path.abspath(image_path)
        mask_path = os.path.abspath(mask_path)
        flow_path = os.path.abspath(flow_path)
        flow_save_path = flow_path.replace(".tif","_flows.tif")
        
        image = tifffile.imread(image_path)
    
        if os.path.exists(mask_path):
            mask = tifffile.imread(mask_path)
            
            annotations = len(np.unique(mask))
            
        else:
            annotations = 0
            mask = None
        
        if os.path.exists(flow_dir)==False:
            os.makedirs(flow_dir)
            
        data = dict(image=image,
                    image_path=image_path,
                    mask=mask,
                    mask_path=mask_path,
                    flow_path=flow_path)
        
        
    else:
        
        data = None
        
    return data









# akseg_dir = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"
# akseg_metadata = glob(akseg_dir + "\Images" + "*\*\*.txt")
#
# akseg_metadata = [pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
#                                                 'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False) for path in akseg_metadata]
#
#
# akseg_metadata = pd.concat(akseg_metadata).reset_index(drop=True)
#
#
# akseg_metadata["mask_save_path"] = akseg_metadata.apply(lambda x: get_akseg_path(x, akseg_dir,"masks"), axis=1)
# akseg_metadata["image_save_path"] = akseg_metadata.apply(lambda x: get_akseg_path(x, akseg_dir,"images"), axis=1)
#
# # akseg_metadata.drop(akseg_metadata.index[akseg_metadata["user_initial"]is not "CF"], inplace=True)
#
# akseg_metadata = akseg_metadata[(akseg_metadata["user_initial"]=="AF") &
#                                 (akseg_metadata["microscope"]=="ScanR")]
#
# akseg_groups = akseg_metadata.groupby(["user_initial","microscope","channel"])
#
#
# device, gpu = models.assign_device((True), True)

#
#
# if __name__=='__main__':
#
#     for i in range(len(akseg_groups)):
#
#         try:
#
#             torch.cuda.empty_cache()
#
#             data = akseg_groups.get_group(list(akseg_groups.groups)[i])
#
#             training_data = data[data["segmentation_curated"]==True]
#             test_data = data[data["segmentation_curated"]==False]
#
#             source = str(data["channel"].unique()[0])
#             user_initial = data["user_initial"].unique()[0]
#             file_name = data["file_name"]
#             microscope = data["microscope"].unique()[0]
#             modality = data["modality"].unique()[0]
#             content = data["content"].unique()[0]
#
#             model_name = user_initial + "-" + str(content) +"-" + str(microscope) +"-" + str(modality) + "-" + str(source)
#             model_save_path = os.path.abspath(akseg_dir + "\\models\\" + user_initial + "\\" + model_name + "\\")
#             model_save_path = model_save_path.replace(" ","")
#
#             meta_file_name = user_initial + "_file_metadata.txt"
#             akseg_meta_path = os.path.join(akseg_dir,"Images",user_initial,meta_file_name)
#
#             if os.path.isdir(model_save_path)==False:
#                 os.makedirs(model_save_path)
#
#             model_type = "nuclei"
#             diam_mean = 15
#             epochs = 100
#             batch_size = 10
#             augmentation_repeats = 3
#
#             cellpose_save_path = os.path.abspath("models\\" + user_initial + "\\" + str(source) + "/")
#
#             training_file_paths = training_data.mask_save_path.tolist()
#             test = test_data.mask_save_path.tolist()
#
#             train, val = train_test_split(training_file_paths, test_size=0.2, random_state=42)
#
#             if len(train) > 0:
#
#                 print(f"user: {user_initial} , microscope: {microscope}, source: {source} , training_images: {len(training_data)} , test_images: {len(test_data)}")
#
#                 with Pool(30) as pool:
#                     train = pool.map(cache_data, train)
#                     val = pool.map(cache_data, val)
#
#                 num_train,num_val = len(train)/augmentation_repeats, len(val)/augmentation_repeats
#
#                 train = process_files(train, device, gpu, recalculate=False)
#                 val = process_files(val, device, gpu, recalculate=False)
#
#
#                 train = apply_training_augmentations(train,True,augmentation_repeats)
#
#                 model = models.CellposeModel(diam_mean = diam_mean,
#                                               model_type=model_type,
#                                               gpu=gpu,
#                                               device = device,
#                                               torch = device,
#                                               net_avg = False,
#                                               omni = False,
#                                             )
#
#
#                 pretrained_model = model.train(train["images"],train["flows"],
#                             test_data=val["images"], test_labels=val["flows"],
#                             channels = [0,0],
#                             save_path =  cellpose_save_path,
#                             batch_size = batch_size,
#                             n_epochs = epochs,
#                             save_every=1,
#                             save_each=False)
#
#
#                 model_save_path = model_save_path.replace(" ","")
#
#                 if os.path.isdir(model_save_path)==False:
#                     os.makedirs(model_save_path)
#
#                 model_path = os.path.abspath(pretrained_model)
#                 model_name = model_path.split("\\")[-1]
#                 shutil.copyfile(model_path, model_save_path + "\\" + model_name)
#
#         except Exception:
#
#             pass
#
#
#
#
                
                

                
                
            
            
        
        
        