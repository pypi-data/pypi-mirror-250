import traceback

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
import pathlib
import time
import datefinder
import re
import cv2


def generate_json_annotation_string(mask, label):

    mask_ids = np.unique(mask)

    annotations = []

    for j in range(len(mask_ids)):
        if j != 0:
            try:
                cnt_mask = mask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j}

                annotations.append(annotation)

            except:
                pass

    return annotations



def export_coco_json(image_name, image, mask, nmask, label, file_path):
    
    file_path = os.path.splitext(file_path)[0] + ".txt"

    info = {"description": "COCO 2017 Dataset", "url": "http://cocodataset.org", "version": "1.0", "year": datetime.now().year, "contributor": "COCO Consortium", "date_created": datetime.now().strftime("%d/%m/%y"), }

    categories = [{"supercategory": "cell", "id": 1, "name": "single"}, {"supercategory": "cell", "id": 2, "name": "dividing"}, {"supercategory": "cell", "id": 3, "name": "divided"},
        {"supercategory": "cell", "id": 4, "name": "vertical"}, {"supercategory": "cell", "id": 5, "name": "broken"}, {"supercategory": "cell", "id": 6, "name": "edge"}, ]

    licenses = [{"url": "https://creativecommons.org/licenses/by-nc-nd/4.0/", "id": 1, "name": "Attribution-NonCommercial-NoDerivatives 4.0 International", }]

    height, width = image.shape[-2], image.shape[-1]

    images = [{"license": 1, "file_name": image_name, "coco_url": "", "height": height, "width": width, "date_captured": "", "flickr_url": "", "id": 0, }]

    mask_ids = np.unique(mask)

    annotations = []

    for j in range(len(mask_ids)):
        if j != 0:
            try:
                cnt_mask = mask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    nmask_ids = np.unique(nmask)

    for j in range(len(nmask_ids)):
        if j != 0:
            try:
                cnt_mask = nmask.copy()

                cnt_mask[cnt_mask != j] = 0

                contours, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE, )
                cnt = contours[0]

                # cnt coco bounding box
                x, y, w, h = cv2.boundingRect(cnt)
                y1, y2, x1, x2 = y, (y + h), x, (x + w)
                coco_BBOX = [x1, y1, h, w]

                # cnt area
                area = cv2.contourArea(cnt)

                segmentation = cnt.reshape(-1, 1).flatten()

                cnt_labels = np.unique(label[cnt_mask != 0])

                if len(cnt_labels) == 0:
                    cnt_label = 1

                else:
                    cnt_label = int(cnt_labels[0])

                annotation = {"nucleoid_segmentation": [segmentation.tolist()], "area": area, "iscrowd": 0, "image_id": 0, "bbox": coco_BBOX, "category_id": cnt_label, "id": j, }

                annotations.append(annotation)

            except:
                pass

    annotation = {"info": info, "licenses": licenses, "images": images, "annotations": annotations, "categories": categories, }

    with open(file_path, "w") as f:
        json.dump(annotation, f)

    return annotation



def autoClassify(mask):

    mask_ids = np.unique(mask)

    label = np.zeros(mask.shape, dtype=np.uint16)

    for mask_id in mask_ids:
        if mask_id != 0:
            cnt_mask = np.zeros(label.shape, dtype=np.uint8)
            cnt_mask[mask == mask_id] = 255

            cnt, _ = cv2.findContours(cnt_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            x, y, w, h = cv2.boundingRect(cnt[0])
            y1, y2, x1, x2 = y, (y + h), x, (x + w)

            # appends contour to list if the bounding coordinates are along the edge of the image
            if y1 > 0 and y2 < cnt_mask.shape[0] and x1 > 0 and x2 < cnt_mask.shape[1]:
                label[mask == mask_id] = 1

            else:
                label[mask == mask_id] = 6

    return label

def update_metadata_element(path, key, value):
    try:

        tif = tifffile.TiffFile(path, mode='r+b')

        metadata = tif.pages[0].tags["ImageDescription"].value
        metadata = json.loads(metadata)

        metadata[key] = value
        metadata = json.dumps(metadata)

        tif.pages[0].tags["ImageDescription"].overwrite(metadata)

    except Exception:
        print(traceback.format_exc())
        pass


def extract_list(data, mode="file"):

    data = data.strip("[]").replace("'", "").split(", ")

    return data


def update_akseg_paths(path, AKSEG_DIRECTORY):
    try:
        path = pathlib.Path(path.replace("\\", "/"))
        AKSEG_DIRECTORY = pathlib.Path(AKSEG_DIRECTORY)

        parts = (*AKSEG_DIRECTORY.parts, "Images", *path.parts[-4:])
        path = pathlib.Path('').joinpath(*parts)

    except:
        path = None

    return str(path)

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

def read_akseg_metadata(AKSEG_DIRECTORY, USER_INITIAL):

    path = glob(AKSEG_DIRECTORY + f"/Images/{USER_INITIAL}/*.txt")[0]

    akseg_metadata = pd.read_csv(path, converters={'channel_list': lambda x: x.strip("[]").split(", "),
                                                        'file_list': lambda x: x.strip("[]").split(", ")}, low_memory=False)

    filtered_metadata = akseg_metadata.copy()

    akseg_metadata["image_save_path"] = akseg_metadata["image_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
    akseg_metadata["mask_save_path"] = akseg_metadata["mask_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))
    akseg_metadata["label_save_path"] = akseg_metadata["label_save_path"].apply(lambda path: update_akseg_paths(path, AKSEG_DIRECTORY))

    akseg_metadata["json_save_path"] = akseg_metadata.apply(lambda dat: generate_json_path(dat, AKSEG_DIRECTORY), axis=1)

    akseg_metadata = akseg_metadata.drop_duplicates(subset=['akseg_hash'], keep="last")

    return akseg_metadata, path


def filter_akseg_metadata(akseg_metadata, filter_dict={}, limit="None"):

    filtered_metadata = akseg_metadata.copy()
    
    if filter_dict != {}:
    
        for key, value in filter_dict.items():
            if key in filtered_metadata.columns:
                filtered_metadata = filtered_metadata[filtered_metadata[key]==value]
    
    image_list = filtered_metadata.groupby(["segmentation_file", "folder"]).first().reset_index().to_dict('records')
    
    if type(limit) == int:
        
        image_list = image_list[:limit]
        
    print(f"Found {len(image_list)} uncurated images to process")
        
    return image_list





def split_dataframe(df, chunk_size = 10000): 
    
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

def read_tif_meta(path):
    
    with tifffile.TiffFile(path) as tif:
        try:
            metadata = tif.pages[0].tags["ImageDescription"].value
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}
            
    return metadata


def read_akseg_image(dat):

    try:
        
        path = dat["image_save_path"]
        
        with tifffile.TiffFile(path) as tif:
        
            tif_metadata = tif.pages[0].tags["ImageDescription"].value
            tif_metadata = json.loads(tif_metadata)
            image = tifffile.imread(path)
    
    except:
        tif_metadata = None
        image = None

    return image, tif_metadata, dat



def load_files(image_list):


    with Pool(2) as p:
        
        results = list(tqdm.tqdm(p.imap(read_akseg_image,image_list), total=len(image_list)))
        p.close()
        p.join()

        results = [dat for dat in results if dat[0] is not None]
        
        images, tif_metadata, db_metadata = zip(*results)
        
    return list(images), list(tif_metadata), list(db_metadata)




def segment_files(images, tif_metadata, db_metadata, gpu = True, omni = False):

    segmented_masks = []
    segmented_images = []
    segmented_tif_metadata = []
    segmented_db_metadata = []

    for image, tif_meta, db_meta in tqdm.tqdm(zip(images, tif_metadata, db_metadata), total=len(images)):

        try:

            if omni:

                mask, _, _ = model.eval([image],
                                        channels=[0,0],
                                        mask_threshold=mask_threshold,
                                        flow_threshold=flow_threshold,
                                        diameter=0,
                                        invert=False,
                                        tile=False,
                                        cluster=False,
                                        net_avg=False,
                                        do_3D=False,
                                        omni=True,
                                        batch_size=10000,
                                        progress=True,
                                        min_size=min_size,
                                        )
            else:

                mask, _, _ = model.eval([image],
                                         diameter=diameter,
                                         channels=[0, 0],
                                         flow_threshold=flow_threshold,
                                         cellprob_threshold=mask_threshold,
                                         min_size=min_size,
                                         batch_size=10000,
                                         progress=True,
                                         )

            segmented_masks.extend(mask)
            segmented_images.append(image)
            segmented_tif_metadata.append(tif_meta)
            segmented_db_metadata.append(db_meta)

        except:
            pass

    return list(segmented_images), list(segmented_tif_metadata), list(segmented_db_metadata), list(segmented_masks)


def upload_files(dat):
    
    try:
    
        img, tif_meta, db_meta, mask = dat
        
        file_name = db_meta["file_name"]
        mask_save_path = db_meta["mask_save_path"]
        json_save_path = str(db_meta["json_save_path"])
        
        label = autoClassify(mask)
        nmask = mask.copy()
        
        num_segmentations = len(np.unique(mask)) - 1
        
        export_coco_json(file_name, img, mask, nmask, label, json_save_path)
        
        if "shape" in tif_meta:
            del tif_meta["shape"]
            
        # tifffile.imwrite(mask_save_path, mask, metadata=tif_meta)
            
        db_meta["segmented"] = True
        db_meta["date_modified"] = str(datetime.now())
        db_meta["num_segmentations"] = num_segmentations

    except:
        db_meta = None
        pass

    return db_meta

def upload_akseg_data(images, tif_metadata, db_metadata, masks):

    upload_data = list(zip(images, tif_metadata, db_metadata, masks))
    
    with Pool() as p:
        
        results = list(tqdm.tqdm(p.imap(upload_files,upload_data), total=len(upload_data)))
        p.close()
        p.join()
        
        uploaded_data = [dat for dat in results if results!=None]
        
    return uploaded_data
    


def extract_list(data, mode="file"):

    data = data.strip("[]").replace("'", "").split(", ")

    return data

def load_cellpose_dependencies():

    import torch
    from cellpose import models
    from cellpose.dynamics import labels_to_flows

    gpu = False

    if torch.cuda.is_available():
        print("Cellpose Using GPU")
        gpu = True
        torch.cuda.empty_cache()

    return gpu, models

def load_omnipose_dependencies():

    import torch
    from cellpose_omni import models
    from omnipose.core import labels_to_flows

    gpu = False

    if torch.cuda.is_available():
        print("Omnipose Using GPU")
        gpu = True
        torch.cuda.empty_cache()

    return gpu, models


def get_cellpose_model(model_name = "", AKSEG_DIRECTORY="", USER_INITIAL="", pretrained_model="", model_library = "cellpose"):
    
    model_list = ["cyto2_omni", "bact_phase_omni", "bact_fluor_omni", "plant_omni", "worm_omni", "worm_bact_omni","worm_high_res_omni", "cyto", "cyto2", "nuclei", ]
    
    if model_name != "":
        
        if "omni"in model_name:
            omni = True
            
            gpu, models = load_omnipose_dependencies()
            model = models.CellposeModel(diam_mean=0, model_type=model_name, gpu=gpu, net_avg=False, )
            
        else:
            omni = False
            
            gpu, models = load_cellpose_dependencies()
            model = models.CellposeModel(diam_mean=15, model_type=model_name, gpu=gpu, net_avg=False, )
    
    else:
        
        assert model_library in ["cellpose", "omnipose"]
    
        model_dir = pathlib.Path('').joinpath(*pathlib.Path(AKSEG_DIRECTORY).parts, 
                                                    "Models", 
                                                    USER_INITIAL, 
                                                    pretrained_model)
    
        cellpose_model_paths = glob(str(model_dir) + "/*")
        
        cellpose_model_paths = [path for path in cellpose_model_paths if model_library in pathlib.Path(path).name]
        
        cellpose_model_names = [pathlib.Path(model_path).name for model_path in cellpose_model_paths]
        
        date_strings = [re.findall(r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}', model_name)[0] for model_name in cellpose_model_names]
        date_strings = [datetime.strptime(date, '%Y_%m_%d_%H_%M_%S') for date in date_strings]
    
        cellpose_models, cellpose_dates = zip(
            *sorted(zip(cellpose_model_paths, date_strings), key=lambda x: x[-1], reverse=True))
    
        model_path = cellpose_models[0]
    
        print(f"Selected model: {pathlib.Path(cellpose_models[0]).name}")
        
        if model_library == "cellpose":
            
            omni = False
            gpu, models = load_cellpose_dependencies()
            model = models.CellposeModel(pretrained_model=model_path, diam_mean=15, model_type=None, gpu=gpu, net_avg=False, )
            
            
        else:
            omni = True
            gpu, models = load_omnipose_dependencies()
            model = models.CellposeModel(pretrained_model=model_path, diam_mean=0, model_type=None, gpu=gpu, net_avg=False, )
        
    return model, omni


def upate_akseg_metadata(akseg_metadata, uploaded_data):
    
    updated_akseg_metadata = akseg_metadata.copy()
    
    for dat in uploaded_data:
        
        segmentation_file = dat["segmentation_file"]
        folder = dat["folder"]

        updated_akseg_metadata.loc[(updated_akseg_metadata['segmentation_file'] == segmentation_file) &
                           (updated_akseg_metadata['folder'] == folder), 'segmented'] = True
        
        updated_akseg_metadata.loc[(updated_akseg_metadata['segmentation_file'] == segmentation_file) &
                           (updated_akseg_metadata['folder'] == folder), 'date_modified'] = str(datetime.now())
        
        updated_akseg_metadata.loc[(updated_akseg_metadata['segmentation_file'] == segmentation_file) &
                           (updated_akseg_metadata['folder'] == folder), 'num_segmentations'] = dat["num_segmentations"]
    

    return updated_akseg_metadata






AKSEG_DIRECTORY = r"/home/turnerp/.cache/gvfs/smb-share:server=physics.ox.ac.uk,share=dfs/DAQ/CondensedMatterGroups/AKGroup/Piers/AKSEG"
# AKSEG_DIRECTORY = r"\\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG"



USER_INITIAL = "PT"
limit = 2000
filter_dict = {"segmented":False,
               "user_meta1":"Trillian Gram Stain DEV",
               "channel":"Phase Contrast",
               }

mask_threshold = 0.9
flow_threshold = 0
min_size = 10
diameter = 15


if __name__=='__main__':
    
    akseg_metadata, metadata_path = read_akseg_metadata(AKSEG_DIRECTORY, USER_INITIAL)
    
    image_list = filter_akseg_metadata(akseg_metadata,filter_dict,limit = limit)
    
    num_images = len(image_list)

    if num_images > 0:

        # model_path = get_cellpose_model(AKSEG_DIRECTORY=AKSEG_DIRECTORY,
        #                                 USER_INITIAL="PT",
        #                                 pretrained_model="PT-E.Coli-Trillian-PhaseContrast-PhaseContrast",
        #                                 model_library="omnipose")

        model, omni = get_cellpose_model("bact_phase_omni")

        print(f"downloading {num_images} images...")

        start_time = time.time()
        images, tif_metadata, db_metadata = load_files(image_list)
        print(f"Completed. Duration: {(time.time() - start_time)/60:.2f} minutes.\n")

        print(f"segmenting {num_images} images...")

        start_time = time.time()
        images, tif_metadata, db_metadata, masks = segment_files(images, tif_metadata, db_metadata, omni=omni)

        print(f"Completed. Duration: {(time.time() - start_time)/60:.2f} minutes.\n")

        # with open('data.pickle', 'wb') as handle:
        #     pickle.dump([images, tif_metadata, db_metadata, masks], handle, protocol=pickle.HIGHEST_PROTOCOL)

        # with open('data.pickle', 'rb') as handle:
        #     images, tif_metadata, db_metadata, masks = pickle.load(handle)

        print(f"uploading {len(masks)} masks...")

        start_time = time.time()
        uploaded_data = upload_akseg_data(images, tif_metadata, db_metadata, masks)
        print(f"Completed. Duration: {(time.time() - start_time)/60:.2f} minutes.\n")


        # with open('uploaded_data.pickle', 'wb') as handle:
        #     pickle.dump([akseg_metadata,uploaded_data], handle, protocol=pickle.HIGHEST_PROTOCOL)

        # with open('uploaded_data.pickle', 'rb') as handle:
        #     akseg_metadata,uploaded_data = pickle.load(handle)

        updated_akseg_metadata = upate_akseg_metadata(akseg_metadata, uploaded_data)
        
        if len(akseg_metadata) == len(updated_akseg_metadata):

            print(f"updating metadata...")

            start_time = time.time()
            updated_akseg_metadata.to_csv(metadata_path, sep=",", index = False)
            print(f"Completed. Duration: {(time.time() - start_time)/60:.2f} minutes.\n")
    
    
    

# with open('uploaded_data.pickle', 'rb') as handle:
#     akseg_metadata,uploaded_data = pickle.load(handle)

# akseg_metadata = upate_akseg_metadata(akseg_metadata, uploaded_data)

# print(f"writing metadata to {metadata_path}...")

# akseg_metadata.to_csv(metadata_path, sep=",", index = False)







# akseg_metadata = split_dataframe(akseg_metadata, 200)


# dat = akseg_metadata[0]

# print(True)

# image_load_paths = dat["image_save_path"].tolist()
# mask_save_paths = [str(path) for path in dat["mask_save_path"].tolist()]

# print("loading images")

# images = [tifffile.imread(path) for path in image_load_paths]
# images_meta = [read_tif_meta(path) for path in image_load_paths]

# print("segmenting_files")

# masks, flows, diams = model.eval(images,
#                                  diameter=diameter,
#                                  channels=[0, 0],
#                                  flow_threshold=flow_threshold,
#                                  cellprob_threshold=mask_threshold,
#                                  min_size=min_size,
#                                  batch_size=200)

# print(len(masks))








# print(mask.shape)



# \\physics\dfs\DAQ\CondensedMatterGroups\AKGroup\Piers\AKSEG\Models\PT\PT-rod-ScanR-Epifluorescence-Trans


