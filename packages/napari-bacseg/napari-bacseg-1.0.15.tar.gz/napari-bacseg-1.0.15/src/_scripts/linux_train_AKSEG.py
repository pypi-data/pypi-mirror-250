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
import pathlib
import cv2
import traceback

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





def process_files(files, omni, device, gpu, recalculate=False):

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
    
    # uncomputed_flows = [path for path in flow_paths if os.path.exists(path.replace(".tif","_flows.tif"))==False]
    #
    # if len(uncomputed_flows)==0 and len(flow_paths) > 0:
    #
    #     for flow_path in flow_paths:
    #         flows.append(tifffile.imread(flow_path.replace(".tif","_flows.tif")))
    #
    # else:
    #
    #     if os.path.exists(mask_paths[0]):


    # if omni==False:
    #
    #     from cellpose import dynamics
    #
    #     flows = dynamics.labels_to_flows(
    #         masks,
    #         use_gpu=gpu,
    #         device=device,
    #         redo_flows=False)
    # else:
    #
    #     from omnipose.core import labels_to_flows, masks_to_flows
    #
    #     flows = labels_to_flows(
    #         masks,
    #         use_gpu=gpu,
    #         device=device,
    #         redo_flows=False,
    #         omni=True)

    files = {"images":images,
            "image_paths":image_paths,
            "masks":masks,
            "mask_paths":mask_paths,
            # "flows":flows,
            # "flow_paths":flow_paths,
             }
    
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


def import_coco_json(json_path):

    try:
        json_path = os.path.splitext(json_path)[0] + ".txt"

        with open(json_path) as f:
            dat = json.load(f)

        h = dat["images"][0]["height"]
        w = dat["images"][0]["width"]

        mask = np.zeros((h, w), dtype=np.uint16)
        nmask = np.zeros((h, w), dtype=np.uint16)
        labels = np.zeros((h, w), dtype=np.uint16)

        categories = {}

        for i, cat in enumerate(dat["categories"]):
            cat_id = cat["id"]
            cat_name = cat["name"]

            categories[cat_id] = cat_name

        annotations = dat["annotations"]

        for i in range(len(annotations)):

            annotation = annotations[i]

            if "segmentation" in annotation.keys():
                annot = annotation["segmentation"][0]
                category_id = annotation["category_id"]

                cnt = np.array(annot).reshape(-1, 1, 2).astype(np.int32)

                cv2.drawContours(mask, [cnt], contourIdx=-1, color=i + 1, thickness=-1)
                cv2.drawContours(labels, [cnt], contourIdx=-1, color=category_id, thickness=-1, )

            if "nucleoid_segmentation" in annotation.keys():
                nucleoid_annot = annotation["nucleoid_segmentation"][0]

                cnt = (np.array(nucleoid_annot).reshape(-1, 1, 2).astype(np.int32))

                cv2.drawContours(nmask, [cnt], contourIdx=-1, color=i + 1, thickness=-1)

    except:
        print(traceback.format_exc())

    return mask, nmask, labels


def cache_data(dat):
    
    data = None
    
    try:
    
        image_path = dat["image_save_path"].unique()[0]
        mask_path = dat["mask_save_path"].unique()[0]
        json_path = dat["json_save_path"].unique()[0]
        channel = dat["channel"].unique()[0].lower()
        
        
        
        load_folder = os.path.abspath(image_path).split("/")[-3]
        flow_path = str(image_path).replace(load_folder,"/flows/")
        flow_dir = os.path.dirname(flow_path)
        
        if os.path.exists(image_path) == True and os.path.exists(json_path) == True:
            
            image = tifffile.imread(image_path)
            
            # if channel == "phaseaise_not(image)

            mask, nmask, labels = import_coco_json(json_path)

            annotations = len(np.unique(mask))
        
            if os.path.exists(flow_dir)==False:
                os.makedirs(flow_dir)
                
            data = dict(image=image,
                        image_path=str(image_path),
                        mask=mask,
                        mask_path=str(mask_path),
                        flow_path=str(flow_path))
                
    except:
        data = None
        print(traceback.format_exc())
        pass
        
    return data



def update_akseg_paths(path, AKSEG_DIRECTORY):
    
    try:
    
        path = pathlib.Path(path.replace("\\","/"))
        AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)
        
        parts = (*AKSEG_DIRECTORY.parts, "Images", *path.parts[-4:])
        path = pathlib.Path('').joinpath(*parts)

    except:
        path = None

    return path


def generate_json_path(dat, AKSEG_DIRECTORY):

    AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)
    segmentation_file = dat["segmentation_file"]
    path = pathlib.Path(dat["mask_save_path"])
    user_initial = path.parts[-4]
    folder = path.parts[-2]

    segmentation_file = pathlib.Path(segmentation_file).with_suffix('.txt')

    parts = (*AKSEG_DIRECTORY.parts, "Images", user_initial, "json", folder, segmentation_file)
    path = pathlib.Path('').joinpath(*parts)

    return path


def get_nile_red_data(akseg_metadata):

    user_initials = akseg_metadata.user_initial.dropna().unique().tolist()

    nile_red_meta = []

    for user in user_initials:
        if user == "PT":
            meta = akseg_metadata[(akseg_metadata["user_initial"] == user) & (akseg_metadata["channel"].isin(["532", "Nile Red", "WGA-488", "FM4-64"])) & (
                akseg_metadata["content"].isin(["E.Coli MG1655", "E.Coli"])) & (akseg_metadata["user_meta2"].isin(["short exposure", np.nan])) & (
                                      akseg_metadata["user_meta3"].isin(["focused", np.nan])) & (akseg_metadata["segmentation_curated"] == True)]

            nile_red_meta.append(meta)

        if user == "AZ":
            meta = akseg_metadata[(akseg_metadata["user_initial"] == user) & (akseg_metadata["channel"].isin(["532"])) & (akseg_metadata["content"].isin(['E.Coli MG1655', 'E.Coli Clinical'])) & (
                akseg_metadata["user_meta1"].isin(['2022 DL Paper'])) & (akseg_metadata["segmentation_curated"] == True)]

            nile_red_meta.append(meta)

        if user == "CF":
            meta = akseg_metadata[(akseg_metadata["user_initial"] == user) & (akseg_metadata["channel"].isin(["Nile Red"])) & (akseg_metadata["segmentation_curated"] == True)]

            nile_red_meta.append(meta)

    akseg_metadata = pd.concat(nile_red_meta)

    return akseg_metadata



AKSEG_DIRECTORY = r"/home/turnerp/.cache/gvfs/smb-share:server=physics.ox.ac.uk,share=dfs/DAQ/CondensedMatterGroups/AKGroup/Piers/AKSEG"
# # AKSEG_DIRECTORY = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"
#
paths = glob(AKSEG_DIRECTORY + "*/Images/PT/*.txt")

akseg_metadata = []
for path in paths:
    try:
        meta = pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
                                                        'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)
        akseg_metadata.append(meta)
    except:
        pass

# akseg_metadata = get_nile_red_data(pd.concat(akseg_metadata).reset_index(drop=True))



# akseg_metadata = [pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
#                                                 'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False) for path in akseg_metadata]
#
akseg_metadata = pd.concat(akseg_metadata).reset_index(drop=True)

akseg_metadata = akseg_metadata[
    (akseg_metadata["user_initial"] == "PT") &
    (akseg_metadata["segmentation_curated"] == True) &
    (akseg_metadata["user_meta1"] == "TrillianSegDev") &
    (akseg_metadata["channel"] == "Phase Contrast")
    ]


akseg_metadata["image_save_path"] = akseg_metadata["image_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
akseg_metadata["mask_save_path"] = akseg_metadata["mask_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
akseg_metadata["label_save_path"] = akseg_metadata["label_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))

akseg_metadata["json_save_path"] = akseg_metadata.apply(lambda dat: generate_json_path(dat, AKSEG_DIRECTORY), axis=1)


# akseg_metadata = akseg_metadata.iloc[:5]

akseg_groups = akseg_metadata.groupby(["user_initial","microscope","channel"])



model_type = "bact_phase_omni"
diam_mean = 15
epochs = 1000
batch_size = 10
augmentation_repeats = 3
omni = True


if omni == False:
    from cellpose import models
    device, gpu = models.assign_device((True), True)
else:
    from cellpose_omni import models
    device, gpu = models.assign_device((True), True)

if __name__=='__main__':

    for i in range(1):

        try:

            torch.cuda.empty_cache()

            data = akseg_groups.get_group(list(akseg_groups.groups)[i])
            # data = akseg_metadata

            source = str(data["channel"].unique()[0])
            user_initial = data["user_initial"].unique()[0]
            file_name = data["file_name"]
            microscope = data["microscope"].unique()[0]
            modality = data["modality"].unique()[0]
            content = data["content"].unique()[0]

            model_name = user_initial + "-" + str(content) +"-" + str(microscope) +"-" + str(modality) + "-" + str(source)

            model_save_path = os.path.abspath(AKSEG_DIRECTORY + "/models/" + user_initial + "/" + model_name + "/")
            model_save_path = model_save_path.replace(" ","")

            meta_file_name = user_initial + "_file_metadata.txt"
            akseg_meta_path = os.path.join(AKSEG_DIRECTORY,"Images",user_initial,meta_file_name)

            if os.path.isdir(model_save_path)==False:
                os.makedirs(model_save_path)

            cellpose_save_path = os.path.abspath("models\\" + user_initial + "\\" + str(source) + "/")

            # list comprehension to split data by segmentation file
            training_files = [data[data["segmentation_file"]==file] for file in data["segmentation_file"].unique()]


            # check json file path is not None in training files
            training_files = [dat for dat in training_files if dat["json_save_path"] is not None]

            # train, val = train_test_split(training_files, test_size=0.1, random_state=42)

            # num_train,num_val = len(train), len(val)

            if len(training_files) > 0:

                print(f"user: {user_initial} , microscope: {microscope}, source: {source} , training_images: {len(training_files)}")

                print("loading data...")

                with Pool(30) as pool:
                    train = pool.map(cache_data, training_files)
                    # val = pool.map(cache_data, val)

                train = process_files(train, omni, device, gpu, recalculate=False)
                # val = process_files(val, device, gpu, recalculate=False)
#
                # print("generating training augmentations...")

                # train = apply_training_augmentations(train,True,augmentation_repeats)

                if omni == False:

                    from cellpose import utils, models, io, dynamics

                    model = models.CellposeModel(
                        diam_mean = diam_mean,
                        model_type=model_type,
                        gpu=gpu,
                        device = device,
                        net_avg = False,
                    )

                    print(f"training model: {model_name}, num_train: {len(training_files)}")

                    pretrained_model = model.train(
                        train["images"],
                        train["masks"],
                        # test_data=val["images"],
                        # test_labels=val["masks"],
                        channels=[0, 0],
                        save_path=cellpose_save_path,
                        batch_size=batch_size,
                        n_epochs=epochs,
                        save_every=1,
                        save_each=False,

                    )

                else:
                    from cellpose_omni import models

                    model = models.CellposeModel(
                        # diam_mean=0,
                        model_type=model_type,
                        gpu=gpu,
                        device=device,
                        net_avg=False,
                        omni=True

                    )

                    pretrained_model = model.train(
                        train["images"],
                        train["masks"],
                        # test_data=val["images"],
                        # test_labels=val["masks"],
                        channels=[0, 0],
                        SGD=False,
                        save_path=cellpose_save_path,
                        batch_size=16,
                        n_epochs=epochs,
                        learning_rate=0.1,
                    )

                model_save_path = model_save_path.replace(" ","")

                print(f"training complete, saving model to: {model_save_path}")

                if os.path.isdir(model_save_path)==False:
                    os.makedirs(model_save_path)

                model_path = os.path.abspath(pretrained_model)

                if omni == False:
                    model_name = "cellpose_" + model_path.split("\\")[-1]
                else:
                    model_name = "omnipose_" + model_path.split("\\")[-1]

                shutil.copyfile(model_path, model_save_path + "\\" + model_name)

        except Exception:
            import traceback
            print(traceback.format_exc())
            pass








                
            
            
        
        
        