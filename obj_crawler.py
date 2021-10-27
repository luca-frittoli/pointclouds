import numpy as np
from plyfile import PlyData, PlyElement
import json

def select_faces(faces, scene_vertices, idx_masked_vertices):
    squeeze_list = lambda lst: [el[0] for el in lst]
    faces = squeeze_list(faces)

    faces_da_tenere = []
    # faces = [ [1,2,3], [4,2,1]]
    # vertici_ok = np.array([1,2,3])
    for f in faces:
        if all(item in idx_masked_vertices for item in f):
            faces_da_tenere.append(f)

    return scene_vertices[idx_masked_vertices], np.array(faces_da_tenere)


def write_obj_file(output_path, obj_vertices, obj_faces):
    with open(output_path, 'w') as f:
        f.write("# OBJ file\n")
        for v in obj_vertices:
            f.write("v %.4f %.4f %.4f\n" % (v[0], v[1], v[2]))
        for face in obj_faces:
            f.write("f")
            for v in face:
                f.write(" %d" % (v + 1))
            f.write("\n")


def crawl_object(scene_name, obj_name, output_name):
    # load scene and take vertices related to mask
    scene_file = open(scene_name, 'rb')
    plydata = PlyData.read(scene_file)
    mask_file = open(obj_name, "r")
    list_mask = [int(i) for i in mask_file.readlines()]
    np_mask = np.array(list_mask)
    idx_masked_vertices = np.where(np_mask != 0)[0]

    # organize vertices in numpy array
    num_verts = plydata['vertex'].count
    scene_vertices = np.zeros(shape=[num_verts, 3], dtype=np.float32)
    scene_vertices[:, 0] = plydata['vertex'].data['x']
    scene_vertices[:, 1] = plydata['vertex'].data['y']
    scene_vertices[:, 2] = plydata['vertex'].data['z']

    # select only obj-related faces
    faces = plydata["face"].data
    obj_vertices, np_faces_da_tenere = select_faces(faces, scene_vertices, idx_masked_vertices)

    # adjust vertices ordering
    rename_vertices = lambda f_list, v_list: [[v_list.index(v) for v in f] for f in f_list]
    obj_faces = rename_vertices(np_faces_da_tenere, idx_masked_vertices.tolist())

    # write down to disk
    write_obj_file(output_name, obj_vertices, obj_faces)




