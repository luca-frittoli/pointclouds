from multiprocessing import Pool
import math
import os, sys, argparse
import inspect
import json
import numpy as np

import util
import util_3d
import export_train_mesh_for_evaluation as angela
import obj_crawler as alberto

#scan_path = "./scans/scene0001_00"
all_paths = os.listdir("./scans")
all_scenes = [os.path.join("./scans", path) for path in all_paths]
ncore = 40

def process_scene(scan_path):
    output_file = os.path.join(scan_path, "o")
    label_map_file = "scannetv2-labels.combined.tsv"

    json_name = os.path.join(scan_path, "ids_to_labels.json")

    scan_name = os.path.split(scan_path)[-1]
    mesh_file = os.path.join(scan_path, scan_name + '_vh_clean_2.ply')
    agg_file = os.path.join(scan_path, scan_name + '.aggregation.json')
    seg_file = os.path.join(scan_path, scan_name + '_vh_clean_2.0.010000.segs.json')
    angela.export(mesh_file, agg_file, seg_file, label_map_file, "instance", output_file, json_name)

    # read json with object classes
    label_file = open(json_name, 'r')
    labels_dict = json.load(label_file)

    our_labels = ['3', '4', '5', '6', '7', '10', '15', '25']
    id_dict = {}
    for idx in labels_dict.keys():
        if all(item in our_labels for item in [labels_dict[idx]]):
            id_dict[idx] = labels_dict[idx]
            

    #scene_id = os.path.split(scan_path)[-1]
    mask_path = "./pred_mask/o_{}.txt"
    output_folder = "./objects/" 
    #output_name = output_folder + scan_name + "_{}.obj"
    for idx in id_dict.keys():
        #print(idx)
        current_folder = os.path.join(output_folder, id_dict[idx])
        if not os.path.isdir(current_folder):
            os.mkdir(current_folder)
        current_mask = mask_path.format(int(idx))
        current_output = os.path.join(current_folder, scan_name + "_{}.obj".format(int(idx)))
        alberto.crawl_object(mesh_file, current_mask, current_output)

if __name__ == '__main__':
    pool = Pool(processes=ncore)
    pool.map(process_scene, all_scenes)


